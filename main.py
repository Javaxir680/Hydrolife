#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import (QApplication, QWidget,QHBoxLayout,QVBoxLayout,QListWidget,QPushButton,QLabel,QFileDialog)
from PyQt5.QtGui import QPixmap

from PIL import ImageFilter
from PIL import Image
import os
from PyQt5.QtCore import Qt

class ImageProcessor():
    def __init__(self): 
        self.image = None 
        self.dir = None # Папка которую мы открыли
        self.filename = None # Название фото из папки
        self.save_dir = 'Modified/' # Папка для измененных фото
    def loadImage(self,filename):
        self.filename = filename
        image_path = os.path.join(workdir,self.filename)
        self.image = Image.open(image_path)
    def showImage(self,path):
        image_label.hide()
        pixmapimage =  QPixmap(path)
        w,h = image_label.width(),image_label.height()
        pixmapimage = pixmapimage.scaled(w,
                    h,Qt.KeepAspectRatio)
        image_label.setPixmap(pixmapimage)
        image_label.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir,self.filename
        )
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir,self.filename
        )
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir,self.filename
        )
        self.showImage(image_path)
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir,self.filename
        )
        self.showImage(image_path)
workimage = ImageProcessor()

def showChosenImage():
    filename = list_image.currentItem().text()
    workimage.loadImage(filename)
    image_path = os.path.join(workdir,filename)
    workimage.showImage(image_path)


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('EASY EDITOR')

main_layout = QHBoxLayout()
row_tools = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

btn_dir = QPushButton('Папка')
list_image = QListWidget()
image_label = QLabel('Картинка')

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton('Ч/Б')

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col1.addWidget(btn_dir)
col1.addWidget(list_image)

col2.addWidget(image_label)
col2.addLayout(row_tools)

main_layout.addLayout(col1,20)
main_layout.addLayout(col2,80)

main_win.setLayout(main_layout)

extensions = ['.jpg','.png','.jpeg']
def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
import os
def showFilenameList():
    extensions = ['.jpg','.bmp','.png','.jpeg','.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    list_image.clear()
    list_image.addItems(filenames)
btn_dir.clicked.connect(showFilenameList)
main_win.resize(700,400)

btn_sharp.clicked.connect(workimage.do_sharp)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_bw.clicked.connect(workimage.do_bw)

list_image.currentRowChanged.connect(showChosenImage)

main_win.show()
app.exec_()
