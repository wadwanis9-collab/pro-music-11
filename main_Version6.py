import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QFileDialog, QLineEdit, QInputDialog, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap
from player import Player
from file_manager import FileManager
from image_manager import ImageManager
from themes import THEMES

class Pro2App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro 2 - Music & Video Player")
        self.setGeometry(100, 100, 900, 600)
        self.player = Player()
        self.file_manager = FileManager()
        self.image_manager = ImageManager()
        self.current_theme = "فاتح"
        self.initUI()
        self.apply_theme(self.current_theme)
    
    def initUI(self):
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(20, 20, 400, 400)
        
        self.playButton = QPushButton("تشغيل", self)
        self.playButton.setGeometry(440, 20, 120, 40)
        self.playButton.clicked.connect(self.play_selected)
        
        self.renameButton = QPushButton("تعديل الاسم", self)
        self.renameButton.setGeometry(440, 70, 120, 40)
        self.renameButton.clicked.connect(self.rename_selected)
        
        self.addImageButton = QPushButton("إدراج صورة", self)
        self.addImageButton.setGeometry(440, 120, 120, 40)
        self.addImageButton.clicked.connect(self.add_image_selected)
        
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(600, 20, 256, 256)
        self.imageLabel.setScaledContents(True)
        
        self.loadFilesButton = QPushButton("إضافة ملفات", self)
        self.loadFilesButton.setGeometry(20, 430, 120, 40)
        self.loadFilesButton.clicked.connect(self.load_files)
        
        # قائمة اختيار الثيم
        self.themeCombo = QComboBox(self)
        self.themeCombo.setGeometry(440, 180, 120, 40)
        self.themeCombo.addItems(THEMES.keys())
        self.themeCombo.currentTextChanged.connect(self.change_theme)
        self.themeCombo.setToolTip("اختر شكل الواجهة")
    
    def apply_theme(self, theme_name):
        theme = THEMES.get(theme_name, THEMES["فاتح"])
        self.setStyleSheet(f"background-color: {theme['background']}; color: {theme['foreground']};")
        self.listWidget.setStyleSheet(f"background-color: {theme['button']}; color: {theme['foreground']};")
        self.playButton.setStyleSheet(f"background-color: {theme['button']}; color: {theme['foreground']};")
        self.renameButton.setStyleSheet(f"background-color: {theme['button']}; color: {theme['foreground']};")
        self.addImageButton.setStyleSheet(f"background-color: {theme['button']}; color: {theme['foreground']};")
        self.loadFilesButton.setStyleSheet(f"background-color: {theme['button']}; color: {theme['foreground']};")
        self.themeCombo.setStyleSheet(f"background-color: {theme['button']}; color: {theme['foreground']};")
        self.imageLabel.setStyleSheet(f"border: 2px solid {theme['highlight']};")
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme(theme_name)
    
    def load_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "اختر ملفات موسيقى أو فيديو", "", "Audio/Video Files (*.mp3 *.wav *.mp4 *.avi)")
        if files:
            self.listWidget.addItems(files)
    
    def play_selected(self):
        selected = self.listWidget.currentItem()
        if selected:
            file_path = selected.text()
            self.player.play(file_path)
    
    def rename_selected(self):
        selected = self.listWidget.currentItem()
        if selected:
            old_path = selected.text()
            new_name, ok = QInputDialog.getText(self, "تعديل الاسم", "ادخل الاسم الجديد:")
            if ok and new_name:
                result = self.file_manager.rename_file(old_path, new_name)
                if result:
                    selected.setText(result)
    
    def add_image_selected(self):
        selected = self.listWidget.currentItem()
        if selected:
            file_path = selected.text()
            image_path, _ = QFileDialog.getOpenFileName(self, "اختر صورة", "", "Image Files (*.jpg *.png)")
            if image_path:
                success = self.image_manager.add_image(file_path, image_path)
                if success:
                    self.imageLabel.setPixmap(QPixmap(image_path))
                else:
                    QMessageBox.warning(self, "خطأ", "تعذر إدراج الصورة. الملف ليس MP3.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Pro2App()
    window.show()
    sys.exit(app.exec_())