import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PIL import Image 

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()

class AutoResizer(QMainWindow):

    def __init__(self):        
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle("Auto Resizer")
        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('Get Value', self)
        self.btn.setGeometry(850, 400, 200, 50)
        self.btn.clicked.connect(lambda: print(self.getSelectedItem()))

    def getSelectedItem(self):
        item = QListWidgetItem(self.listbox_view.currentItem())
        return item.text()

    def resize_auto(image_path, desired_size = 1024):

        image_path = './sloth2.jpg'

        try: 
            img = Image.open(image_path)
            original_width, original_height = img.size
            ratio = 0
            if max(original_width, original_height) <= desired_size:
                # return img
                print('I aint done shit')
            
            elif original_height >= original_width:
                ratio += original_width / float(original_height)
                new_width = int(desired_size * ratio)
                resized = img.resize((new_width, desired_size))
                w, h = resized.size
                print(w, h)
            else:   
                ratio += original_height / float(original_width)
                new_height = int(desired_size * ratio)
                resized = img.resize((desired_size, new_height))
                w, h = resized.size
                print(w, h)
        except TypeError:
            print(TypeError)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AutoResizer()
    demo.show()

    sys.exit(app.exec_())