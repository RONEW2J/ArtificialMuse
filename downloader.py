import sys
import os
import requests
import random
import datetime
from PIL import Image
from io import BytesIO
from PySide6.QtCore import QThread, Signal


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DownloadImageWorker(QThread):
    progress = Signal(int)
    finished = Signal(bool, list)
    image_generated = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, prompt, final_width, final_height, models, save_dir, count):
        super().__init__()
        self.prompt = prompt
        self.final_width = final_width
        self.final_height = final_height
        self.models = models
        self.save_dir = save_dir
        self.count = count
        self._is_running = True

    def run(self):
        fails = []
        try:
            total = len(self.models) * self.count
            if total == 0:
                self.finished.emit(True, [])
                return

            done = 0

            for model in self.models:
                if not self._is_running: break
                for i in range(1, self.count + 1):
                    if not self._is_running: break
                    try:
                        seed = random.randint(1, 1000000)
                        encoded_prompt = requests.utils.quote(self.prompt)
                        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

                        params = {
                            "model": model,
                            "seed": seed,
                            "width": self.final_width,
                            "height": self.final_height,
                            "nologo": "true"
                        }
                        print(f"Запрос: {url} с параметрами {params}")

                        r = requests.get(url, params=params, timeout=60, stream=True)

                        r.raise_for_status()

                        content_type = r.headers.get('content-type')
                        if content_type and 'image' in content_type:
                            img = Image.open(BytesIO(r.content))
                            safe_model_name = "".join(c if c.isalnum() else "_" for c in model)
                            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                            filename = f"generated_{safe_model_name}_{timestamp}_{i}.jpg"
                            path = os.path.join(self.save_dir, filename)
                            img.save(path, quality=95)

                            self.image_generated.emit(path)

                            done += 1
                            percent = int(done / total * 100)
                            self.progress.emit(percent)
                        else:
                            error_message = f"Модель '{model}' (попытка {i}) вернула не изображение (Content-Type: {content_type}). Ответ:\n{r.text[:200]}..."
                            print(error_message)
                            self.error_occurred.emit(error_message)
                            fails.append({
                                'model': model,
                                'count': i,
                                'error': f"Неверный Content-Type: {content_type}"
                            })


                    except requests.exceptions.Timeout:
                        error_message = f"Модель '{model}' (попытка {i}): Время ожидания запроса истекло."
                        print(error_message)
                        self.error_occurred.emit(error_message)
                        fails.append({
                            'model': model,
                            'count': i,
                            'error': "Timeout"
                        })
                    except requests.exceptions.RequestException as e:
                        error_message = f"Модель '{model}' (попытка {i}): Ошибка сети/HTTP: {e}"
                        print(error_message)
                        self.error_occurred.emit(error_message)
                        fails.append({
                            'model': model,
                            'count': i,
                            'error': str(e)
                        })
                    except Exception as e:
                        error_message = f"Модель '{model}' (попытка {i}): Неожиданная ошибка: {e}"
                        print(error_message)
                        self.error_occurred.emit(error_message)
                        fails.append({
                            'model': model,
                            'count': i,
                            'error': str(e)
                        })

                if not self._is_running: break

            final_success = done > 0 and self._is_running
            self.finished.emit(final_success, fails)

        except Exception as e:
            error_message = f"Критическая ошибка в потоке генерации: {e}"
            print(error_message)
            self.error_occurred.emit(error_message)
            self.finished.emit(False, [{'model': 'N/A', 'count': 0, 'error': str(e)}])

    def stop(self):
        """Метод для запроса остановки потока."""
        print("Запрос на остановку потока...")
        self._is_running = False
