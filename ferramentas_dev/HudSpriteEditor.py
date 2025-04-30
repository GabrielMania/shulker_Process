import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.uic import loadUi

class HudSpriteEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('HudSpriteEditor.ui', self)

        # Connect buttons to their respective methods
        self.saveButton.clicked.connect(self.save_drawing)
        self.loadButton.clicked.connect(self.load_drawing)
        self.importButton.clicked.connect(self.import_data)
        self.exportButton.clicked.connect(self.export_data)

        # Placeholder for drawing content
        self.drawing_pixmap = QPixmap(self.areaDesenho.size())
        self.drawing_pixmap.fill()  # Fill with default background color

    def paintEvent(self, event):
        """Render the drawing area."""
        painter = QPainter(self)
        painter.drawPixmap(self.areaDesenho.geometry(), self.drawing_pixmap)

    def save_drawing(self):
        """Save the current drawing state to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Drawing', '', 'PNG Files (*.png);;All Files (*)')
        if file_path:
            self.drawing_pixmap.save(file_path)

    def load_drawing(self):
        """Load a previously saved drawing state from a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Drawing', '', 'PNG Files (*.png);;All Files (*)')
        if file_path:
            self.drawing_pixmap.load(file_path)
            self.update()

    def import_data(self):
        """Import data/image into the drawing area."""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import Data', '', 'Image Files (*.png *.jpg *.bmp);;All Files (*)')
        if file_path:
            imported_pixmap = QPixmap(file_path)
            painter = QPainter(self.drawing_pixmap)
            painter.drawPixmap(0, 0, imported_pixmap)
            self.update()

    def export_data(self):
        """Export the drawing area contents to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, 'Export Drawing', '', 'PNG Files (*.png);;All Files (*)')
        if file_path:
            self.drawing_pixmap.save(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HudSpriteEditor()
    window.show()
    sys.exit(app.exec_())