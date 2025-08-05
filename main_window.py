from PyQt5.QtWidgets import QLabel,QMainWindow,QLineEdit,QPushButton,QFileDialog
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from tkinter import filedialog

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
            
    def edit_files(self):
        for x in self.listofFiles:
            img = Image.open(x)
            draw = ImageDraw.Draw(img)
            draw.text(((img.width/2),(img.height/2)),self.textToAddtxtbox.text(),font=ImageFont.truetype("arial.ttf",60),fill=(255,0,0),align="center")
            print("not yet")
            img.save(f"C:\\Users\\Reza\\Desktop\\gs.png")
            print("saved")

            