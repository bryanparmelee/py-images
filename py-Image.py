import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QErrorMessage
from PyQt5.QtCore import Qt, QUrl
from PIL import Image, UnidentifiedImageError

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
        self.btn.clicked.connect(self.resize_auto)

        self.error_dialog = QErrorMessage()

    def resize_auto(self):
        desired_size = 1024
        image_path = QListWidgetItem(self.listbox_view.currentItem()).text()
        filepath = os.path.split(os.path.abspath(image_path))[0] + '/'
        filename = os.path.splitext(os.path.basename(image_path))[0]
        
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
                try:
                    resized.save(filepath + filename + '-web.jpg')
                except ValueError:
                    self.error_dialog.showMessage("Output format could not be determined.")
                except OSError:
                    self.error_dialog.showMessage("File could not be written.")
            else:   
                ratio += original_height / float(original_width)    
                new_height = int(desired_size * ratio)
                resized = img.resize((desired_size, new_height))
                try: 
                    resized.save(filepath + filename + '-web.jpg')
                except ValueError:
                    self.error_dialog.showMessage("Output format could not be determined.")
                except OSError:
                    self.error_dialog.showMessage("File could not be written.")
        except FileNotFoundError:
            self.error_dialog.showMessage("File not found.")
        except UnidentifiedImageError:
            self.error_dialog.showMessage("Unsupported file type.")
        except ValueError:
            self.error_dialog.showMessage("Value error.")
        except TypeError:
            self.error_dialog.showMessage("Type error.")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AutoResizer()
    demo.show()

    sys.exit(app.exec_())