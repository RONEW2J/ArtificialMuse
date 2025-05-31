class Styles:
    """ styles for AI Image Generator with dark and light theme support"""
    
    def __init__(self):
        self.dark_style = self._create_dark_style()
        self.light_style = self._create_light_style()
        
    def get_style(self, theme="dark"):
        """
        Returns style for specified theme
        :param theme: "dark" or "light" 
        :return: string with CSS styles
        """
        return self.dark_style if theme == "dark" else self.light_style

    def _create_dark_style(self):
        """Creates dark theme in modern style"""
        return """
/* =========================== ОСНОВНЫЕ КОМПОНЕНТЫ =========================== */

QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'San Francisco', system-ui, -apple-system, sans-serif;
    font-size: 14px;
    font-weight: 400;
    selection-background-color: #667eea;
    selection-color: white;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #1a1a1a, stop:1 #2d2d2d);
}

/* =========================== ЛЕЙБЛЫ И ТЕКСТ =========================== */

QLabel {
    color: #e0e0e0;
    border: none;
    padding: 2px;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    padding: 8px 0;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #b0b0b0;
    font-weight: 300;
    margin-bottom: 10px;
}

QLabel#cardTitle {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    padding: 0 0 8px 0;
    border-bottom: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    margin-bottom: 8px;
}

QLabel#paramLabel {
    font-weight: 500;
    color: #d0d0d0;
    font-size: 13px;
}

QLabel#pathLabel {
    color: #a0a0a0;
    font-style: italic;
    padding: 8px 12px;
    background-color: #2a2a2a;
    border-radius: 8px;
    border-left: 3px solid #667eea;
}

QLabel#aboutTitle {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 10px 0;
}

QLabel#aboutDescription {
    font-size: 14px;
    color: #c0c0c0;
    line-height: 1.5;
    margin: 15px 0;
}

QLabel#authorInfo {
    font-size: 13px;
    color: #b0b0b0;
    line-height: 1.6;
    margin: 20px 0;
}

/* =========================== КАРТОЧКИ =========================== */

Card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #2a2a2a, stop:1 #1f1f1f);
    border: 1px solid #3a3a3a;
    border-radius: 16px;
    margin: 4px;
}

Card:hover {
    border: 1px solid #667eea;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #2e2e2e, stop:1 #232323);
}

/* =========================== КНОПКИ =========================== */

AnimatedButton, QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    font-size: 14px;
    min-height: 20px;
    text-align: center;
}

AnimatedButton:hover, QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #5a67d8, stop:1 #6b46c1);
    margin-top: -2px;
    margin-bottom: 2px;
}

AnimatedButton:pressed, QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #4c51bf, stop:1 #553c9a);
    margin: 0px;
}

AnimatedButton:disabled, QPushButton:disabled {
    background: #404040;
    color: #808080;
    border: 1px solid #555555;
}

QPushButton#generateButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #ff6b6b, stop:1 #ee5a24);
    font-size: 16px;
    font-weight: 700;
    min-height: 30px;
    border-radius: 14px;
}

QPushButton#generateButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #ff5252, stop:1 #e55100);
}

QPushButton[active="true"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #48bb78, stop:1 #38a169);
    border: 2px solid #68d391;
}

/* =========================== ПОЛЯ ВВОДА =========================== */

QLineEdit, QTextEdit {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 2px solid #404040;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 14px;
    selection-background-color: #667eea;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #667eea;
    background-color: #2e2e2e;
}

QTextEdit#promptInput {
    font-family: 'Consolas', 'Monaco', monospace;
    line-height: 1.4;
    border-radius: 12px;
}

/* =========================== ВЫПАДАЮЩИЕ СПИСКИ =========================== */

StyledComboBox, QComboBox {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 2px solid #404040;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 14px;
    min-height: 20px;
}

StyledComboBox:hover, QComboBox:hover {
    border-color: #667eea;
    background-color: #2e2e2e;
}

StyledComboBox:focus, QComboBox:focus {
    border: 2px solid #667eea;
    background-color: #2e2e2e;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid #e0e0e0;
    width: 0;
    height: 0;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 1px solid #667eea;
    border-radius: 8px;
    selection-background-color: #667eea;
    color: #e0e0e0;
    padding: 4px;
}

/* =========================== СПИНБОКСЫ =========================== */

StyledSpinBox, QSpinBox {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 2px solid #404040;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 14px;
    min-height: 20px;
}

StyledSpinBox:hover, QSpinBox:hover {
    border-color: #667eea;
    background-color: #2e2e2e;
}

StyledSpinBox:focus, QSpinBox:focus {
    border: 2px solid #667eea;
    background-color: #2e2e2e;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #404040;
    border: none;
    width: 20px;
    border-radius: 4px;
    margin: 2px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #667eea;
}

QSpinBox::up-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 6px solid #e0e0e0;
    width: 0;
    height: 0;
}

QSpinBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #e0e0e0;
    width: 0;
    height: 0;
}

/* =========================== СПИСКИ =========================== */

ListWidget, QListWidget {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 2px solid #404040;
    border-radius: 12px;
    padding: 8px;
    alternate-background-color: #2e2e2e;
    selection-background-color: #667eea;
}

QListWidget::item {
    background-color: #333333;
    border: 1px solid #404040;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 2px 0;
    font-weight: 500;
}

QListWidget::item:hover {
    background-color: #3a3a3a;
    border-color: #667eea;
}

QListWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border-color: #667eea;
}

QListWidget::item::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #606060;
    border-radius: 4px;
    background-color: #2a2a2a;
    margin-right: 8px;
}

QListWidget::item::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    border-color: #667eea;
}

/* =========================== ЧЕКБОКСЫ =========================== */

CheckBox, QCheckBox {
    color: #e0e0e0;
    font-weight: 500;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #606060;
    border-radius: 6px;
    background-color: #2a2a2a;
}

QCheckBox::indicator:hover {
    border-color: #667eea;
    background-color: #2e2e2e;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    border-color: #667eea;
}

/* =========================== ПРОГРЕСС-БАР =========================== */

QProgressBar, QProgressBar#ProgressBar {
    background-color: #2a2a2a;
    border: 2px solid #404040;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 14px;
    color: #e0e0e0;
    padding: 2px;
    min-height: 20px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 10px;
    margin: 2px;
}

/* =========================== ВКЛАДКИ =========================== */

QTabWidget::pane {
    border: none;
    background-color: transparent;
    border-radius: 12px;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #3a3a3a, stop:1 #2a2a2a);
    color: #b0b0b0;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border: 2px solid #404040;
    border-bottom: none;
    font-weight: 600;
    min-width: 80px;
}

QTabBar::tab:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #4a4a4a, stop:1 #3a3a3a);
    color: #e0e0e0;
    border-color: #667eea;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border-color: #667eea;
    border-bottom: 2px solid #667eea;
}

/* =========================== ПРОКРУТКА =========================== */

QScrollArea {
    background-color: transparent;
    border: none;
    border-radius: 8px;
}

QScrollBar:vertical {
    background-color: #2a2a2a;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 6px;
    min-height: 30px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #5a67d8, stop:1 #6b46c1);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0;
}

QScrollBar:horizontal {
    background-color: #2a2a2a;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 6px;
    min-width: 30px;
    margin: 2px;
}

/* =========================== РАЗДЕЛИТЕЛИ =========================== */

QSplitter::handle {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #404040, stop:1 #606060);
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 6px;
}

QSplitter::handle:vertical {
    height: 6px;
}

QSplitter::handle:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
}

/* =========================== МЕНЮ И ДИАЛОГИ =========================== */

QMenu {
    background-color: #2a2a2a;
    border: 2px solid #667eea;
    border-radius: 8px;
    padding: 4px;
    color: #e0e0e0;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 4px;
    margin: 1px;
}

QMenu::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
}

QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #1a1a1a, stop:1 #2d2d2d);
    color: #e0e0e0;
}

/* =========================== ГРУППЫ =========================== */

QGroupBox {
    color: #e0e0e0;
    border: 2px solid #404040;
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px 0 8px;
    color: #ffffff;
    background-color: #1a1a1a;
}
"""

    def _create_light_style(self): 
        """Создает светлую тему в современном стиле"""
        return """
/* =========================== ОСНОВНЫЕ КОМПОНЕНТЫ =========================== */

QWidget {
    background-color: #fafafa;
    color: #2d3748;
    font-family: 'Segoe UI', 'San Francisco', system-ui, -apple-system, sans-serif;
    font-size: 14px;
    font-weight: 400;
    selection-background-color: #667eea;
    selection-color: white;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #fafafa, stop:1 #f7fafc);
}

/* =========================== ЛЕЙБЛЫ И ТЕКСТ =========================== */

QLabel {
    color: #2d3748;
    border: none;
    padding: 2px;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: 700;
    color: #1a202c;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    -webkit-background-clip: text;
    background-clip: text;
    padding: 8px 0;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #718096;
    font-weight: 300;
    margin-bottom: 10px;
}

QLabel#cardTitle {
    font-size: 16px;
    font-weight: 600;
    color: #1a202c;
    padding: 0 0 8px 0;
    border-bottom: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    margin-bottom: 8px;
}

QLabel#paramLabel {
    font-weight: 500;
    color: #4a5568;
    font-size: 13px;
}

QLabel#pathLabel {
    color: #718096;
    font-style: italic;
    padding: 8px 12px;
    background-color: #edf2f7;
    border-radius: 8px;
    border-left: 3px solid #667eea;
}

QLabel#aboutTitle {
    font-size: 24px;
    font-weight: 700;
    color: #1a202c;
    margin: 10px 0;
}

QLabel#aboutDescription {
    font-size: 14px;
    color: #4a5568;
    line-height: 1.5;
    margin: 15px 0;
}

QLabel#authorInfo {
    font-size: 13px;
    color: #718096;
    line-height: 1.6;
    margin: 20px 0;
}

/* =========================== КАРТОЧКИ =========================== */

Card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #ffffff, stop:1 #f7fafc);
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    margin: 4px;
}

Card:hover {
    border: 1px solid #667eea;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #ffffff, stop:1 #edf2f7);
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
}

/* =========================== КНОПКИ =========================== */

AnimatedButton, QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    font-size: 14px;
    min-height: 20px;
    text-align: center;
}

AnimatedButton:hover, QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #5a67d8, stop:1 #6b46c1);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transform: translateY(-2px);
}

AnimatedButton:pressed, QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #4c51bf, stop:1 #553c9a);
    transform: translateY(0px);
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

AnimatedButton:disabled, QPushButton:disabled {
    background: #cbd5e0;
    color: #a0aec0;
    border: 1px solid #e2e8f0;
}

QPushButton#generateButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #ff6b6b, stop:1 #ee5a24);
    font-size: 16px;
    font-weight: 700;
    min-height: 30px;
    border-radius: 14px;
}

QPushButton#generateButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #ff5252, stop:1 #e55100);
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

/* =========================== ПОЛЯ ВВОДА =========================== */

QLineEdit, QTextEdit {
    background-color: #ffffff;
    color: #2d3748;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 14px;
    selection-background-color: #667eea;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #667eea;
    background-color: #f7fafc;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

QTextEdit#promptInput {
    font-family: 'Consolas', 'Monaco', monospace;
    line-height: 1.4;
    border-radius: 12px;
}

/* =========================== ВЫПАДАЮЩИЕ СПИСКИ =========================== */

StyledComboBox, QComboBox {
    background-color: #ffffff;
    color: #2d3748;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 14px;
    min-height: 20px;
}

StyledComboBox:hover, QComboBox:hover {
    border-color: #667eea;
    background-color: #f7fafc;
}

StyledComboBox:focus, QComboBox:focus {
    border: 2px solid #667eea;
    background-color: #f7fafc;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid #4a5568;
    width: 0;
    height: 0;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #667eea;
    border-radius: 8px;
    selection-background-color: #667eea;
    color: #2d3748;
    padding: 4px;
}

/* =========================== СПИНБОКСЫ =========================== */

StyledSpinBox, QSpinBox {
    background-color: #ffffff;
    color: #2d3748;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 14px;
    min-height: 20px;
}

StyledSpinBox:hover, QSpinBox:hover {
    border-color: #667eea;
    background-color: #f7fafc;
}

StyledSpinBox:focus, QSpinBox:focus {
    border: 2px solid #667eea;
    background-color: #f7fafc;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #edf2f7;
    border: none;
    width: 20px;
    border-radius: 4px;
    margin: 2px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #667eea;
}

QSpinBox::up-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 6px solid #4a5568;
    width: 0;
    height: 0;
}

QSpinBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #4a5568;
    width: 0;
    height: 0;
}

/* =========================== СПИСКИ =========================== */

ListWidget, QListWidget {
    background-color: #ffffff;
    color: #2d3748;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 8px;
    alternate-background-color: #f7fafc;
    selection-background-color: #667eea;
}

QListWidget::item {
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 2px 0;
    font-weight: 500;
}

QListWidget::item:hover {
    background-color: #3a3a3a;
    border-color: #667eea;
}

QListWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border-color: #667eea;
}

QListWidget::item::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #606060;
    border-radius: 4px;
    background-color: #2a2a2a;
    margin-right: 8px;
}

QListWidget::item::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    border-color: #667eea;
}

/* =========================== ЧЕКБОКСЫ =========================== */

CheckBox, QCheckBox {
    color: #e0e0e0;
    font-weight: 500;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #606060;
    border-radius: 6px;
    background-color: #2a2a2a;
}

QCheckBox::indicator:hover {
    border-color: #667eea;
    background-color: #2e2e2e;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    border-color: #667eea;
}

/* =========================== ПРОГРЕСС-БАР =========================== */

QProgressBar, QProgressBar#ProgressBar {
    background-color: #2a2a2a;
    border: 2px solid #404040;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 14px;
    color: #e0e0e0;
    padding: 2px;
    min-height: 20px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 10px;
    margin: 2px;
}

/* =========================== ВКЛАДКИ =========================== */

QTabWidget::pane {
    border: none;
    background-color: transparent;
    border-radius: 12px;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #3a3a3a, stop:1 #2a2a2a);
    color: #b0b0b0;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border: 2px solid #404040;
    border-bottom: none;
    font-weight: 600;
    min-width: 80px;
}

QTabBar::tab:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #4a4a4a, stop:1 #3a3a3a);
    color: #e0e0e0;
    border-color: #667eea;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border-color: #667eea;
    border-bottom: 2px solid #667eea;
}

/* =========================== ПРОКРУТКА =========================== */

QScrollArea {
    background-color: transparent;
    border: none;
    border-radius: 8px;
}

QScrollBar:vertical {
    background-color: #2a2a2a;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 6px;
    min-height: 30px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #5a67d8, stop:1 #6b46c1);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0;
}

QScrollBar:horizontal {
    background-color: #2a2a2a;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 6px;
    min-width: 30px;
    margin: 2px;
}

/* =========================== РАЗДЕЛИТЕЛИ =========================== */

QSplitter::handle {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #404040, stop:1 #606060);
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 6px;
}

QSplitter::handle:vertical {
    height: 6px;
}

QSplitter::handle:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
}

/* =========================== МЕНЮ И ДИАЛОГИ =========================== */

QMenu {
    background-color: #2a2a2a;
    border: 2px solid #667eea;
    border-radius: 8px;
    padding: 4px;
    color: #e0e0e0;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 4px;
    margin: 1px;
}

QMenu::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
}

QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 #1a1a1a, stop:1 #2d2d2d);
    color: #e0e0e0;
}

/* =========================== ГРУППЫ =========================== */

QGroupBox {
    color: #e0e0e0;
    border: 2px solid #404040;
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px 0 8px;
    color: #ffffff;
    background-color: #1a1a1a;
}
"""

def load_style(style_name):
    """Loads style by name using Styles class"""
    styles = Styles()
    return styles.get_style(style_name)