import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QErrorMessage, QMessageBox, QProgressBar, QPushButton, QSpinBox, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QUrl
from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener

# Add HEIC support
register_heif_opener()

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def resizePhoto(self):
        desired_size = demo.spinbox.value()
        item_count = demo.listbox_view.count()

        for i in range(item_count):
            percentage = int(100 / item_count)         
            url = demo.listbox_view.item(i).text()

            try:
                self.save_image(url, desired_size)
            except FileNotFoundError:
                self.error.emit("File not found.")      
            except UnidentifiedImageError:
                self.error.emit("File '" + os.path.basename(url) + "' is an unsupported file type.")
            except ValueError:
                self.error.emit("Value error.")
            except TypeError:
                self.error.emit("Type error.")
            self.progress.emit((i + 1) * percentage)

        self.finished.emit()

    def save_image(self, url, desired_size):
        path = os.path.split(os.path.abspath(url))[0] + '/'
        name = os.path.splitext(os.path.basename(url))[0]
        img = Image.open(url)
        original_width, original_height = img.size

        if max(original_width, original_height) <= desired_size:
            try: 
                img.save(path + name + '-web.jpg')    
            except ValueError:
                self.error.emit("Output format could not be determined.")
            except OSError:
                self.error.emit("File could not be written.")                
        elif original_height >= original_width:
            ratio = original_width / float(original_height)
            new_width = int(desired_size * ratio)
            resized = img.resize((new_width, desired_size))
            try:
                resized.save(path + name + '-web.jpg')             
            except ValueError:
                self.error.emit("Output format could not be determined.")
            except OSError:
                self.error.emit("File could not be written.")
        else:   
            ratio = original_height / float(original_width)    
            new_height = int(desired_size * ratio)
            resized = img.resize((desired_size, new_height))
            try: 
                resized.save(path + name + '-web.jpg')                          
            except ValueError:
                self.error.emit("Output format could not be determined.")
            except OSError:
                self.error.emit("File could not be written.")                      

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
        self.setWindowTitle("Image Resizer")
        self.listbox_view = ListBoxWidget(self)
        self.setStyleSheet('''
            ListBoxWidget {                         
                background-image: url(./dnd.png);                            
                                        }
            QProgressBar {
                text-align: right;
                margin-right: 40px;                    
                           }
                                        ''')
        
        self.spinbox = QSpinBox(self)
        self.spinbox.setMinimum(80)
        self.spinbox.setMaximum(5000)
        self.spinbox.setValue(1024)
        self.spinbox.setGeometry(210, 450, 180, 30) 

        self.size_label = QLabel("Desired size:", self)  
        self.size_label.setGeometry(260, 430, 200, 20)    

        self.btn = QPushButton('Resize', self)
        self.btn.setGeometry(200, 480, 200, 50)
        self.btn.clicked.connect(self.resize_auto)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(205, 535, 230, 25)   
        self.progress_bar.format()
        self.progress_bar.hide()       

    def resize_auto(self):
        self.thread = QThread(parent=self)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.progress_bar.show)
        self.thread.started.connect(self.worker.resizePhoto)          
        self.worker.progress.connect(self.reportProgress)
        self.worker.error.connect(self.handleError)
        self.thread.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)   
        self.worker.finished.connect(self.resetAll)  
        
        self.thread.start()      
      
    def reportProgress(self, value):
        self.progress_bar.setValue(value)

    def showMessage(self):
        QMessageBox.information(self, "Information", "Operation complete")

    def handleError(self, error):   
        self.error_dialog = QErrorMessage() 
        self.error_dialog.showMessage(error)

    def resetAll(self):    
        self.listbox_view.clear()
        self.progress_bar.reset()
        self.progress_bar.hide()
        self.showMessage()
          
if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AutoResizer()
    demo.show()

    sys.exit(app.exec_())