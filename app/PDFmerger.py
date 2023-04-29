import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QFileDialog, QPushButton, QListWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QIcon
from PyPDF2 import PdfMerger

basedir = os.path.dirname(__file__)

class PDFMerger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Merger')
        self.setAcceptDrops(True)
        self.setGeometry(100, 100, 500, 400)

        # Create a central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Create a label widget
        self.label = QLabel('Drag and drop PDF docs in the order you want them merged', self.central_widget)
        self.layout.addWidget(self.label)
        self.list_widget = QListWidget(self.central_widget)
        self.layout.addWidget(self.list_widget)

        # Create the clear button
        self.clear_button = QPushButton('Clear List', self.central_widget)
        self.clear_button.clicked.connect(self.clearList)
        self.layout.addWidget(self.clear_button)

        # Create the merge and save button
        self.save_button = QPushButton("Merge and Save As...", self.central_widget)
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button)

        # Set the layout on the central widget
        self.central_widget.setLayout(self.layout)

        # Set the central widget
        self.setCentralWidget(self.central_widget)

    def clearList(self):
        self.list_widget.clear()
        if(hasattr(self,"merger")):
            self.merger.close()
            self.merger = PdfMerger()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # Only accept PDF files
            for url in event.mimeData().urls():
                if not url.toString().lower().endswith('.pdf'):
                    event.ignore()
                    return
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        # Add the accepted PDF files to the list widget
        for url in event.mimeData().urls():
            if url.toString().lower().endswith('.pdf'):
                self.list_widget.addItem(url.fileName())
                if(hasattr(self,"merger")):
                    self.merger.append(url.toString()[8:])
                else:
                    self.merger = PdfMerger()
                    self.merger.append(url.toString()[8:])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() == Qt.LeftButton):
            return
        if ((event.pos() - self.drag_start_position).manhattanLength()
                < QApplication.startDragDistance()):
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        drag.setMimeData(mime_data)

    def display_file(self):
        self.file_label.setText(f"File: {self.file_path}")

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As...", "", "PDF files (*.pdf)", options=options)
        if file_name:
            with open(file_name + ".pdf", "wb") as f:
                self.merger.write(f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir,'icons\merge.ico')))
    viewer = PDFMerger()
    viewer.show()
    sys.exit(app.exec_())
