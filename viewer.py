import os
from PySide6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QMenu, QDialog, QLabel, QHBoxLayout, QPushButton, QApplication,
    QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QMouseEvent, QIcon


def clamp_index(index, maximum):
    if maximum <= 0:
        return 0
    if index < 0:
        return 0
    if index >= maximum:
        return maximum - 1
    return index


class ImageViewerDialog(QDialog):

    def __init__(self, images, current_index=0, parent=None):
        super().__init__(parent)
        self.images = images
        self.current_index = current_index
        self.setWindowTitle("Предпросмотр изображения")
        self.setMinimumSize(800, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label, stretch=1)

        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)

        self.prev_button = QPushButton("◀ Назад")
        self.prev_button.clicked.connect(self.show_prev)
        self.next_button = QPushButton("Вперёд ▶")
        self.next_button.clicked.connect(self.show_next)

        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addSpacing(20)
        nav_layout.addWidget(self.next_button)
        nav_layout.addStretch()

        main_layout.addLayout(nav_layout)

        self.show_image(self.current_index)

    def show_image(self, index):
        if not self.images:
            self.label.setText("Нет изображений для просмотра")
            self.setWindowTitle("Предпросмотр изображения")
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.current_index = clamp_index(index, len(self.images))
        current_item = self.images[self.current_index]
        image_path = None
        if isinstance(current_item, ImageItemWidget) and \
                hasattr(current_item, 'image_path'):
            image_path = current_item.image_path

        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(self.label.size() * 0.95, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)
                self.setWindowTitle(
                    f"Просмотр {self.current_index + 1}/{len(self.images)}: {os.path.basename(image_path)}")
            else:
                self.label.setText(f"Не удалось загрузить\nизображение:\n{os.path.basename(image_path)}")
                self.setWindowTitle(f"Ошибка загрузки {self.current_index + 1}/{len(self.images)}")
        else:
            self.label.setText(f"Ошибка: Изображение {self.current_index + 1} не найдено или повреждено.")
            self.setWindowTitle(f"Ошибка просмотра {self.current_index + 1}/{len(self.images)}")

        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.images) - 1)

    def show_prev(self):
        self.show_image(self.current_index - 1)

    def show_next(self):
        self.show_image(self.current_index + 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.prev_button.isEnabled(): self.show_prev()
        elif event.key() == Qt.Key_Right:
            if self.next_button.isEnabled(): self.show_next()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            if self.prev_button.isEnabled(): self.show_prev()
        elif delta < 0:
            if self.next_button.isEnabled(): self.show_next()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.images and self.current_index >= 0:
            self.show_image(self.current_index)


class ImageItemWidget(QWidget):
    request_delete = Signal(object)

    def __init__(self, image_path, preview_widget, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.preview_widget = preview_widget
        self.selected = False

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.thumbnail_size = QSize(280, 280)
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            thumbnail = pixmap.scaled(self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(thumbnail)
            self.setToolTip(
                f"{os.path.basename(image_path)}\n{pixmap.width()}x{pixmap.height()} px")
        else:
            self.label.setText(f"Не удалось\nзагрузить\n{os.path.basename(image_path)}")
            self.setToolTip(f"Ошибка загрузки: {os.path.basename(image_path)}")

        self.delete_button = QPushButton("✖")
        self.delete_button.setFlat(True)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(200, 0, 0, 0.6); /* Полупрозрачный красный */
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px; /* Размер крестика */
                padding: 0px; /* Убираем паддинг у кнопки удаления */
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.8); /* Ярче при наведении */
            }
        """)
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setParent(self)
        self.delete_button.move(self.width() - self.delete_button.width() - 3, 3)
        self.delete_button.clicked.connect(self.delete_image_requested)
        self.delete_button.raise_()

        self.update_style()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.delete_button.move(self.width() - self.delete_button.width() - 3, 3)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:
                self.preview_widget.toggle_item_selection(self)
            elif modifiers == Qt.ShiftModifier:
                self.preview_widget.select_range(self)
            else:
                if not self.selected:
                    self.preview_widget.clear_selection()
                    self.preview_widget.toggle_item_selection(self)
                self.preview_widget.set_last_selected(self)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            try:
                all_visible_widgets = self.preview_widget.get_visible_items()
                if self in all_visible_widgets:
                    index = all_visible_widgets.index(self)
                    dialog = ImageViewerDialog(all_visible_widgets, current_index=index, parent=self.preview_widget)
                    dialog.exec_()
                else:
                    print("Ошибка: элемент не найден в списке видимых виджетов.")

            except ValueError:
                print("Ошибка: не удалось найти индекс элемента в списке видимых.")
            except Exception as e:
                print(f"Ошибка при открытии диалога: {e}")

    def set_selected(self, selected: bool):
        if self.selected != selected:
            self.selected = selected
            self.update_style()

    def update_style(self):
        padding = 5
        border_width = 3
        if self.selected:
            self.setStyleSheet(
                f"QWidget {{ border: {border_width}px solid #007BFF; border-radius: 5px; padding: {padding}px; background-color: rgba(0, 123, 255, 0.1); }}")
        else:
            self.setStyleSheet(
                f"QWidget {{ border: {border_width}px solid transparent; border-radius: 5px; padding: {padding}px; background-color: transparent; }}")

    def delete_image_requested(self):
        self.request_delete.emit(self)


class ImagePreviewWidget(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._items = []
        self.selected_items = []
        self.last_selected_item = None

    def add_image(self, image_path):
        if not os.path.exists(image_path):
            print(f"Предупреждение: Попытка добавить несуществующий файл: {image_path}")
            return

        item = ImageItemWidget(image_path, preview_widget=self)
        item.request_delete.connect(self.remove_image_widget)
        self.main_layout.addWidget(item)
        self._items.append(item)

    def remove_image_widget(self, item_widget):
        """Удаляет виджет изображения и сам файл."""
        if item_widget not in self._items:
            print("Предупреждение: Попытка удалить уже удаленный виджет.")
            return

        reply = QMessageBox.question(self, "Подтверждение удаления",
                                     f"Вы уверены, что хотите удалить файл?\n{os.path.basename(item_widget.image_path)}\nЭто действие необратимо.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                image_path_to_delete = item_widget.image_path
                if os.path.exists(image_path_to_delete):
                    os.remove(image_path_to_delete)
                    print(f"Файл удален: {image_path_to_delete}")

                self._items.remove(item_widget)
                if item_widget in self.selected_items:
                    self.selected_items.remove(item_widget)
                    if self.last_selected_item == item_widget:
                        self.last_selected_item = self.selected_items[-1] if self.selected_items else None

                self.main_layout.removeWidget(item_widget)
                item_widget.deleteLater()

            except OSError as e:
                QMessageBox.warning(self, "Ошибка удаления файла", f"Не удалось удалить файл:\n{e}")
                print(f"Ошибка удаления файла {image_path_to_delete}: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при удалении: {e}")
                print(f"Неожиданная ошибка при удалении {image_path_to_delete}: {e}")

    def toggle_item_selection(self, item):
        """Переключает выделение для одного элемента."""
        if item.selected:
            item.set_selected(False)
            if item in self.selected_items:
                self.selected_items.remove(item)
            if self.last_selected_item == item:
                self.last_selected_item = self.selected_items[-1] if self.selected_items else None
        else:
            item.set_selected(True)
            if item not in self.selected_items:
                self.selected_items.append(item)
            self.last_selected_item = item

    def clear_selection(self):
        """Снимает выделение со всех элементов."""
        items_to_clear = list(self.selected_items)
        for item in items_to_clear:
            if item in self._items:
                item.set_selected(False)
        self.selected_items.clear()
        self.last_selected_item = None

    def set_last_selected(self, item):
        """Устанавливает элемент как последний активный (для Shift-клика)."""
        self.last_selected_item = item

    def select_range(self, target_item):
        """Выделяет диапазон элементов с помощью Shift."""
        if not self.last_selected_item or self.last_selected_item not in self._items:
            self.clear_selection()
            if target_item in self._items:
                self.toggle_item_selection(target_item)
            return

        if target_item not in self._items:
            print("Ошибка: целевой элемент для выделения диапазона не найден.")
            return

        try:
            start_index = self._items.index(self.last_selected_item)
            end_index = self._items.index(target_item)
        except ValueError:
            print("Ошибка: один из элементов для выделения диапазона не найден в _items.")
            return

        if start_index > end_index:
            start_index, end_index = end_index, start_index

        self.clear_selection()

        for i in range(start_index, end_index + 1):
            if i < len(self._items):
                current_item = self._items[i]
                if not current_item.selected:
                    current_item.set_selected(True)
                    self.selected_items.append(current_item)
        self.last_selected_item = target_item

    def get_visible_items(self):
        """Возвращает список видимых виджетов ImageItemWidget."""
        return self._items

    def contextMenuEvent(self, event):
        """Создает контекстное меню для выделенных элементов."""
        child = self.childAt(event.pos())
        item_under_cursor = None
        while child is not None:
            if isinstance(child, ImageItemWidget):
                item_under_cursor = child
                break
            child = child.parent()

        if item_under_cursor and item_under_cursor not in self.selected_items:
            self.clear_selection()
            self.toggle_item_selection(item_under_cursor)

        if not self.selected_items:
            return

        menu = QMenu(self)
        delete_action = menu.addAction(f"Удалить выбранные ({len(self.selected_items)})")
        open_folder_action = None
        if len(self.selected_items) == 1:
            open_folder_action = menu.addAction("Открыть папку с файлом")

        menu.addSeparator()
        clear_selection_action = menu.addAction("Снять выделение")

        action = menu.exec_(event.globalPos())

        if action == delete_action:
            items_to_delete = list(self.selected_items)
            count = len(items_to_delete)

            reply = QMessageBox.question(self, "Подтверждение удаления",
                                         f"Вы уверены, что хотите удалить выбранные файлы ({count} шт.)?\nЭто действие необратимо.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                deleted_count = 0
                error_messages = []
                for item in items_to_delete:
                    try:
                        if item in self._items:
                            image_path_to_delete = item.image_path
                            if os.path.exists(image_path_to_delete):
                                os.remove(image_path_to_delete)

                            self._items.remove(item)
                            if item in self.selected_items:
                                self.selected_items.remove(item)

                            self.main_layout.removeWidget(item)
                            item.deleteLater()
                            deleted_count += 1
                        else:
                            print(f"Предупреждение: Попытка удалить элемент {item}, который уже не в списке _items.")


                    except Exception as e:
                        error_msg = f"Не удалось удалить {os.path.basename(item.image_path)}: {e}"
                        print(error_msg)
                        error_messages.append(error_msg)

                print(f"Удалено {deleted_count} из {count} выбранных файлов.")
                if error_messages:
                    QMessageBox.warning(self, "Ошибки при удалении", "\n".join(error_messages))

                self.last_selected_item = None

        elif action == open_folder_action:
            if len(self.selected_items) == 1:
                try:
                    item = self.selected_items[0]
                    folder_path = os.path.dirname(item.image_path)
                    from PySide2.QtGui import QDesktopServices
                    from PySide2.QtCore import QUrl
                    QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось открыть папку: {e}")

        elif action == clear_selection_action:
            self.clear_selection()
