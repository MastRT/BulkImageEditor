from PyQt5.QtWidgets import QLabel,QMainWindow,QLineEdit,QPushButton,QFileDialog,QListWidget
from PyQt5.QtGui import QPixmap
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path

class Form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(500,500)

        #label
        inputlbl = QLabel(self)
        inputlbl.setText("text to add to picture:")
        inputlbl.move(50,50)

        #inputs
        self.textToAddtxtbox = QLineEdit(self)
        self.textToAddtxtbox.move(200,50)

        #directory Dialog
        dialog = QFileDialog(self)
        dialog.setNameFilter("Images (*.png *.jpg)")

        #Open button
        openbtn = QPushButton(self)
        openbtn.setText("Open")
        openbtn.move(400,50)
        openbtn.clicked.connect(self.open_file_dialog)

        #Add Text
        addbtn = QPushButton(self)
        addbtn.setText("add file")
        addbtn.move(400,100)
        addbtn.clicked.connect(self.edit_files)

        #Preview the image
        preview = QLabel(self)

        #list of selected files
        self.listOfSelectedFiles = QListWidget(self)
        self.listOfSelectedFiles.setFixedSize(200,100)
        self.listOfSelectedFiles.move(50,200)
        self.listOfSelectedFiles.itemClicked.connect(str(preview.setText(self.listOfSelectedFiles.currentItem().text())))
        

        
        
        
    def preview(self):
        print(self.listOfSelectedFiles.currentItem().text())
        #pixmap = QPixmap(preview)

    
    def open_file_dialog(self):
        self.listofFiles = []
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "D://",
            "Images (*.png *.jpg)"
        )
        if filenames:
            self.listofFiles.extend([str(Path(filename))
                                     for filename in filenames])
        self.listOfSelectedFiles.addItems(self.listofFiles)
            
    def edit_files(self):
        for x in self.listofFiles:
            img = Image.open(x)
            draw = ImageDraw.Draw(img)
            draw.text((300,69),self.textToAddtxtbox.text(),font=ImageFont.truetype("arial.ttf",60),fill=(255,0,0),align="center")
            print("not yet")
            img.save(f"C:\\Users\\Reza\\Desktop\\gs.png")
            print("saved")

            