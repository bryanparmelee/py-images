import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QErrorMessage, QMessageBox
from PyQt5.QtCore import Qt
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
        self.resize(600, 600)
        self.setWindowTitle("Auto Resizer")
        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('Resize photos', self)
        self.btn.setGeometry(200, 500, 200, 50)
        self.btn.clicked.connect(self.resize_auto)

        self.error_dialog = QErrorMessage()
        self.message_box = QMessageBox()

    def resize_auto(self):
        
        for i in range(self.listbox_view.count()):
            desired_size = 1024
            url = self.listbox_view.item(i).text()

            try:
                self.save_image(url, desired_size)
            except FileNotFoundError:
                self.error_dialog.showMessage("File not found.")
            except UnidentifiedImageError:
                self.error_dialog.showMessage("File '" + os.path.basename(url) + "' is an unsupported file type.")
            except ValueError:
                self.error_dialog.showMessage("Value error.")
            except TypeError:
                self.error_dialog.showMessage("Type error.")
               
        self.message_box.information(None, "information", "Operation complete.")    
        self.listbox_view.clear()

    def save_image(self, url, desired_size):
            path = os.path.split(os.path.abspath(url))[0] + '/'
            name = os.path.splitext(os.path.basename(url))[0]
            img = Image.open(url)
            original_width, original_height = img.size

            if max(original_width, original_height) <= desired_size:
                try: 
                    img.save(path + name + '-web.jpg')    
                except ValueError:
                    self.error_dialog.showMessage("Output format could not be determined.")
                except OSError:
                    self.error_dialog.showMessage("File could not be written.")                
            elif original_height >= original_width:
                ratio = original_width / float(original_height)
                new_width = int(desired_size * ratio)
                resized = img.resize((new_width, desired_size))
                try:
                    resized.save(path + name + '-web.jpg')             
                except ValueError:
                    self.error_dialog.showMessage("Output format could not be determined.")
                except OSError:
                    self.error_dialog.showMessage("File could not be written.")
            else:   
                ratio = original_height / float(original_width)    
                new_height = int(desired_size * ratio)
                resized = img.resize((desired_size, new_height))
                try: 
                    resized.save(path + name + '-web.jpg')                          
                except ValueError:
                    self.error_dialog.showMessage("Output format could not be determined.")
                except OSError:
                    self.error_dialog.showMessage("File could not be written.")
 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AutoResizer()
    demo.show()

    sys.exit(app.exec_())