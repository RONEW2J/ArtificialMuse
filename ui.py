import sys
import os
import requests

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QProgressBar, QFileDialog, QMessageBox, QSpinBox, QHBoxLayout, QTabWidget,
    QComboBox, QListWidget, QListWidgetItem, QMenu, QSplitter, QFrame,
    QGraphicsDropShadowEffect, QScrollArea, QGridLayout, QCheckBox, QGroupBox,
    QTextEdit, QButtonGroup
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, Signal, QSize
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QPainter, QPainterPath, QPixmap

from downloader import DownloadImageWorker
from styles import Styles
from viewer import ImagePreviewWidget


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Card(QFrame):
    """Современная карточка с тенью и закругленными углами"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        
        # Добавляем тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def focusInEvent(self, event):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(102, 126, 234, 100))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setGraphicsEffect(None)
        super().focusOutEvent(event)


class AnimatedButton(QPushButton):
    """Кнопка с анимацией нажатия"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)


class CheckBox(QCheckBox):
    """Современный чекбокс с улучшенным дизайном"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)


class StyledSpinBox(QSpinBox):
    """Стилизованный SpinBox"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)


class StyledComboBox(QComboBox):
    """Стилизованный ComboBox"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)


class ListWidget(QListWidget):
    """Современный список с карточками"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(4)
        self.setUniformItemSizes(True)


class ImageDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_style = "dark"
        self.remote_models_loaded = False
        self.remote_models_list = []
        self.local_models_list = [
            "flux-pro", "stable-diffusion", "vqgan-clip", "midjourney",
            "animegan", "pixel-art", "watercolor", "oil-painting"
        ]
        self.save_dir = ""
        self.styles = Styles()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(resource_path("resources/icon.png")))
        self.setWindowTitle("🎨 ArtificialMuse")
        self.setGeometry(200, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        # Основной layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Создаем сплиттер
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(3)
        splitter.setChildrenCollapsible(False)

        # Левая панель (основные настройки)
        left_panel = self.create_left_panel()
        left_panel.setMinimumWidth(450)
        left_panel.setMaximumWidth(600)

        # Правая панель (превью)
        right_panel = self.create_right_panel()
        right_panel.setMinimumWidth(400)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Применяем стили
        self.apply__style()

        # Настройка пресетов размеров
        self.setup_size_presets()

    def create_left_panel(self):
        """Создает левую панель с настройками"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок приложения
        header = self.create_header()
        layout.addWidget(header)

        # Табы
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        
        # Вкладка генерации
        generate_tab = self.create_generate_tab()
        settings_tab = self.create_settings_tab()
        about_tab = self.create_about_tab()
        
        tabs.addTab(generate_tab, "🎯 Генерация")
        tabs.addTab(settings_tab, "⚙️ Настройки")
        tabs.addTab(about_tab, "ℹ️ О программе")
        
        layout.addWidget(tabs)

        # Нижняя панель с кнопками
        bottom_panel = self.create_bottom_panel()
        layout.addWidget(bottom_panel)

        return panel

    def create_header(self):
        """Создает заголовок приложения"""
        header_card = Card()
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(25, 20, 25, 20)

        title = QLabel("AI Image Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")

        subtitle = QLabel("Создавайте потрясающие изображения с помощью ИИ")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitleLabel")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        return header_card

    def create_generate_tab(self):
        """Создает вкладку генерации"""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(QFrame.NoFrame)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # Карточка промпта
        prompt_card = self.create_prompt_card()
        layout.addWidget(prompt_card)

        # Карточка моделей
        models_card = self.create_models_card()
        layout.addWidget(models_card)

        # Карточка параметров
        params_card = self.create_parameters_card()
        layout.addWidget(params_card)

        layout.addStretch()
        scroll.setWidget(content)
        
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        
        return tab

    def create_prompt_card(self):
        """Создает карточку для ввода промпта"""
        card = Card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("📝 Описание изображения")
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        self.input_prompt = QTextEdit()
        self.input_prompt.setPlaceholderText("Например: Кот в космосе в стиле Ван Гога, детализированно, 4K качество...")
        self.input_prompt.setMaximumHeight(100)
        self.input_prompt.setObjectName("promptInput")
        layout.addWidget(self.input_prompt)

        return card

    def create_models_card(self):
        """Создает карточку выбора моделей"""
        card = Card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("🤖 Модели ИИ")
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        # Табы для локальных и удаленных моделей
        models_tabs = QTabWidget()
        models_tabs.setMaximumHeight(300)

        # Локальные модели
        local_tab = QWidget()
        local_layout = QVBoxLayout(local_tab)
        local_layout.setContentsMargins(10, 10, 10, 10)

        self.local_model_list = ListWidget()
        self.local_model_list.setMaximumHeight(200)
        
        for model in self.local_models_list:
            item = QListWidgetItem(f"🎨 {model}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.local_model_list.addItem(item)

        local_layout.addWidget(self.local_model_list)
        models_tabs.addTab(local_tab, "Базовые")

        # Удаленные модели
        remote_tab = QWidget()
        remote_layout = QVBoxLayout(remote_tab)
        remote_layout.setContentsMargins(10, 10, 10, 10)

        self.remote_model_list = ListWidget()
        self.remote_model_list.setMaximumHeight(150)
        remote_layout.addWidget(self.remote_model_list)

        self.refresh_models_button = AnimatedButton("🔄 Загрузить модели API")
        self.refresh_models_button.clicked.connect(self.load_remote_models)
        remote_layout.addWidget(self.refresh_models_button)

        models_tabs.addTab(remote_tab, "API модели")
        layout.addWidget(models_tabs)

        return card

    def create_parameters_card(self):
        """Создает карточку параметров генерации"""
        card = Card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("⚙️ Параметры генерации")
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        # Grid layout для параметров
        params_grid = QGridLayout()
        params_grid.setSpacing(15)

        # Количество изображений
        count_label = QLabel("Количество:")
        count_label.setObjectName("paramLabel")
        self.input_count = StyledSpinBox()
        self.input_count.setRange(1, 50)
        self.input_count.setValue(1)
        self.input_count.setSuffix(" шт.")

        params_grid.addWidget(count_label, 0, 0)
        params_grid.addWidget(self.input_count, 0, 1)

        # Размер изображения
        size_label = QLabel("Размер:")
        size_label.setObjectName("paramLabel")
        self.combo_preset = StyledComboBox()
        
        params_grid.addWidget(size_label, 1, 0)
        params_grid.addWidget(self.combo_preset, 1, 1)

        # Пользовательские размеры
        self.input_width = StyledSpinBox()
        self.input_width.setRange(256, 4096)
        self.input_width.setValue(1024)
        self.input_width.setSuffix(" px")
        
        self.input_height = StyledSpinBox()
        self.input_height.setRange(256, 4096)
        self.input_height.setValue(1024)
        self.input_height.setSuffix(" px")

        params_grid.addWidget(QLabel("Ширина:"), 2, 0)
        params_grid.addWidget(self.input_width, 2, 1)
        params_grid.addWidget(QLabel("Высота:"), 3, 0)
        params_grid.addWidget(self.input_height, 3, 1)

        layout.addLayout(params_grid)
        return card

    def create_settings_tab(self):
        """Создает вкладку настроек"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Карточка папки сохранения
        folder_card = Card()
        folder_layout = QVBoxLayout(folder_card)
        folder_layout.setContentsMargins(25, 20, 25, 20)
        folder_layout.setSpacing(15)

        folder_title = QLabel("📁 Папка сохранения")
        folder_title.setObjectName("cardTitle")
        folder_layout.addWidget(folder_title)

        self.folder_button = AnimatedButton("Выбрать папку")
        self.folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_button)

        self.folder_path_label = QLabel("Папка не выбрана")
        self.folder_path_label.setObjectName("pathLabel")
        self.folder_path_label.setWordWrap(True)
        folder_layout.addWidget(self.folder_path_label)

        layout.addWidget(folder_card)

        # Карточка темы
        theme_card = Card()
        theme_layout = QVBoxLayout(theme_card)
        theme_layout.setContentsMargins(25, 20, 25, 20)
        theme_layout.setSpacing(15)

        theme_title = QLabel("🎨 Внешний вид")
        theme_title.setObjectName("cardTitle")
        theme_layout.addWidget(theme_title)

        theme_buttons_layout = QHBoxLayout()
        self.dark_theme_btn = AnimatedButton("🌙 Темная")
        self.light_theme_btn = AnimatedButton("☀️ Светлая")
        
        self.dark_theme_btn.clicked.connect(lambda: self.set_theme("dark"))
        self.light_theme_btn.clicked.connect(lambda: self.set_theme("light"))
        
        theme_buttons_layout.addWidget(self.dark_theme_btn)
        theme_buttons_layout.addWidget(self.light_theme_btn)
        theme_layout.addLayout(theme_buttons_layout)

        layout.addWidget(theme_card)
        layout.addStretch()

        return tab

    def create_about_tab(self):
        """Создает вкладку 'О программе'"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        card = Card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.setSpacing(20)

        # Заголовок
        title = QLabel("🎨 AI Image Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("aboutTitle")
        card_layout.addWidget(title)

        # Описание
        description = QLabel(
            "Мощное приложение для генерации изображений с помощью "
            "различных моделей искусственного интеллекта через API Pollinations.AI"
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description.setObjectName("aboutDescription")
        card_layout.addWidget(description)

        # Информация об авторе
        author_info = QLabel(
            "<b>Автор:</b> Ronew2J<br>"
            "<b>Telegram:</b> <a href='https://t.me/RonewJJ' style='color: #667eea;'>@RonewJJ</a><br>"
            "<b>Email:</b> <a href='mailto:ronew2j@gmail.com' style='color: #667eea;'>ronew2j@gmail.com</a>"
        )
        author_info.setAlignment(Qt.AlignCenter)
        author_info.setTextInteractionFlags(Qt.TextBrowserInteraction)
        author_info.setOpenExternalLinks(True)
        author_info.setObjectName("authorInfo")
        card_layout.addWidget(author_info)

        layout.addWidget(card)
        layout.addStretch()

        return tab

    def create_bottom_panel(self):
        """Создает нижнюю панель с кнопкой генерации и прогресс-баром"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # Кнопка генерации
        self.generate_button = AnimatedButton("🚀 Начать генерацию")
        self.generate_button.setObjectName("generateButton")
        self.generate_button.setMinimumHeight(50)
        self.generate_button.clicked.connect(self.start_download)
        layout.addWidget(self.generate_button)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        self.progress_bar.setObjectName("ProgressBar")
        layout.addWidget(self.progress_bar)

        return panel

    def create_right_panel(self):
        """Создает правую панель с превью"""
        panel = Card()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("🖼️ Превью изображений")
        title.setObjectName("cardTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.preview = ImagePreviewWidget()
        layout.addWidget(self.preview)

        return panel

    def setup_size_presets(self):
        """Настраивает пресеты размеров"""
        self.preset_sizes = {
            0: (None, None),
            1: (1920, 1080),
            2: (2560, 1440),
            3: (3840, 2160),
            4: (1024, 1024),
            5: (2048, 2048),
            6: (1080, 1920),
            7: (1440, 2560),
            8: (2160, 3840),
        }

        presets = [
            "Пользовательский",
            "Full HD (1920×1080)",
            "2K (2560×1440)",
            "4K (3840×2160)",
            "Квадрат 1K (1024×1024)",
            "Квадрат 2K (2048×2048)",
            "Телефон Full HD (1080×1920)",
            "Телефон 2K (1440×2560)",
            "Телефон 4K (2160×3840)"
        ]

        for preset in presets:
            self.combo_preset.addItem(preset)

        self.combo_preset.currentIndexChanged.connect(self.preset_changed)
        self.preset_changed(0)

    def apply__style(self):
        """Применяет современные стили"""
        stylesheet = self.styles.get_style(self.current_style)
        self.setStyleSheet(stylesheet)

    def set_theme(self, theme):
        """Устанавливает тему"""
        self.current_style = theme
        self.apply__style()
        
        # Обновляем состояние кнопок темы
        if theme == "dark":
            self.dark_theme_btn.setProperty("active", True)
            self.light_theme_btn.setProperty("active", False)
        else:
            self.dark_theme_btn.setProperty("active", False)
            self.light_theme_btn.setProperty("active", True)
        
        self.dark_theme_btn.style().unpolish(self.dark_theme_btn)
        self.dark_theme_btn.style().polish(self.dark_theme_btn)
        self.light_theme_btn.style().unpolish(self.light_theme_btn)
        self.light_theme_btn.style().polish(self.light_theme_btn)

    def preset_changed(self, index):
        """Обработка изменения пресета размера"""
        size = self.preset_sizes.get(index, (None, None))
        if size[0] is None:
            self.input_width.setEnabled(True)
            self.input_height.setEnabled(True)
        else:
            w, h = size
            self.input_width.setValue(w)
            self.input_height.setValue(h)
            self.input_width.setEnabled(False)
            self.input_height.setEnabled(False)

    def select_folder(self):
        """Выбор папки для сохранения"""
        start_dir = self.save_dir if self.save_dir else os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(
            self, "Выберите папку для сохранения", start_dir
        )
        if folder:
            self.save_dir = folder
            self.folder_path_label.setText(f"📁 {self.save_dir}")
            self.folder_button.setText("✅ Папка выбрана")

    def load_remote_models(self):
        """Загружает список удаленных моделей"""
        self.remote_model_list.clear()
        self.refresh_models_button.setEnabled(False)
        self.refresh_models_button.setText("⏳ Загрузка...")
        QApplication.processEvents()

        try:
            response = requests.get("https://image.pollinations.ai/models", timeout=20)
            if response.status_code == 200:
                models = response.json()
                if isinstance(models, list) and all(isinstance(m, str) for m in models):
                    models.sort()
                    for model in models:
                        item = QListWidgetItem(f"🔗 {model}")
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item.setCheckState(Qt.Unchecked)
                        self.remote_model_list.addItem(item)
                    self.remote_models_loaded = True
                    self.refresh_models_button.setText("✅ Модели загружены")
                else:
                    QMessageBox.warning(self, "Ошибка", "Неожиданный формат данных API")
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка загрузки: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.warning(self, "Ошибка сети", f"Не удалось подключиться: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
        finally:
            self.refresh_models_button.setEnabled(True)
            if not self.remote_models_loaded:
                self.refresh_models_button.setText("🔄 Загрузить модели API")

    def start_download(self):
        """Запускает процесс генерации изображений"""
        prompt = self.input_prompt.toPlainText().strip()
        count = self.input_count.value()
        width = self.input_width.value()
        height = self.input_height.value()

        # Собираем выбранные модели
        local_selected = []
        for i in range(self.local_model_list.count()):
            item = self.local_model_list.item(i)
            if item.checkState() == Qt.Checked:
                local_selected.append(item.text().replace("🎨 ", ""))

        remote_selected = []
        for i in range(self.remote_model_list.count()):
            item = self.remote_model_list.item(i)
            if item.checkState() == Qt.Checked:
                remote_selected.append(item.text().replace("🔗 ", ""))

        all_models = local_selected + remote_selected

        # Валидация
        if not prompt:
            QMessageBox.warning(self, "Ошибка", "Введите описание изображения!")
            return
        if not all_models:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одну модель!")
            return
        if not self.save_dir:
            QMessageBox.warning(self, "Ошибка", "Выберите папку для сохранения!")
            return

        # Отключаем интерфейс
        self.set_ui_enabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("🚀 Начинаем генерацию...")

        # Запускаем воркер
        self.worker = DownloadImageWorker(
            prompt=prompt,
            final_width=width,
            final_height=height,
            models=all_models,
            save_dir=self.save_dir,
            count=count
        )
        
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.image_generated.connect(self.preview.add_image)
        self.worker.error_occurred.connect(self.show_generation_error)
        self.worker.start()

    def set_ui_enabled(self, enabled):
        """Включает/выключает элементы интерфейса"""
        self.generate_button.setEnabled(enabled)
        self.folder_button.setEnabled(enabled)
        self.refresh_models_button.setEnabled(enabled)
        self.input_prompt.setEnabled(enabled)
        self.input_count.setEnabled(enabled)
        self.combo_preset.setEnabled(enabled)
        self.local_model_list.setEnabled(enabled)
        self.remote_model_list.setEnabled(enabled)
        
        if not enabled:
            self.generate_button.setText("⏳ Генерация...")
        else:
            self.generate_button.setText("🚀 Начать генерацию")

    def update_progress(self, value):
        """Обновляет прогресс-бар"""
        self.progress_bar.setValue(value)
        if value < 100:
            self.progress_bar.setFormat(f"🎨 Генерация... {value}%")
        else:
            self.progress_bar.setFormat("✅ Готово!")

    def show_generation_error(self, error_msg):
        """Показывает ошибку генерации"""
        print(f"Ошибка генерации: {error_msg}")

    def download_finished(self, success, failed_images):
        """Обработка завершения генерации"""
        self.set_ui_enabled(True)
        
        if success and not failed_images:
            self.progress_bar.setFormat("✅ Все изображения готовы!")
            QMessageBox.information(
                self, "🎉 Успех!", 
                "Все изображения успешно сгенерированы и сохранены!"
            )
        elif failed_images:
            failed_count = len(failed_images)
            self.progress_bar.setFormat(f"⚠️ Готово с ошибками ({failed_count})")
            
            msg = f"Генерация завершена, но {failed_count} изображений не удалось создать:\n\n"
            for i, fail in enumerate(failed_images[:5]):
                msg += f"• {fail['model']}: {fail['error']}\n"
            if failed_count > 5:
                msg += f"\n... и еще {failed_count - 5} ошибок."
                
            QMessageBox.warning(self, "⚠️ Завершено с ошибками", msg)
        else:
            self.progress_bar.setFormat("❌ Ошибка!")
            QMessageBox.critical(
                self, "❌ Критическая ошибка",
                "Произошла критическая ошибка во время генерации."
            )
