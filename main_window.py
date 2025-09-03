from PyQt5.QtWidgets import QLabel,QMainWindow,QLineEdit,QPushButton,QFileDialog,QListWidget,QMessageBox,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PIL import Image,ImageDraw,ImageFont,ImageQt
from pathlib import Path
import os

class Form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(700,700)
        self.state = {'position':50}
        self.addedTxtBoxes = []
        self.fileNameAndAddress = []
        self.textbox = []
        
        #label
        inputlbl = QLabel(self)
        inputlbl.setText("text to add to picture:")
        inputlbl.move(50,50)

        #MessageBox
        self.message = QMessageBox(self)
        self.message.setText("that's it")
        self.message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        

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

        #Add more textbox
        addMoreTextBoxbtn = QPushButton(self)
        addMoreTextBoxbtn.setText("+")
        addMoreTextBoxbtn.move(400,150)
        addMoreTextBoxbtn.clicked.connect(self.addMoretxtBoxes)

        #Preview the image
        self.previewlbl = QLabel(self)
        self.previewlbl.setText("Empty")
        self.previewlbl.move(300,200)
        self.previewlbl.setFixedSize(300,300)
        self.previewlbl.setStyleSheet("border: 2px solid black;" \
        "text-align: justify")
    

        #list of selected files
        self.listOfSelectedFiles = QListWidget(self)
        self.listOfSelectedFiles.setFixedSize(200,100)
        self.listOfSelectedFiles.move(50,200)
        self.listOfSelectedFiles.itemClicked.connect(self.on_item_clicked)
########### buggy ---------------------- >
        #list of loaded data
        self.listOfloadedData = QTableWidget(self)
        self.listOfloadedData.setFixedSize(200,300)
        self.listOfloadedData.move(50,350)
        #self.listOfloadedData.setHorizontalHeaderLabels(columns)
        #self.listOfloadedData.setItem(0,0,QTableWidgetItem("test"))
        self.listOfloadedData.show()

        showBtn = QPushButton(self)
        showBtn.setText("Show")
        showBtn.move(500,50)
        showBtn.clicked.connect(self.showmsg)

    def loadListOfNamesFile(self):
        file_path = "C:\\Users\\Reza\\Desktop\\sampleData.txt"
        file = open(file_path,'r')
        lines = file.readlines()
        return lines
    

    def showmsg(self):
        lines = self.loadListOfNamesFile()
        listOfHeaders = []
        numberOfColumns = 0
        row = 1
        column = 0
        lookingForHeader = True
        for line in lines:
            if lookingForHeader == True:
                if line == "--\n":
                    lookingForHeader = False
                    self.listOfloadedData.setColumnCount(column)
                    self.listOfloadedData.setHorizontalHeaderLabels(listOfHeaders)
                column += 1
                listOfHeaders.append(line)
            if lookingForHeader == False:
                self.listOfloadedData.setRowCount(2)
                if (line != "==\n") and (line != "--\n"):
                    if numberOfColumns < len(listOfHeaders):
                        self.listOfloadedData.setItem(row,numberOfColumns,QTableWidgetItem(line))
                        numberOfColumns += 1
                if line == "==\n":
                    row += 1
                    numberOfColumns = 0
            
        
                
########### buggy <-----------------------
   

    def addMoretxtBoxes(self):
        box = QLineEdit(self)
        self.state['position'] += 50
        box.move(200,self.state['position'])
        self.addedTxtBoxes.append(box) # add new text boxes to program to an array for foloowing it
        box.show()
        

        
    
    def on_item_clicked(self,item):
        for address in self.fileNameAndAddress: # looking to find the location of corespondong selected image
            # if item.text() != "":
                if item.text() == address[0]:   #check if the file names are Same
                    try: #Try opening the thumbnail if it was created before
                        pixmap = QPixmap(f"C:\\Users\\Reza\\Desktop\\temp\\{item.text()}")
                        self.previewlbl.setPixmap(pixmap)
                    finally: #if the thumbnail was not created,tries to create it
                        image = Image.open(address[1])
                        copy = image.copy()
                        max_size = (256,256)
                        image.thumbnail(max_size,Image.Resampling.LANCZOS)
                        image.save(f"C:\\Users\\Reza\\Desktop\\temp\\{item.text()}")
        

    
    def open_file_dialog(self):
        self.listofFilesAddress = []
        # nameAndAddressTuple = tuple()
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "D://",
            "Images (*.png *.jpg)"
        )
        if filenames:
            self.listofFilesAddress.extend([str(Path(filename))
                                     for filename in filenames])
        for filename in self.listofFilesAddress:
            nameAndAddressTuple = (os.path.basename(filename),filename)
            self.fileNameAndAddress.append(nameAndAddressTuple)
            self.listOfSelectedFiles.addItem(os.path.basename(filename))
            

    def edit_files(self):
        for x in self.fileNameAndAddress:
            img = Image.open(x[1])
            draw = ImageDraw.Draw(img)
            draw.text((300,69),self.textToAddtxtbox.text(),font=ImageFont.truetype("arial.ttf",60),fill=(255,0,0),align="center")
            img.save(f"C:\\Users\\Reza\\Desktop\\result\\{x[0]}")

            