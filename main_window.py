from PyQt5.QtWidgets import QLabel,QMainWindow,QLineEdit,QPushButton \
    ,QFileDialog,QListWidget,QMessageBox,QTableWidget,QTableWidgetItem \
    ,QComboBox,QColorDialog,QCheckBox,QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap,QFontDatabase,QFont
from PyQt5.QtCore import Qt
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import os

class Form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(900,600)
        self.state = {'position':50}
        self.addedTxtBoxes = []
        self.fileNameAndAddress = []
        self.textbox = []
        self.font_path = ''

        # Background LBL
        background_lbl = QLabel(self)
        background_lbl.setFixedSize(900,600)
        background_lbl.setStyleSheet("background-image: url(img/background.jpg);" \
        "background-repeat: no-repeat;" \
        "background-position: center;")
        background_lbl.lower()

        #TitleBar
        titleBarlbl = QLabel(self)
        titleBarlbl.setStyleSheet("background-color:#001223;")
        titleBarlblOpacityEffect = QGraphicsOpacityEffect()
        titleBarlblOpacityEffect.setOpacity(0.8)
        titleBarlbl.setGraphicsEffect(titleBarlblOpacityEffect)
        titleBarlbl.setFixedSize(900,28)
        titleBarlbl.show()


        lblStyle = "QLabel#lbl{color:white;border:none;font:16px;}"

        tempPicturelbl = QLabel(self)
        tempPicturelbl.setText("Add Template")
        tempPicturelbl.setObjectName("lbl")
        tempPicturelbl.setStyleSheet(lblStyle)
        tempPicturelbl.move(734,91)

        minimizelbl = QLabel(self)
        minimizelbl.setText("\u005F")
        minimizelbl.move(851,2)
        minimizelbl.setStyleSheet("color: white")


        exitlbl = QLabel(self)
        exitlbl.setText("\u00D7")
        exitlbl.move(880,2)
        exitlbl.setStyleSheet("color: white")

        fontlbl = QLabel(self)
        fontlbl.setText("Font:")
        fontlbl.setObjectName("lbl")
        fontlbl.setStyleSheet(lblStyle)
        fontlbl.move(488,369)

        colorlbl = QLabel(self)
        colorlbl.setText("Color:")
        colorlbl.setObjectName("lbl")
        colorlbl.setStyleSheet(lblStyle)
        colorlbl.move(484,408)

        sizelbl = QLabel(self)
        sizelbl.setText("Size:")
        sizelbl.setObjectName("lbl")
        sizelbl.setStyleSheet(lblStyle)
        sizelbl.move(495,447)

        sizeTxtBox = QLineEdit(self)
        sizeTxtBox.setFixedSize(160,27)
        sizeTxtBox.move(304,443)
        sizeTxtBox.setStyleSheet("background-color: #003f74;color: white;border: none")



        #Style for all functional buttons in program
        btnStyle = "QPushButton#btn{background-color: #003f74;color:white;border:none;font:16px;}"


        #MessageBox
        self.message = QMessageBox(self)
        self.message.setText("that's it")
        self.message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        #directory Dialog
        dialog = QFileDialog(self)
        dialog.setNameFilter("Images (*.png *.jpg)")

        #button for adding to picture list
        addPicturebtn = QPushButton(self)
        addPicturebtn.setText("add picture")
        addPicturebtn.setFixedSize(300,27)
        addPicturebtn.setObjectName("btn")
        addPicturebtn.setStyleSheet(btnStyle)
        addPicturebtn.move(548,295)
        addPicturebtn.clicked.connect(self.open_file_dialog)

        #button for adding data to list
        addDatabtn = QPushButton(self)
        addDatabtn.setText("add data")
        addDatabtn.setFixedSize(300,27)
        addDatabtn.setObjectName("btn")
        addDatabtn.setStyleSheet(btnStyle)
        addDatabtn.move(548,509)



        #Add Text
        addbtn = QPushButton(self)
        addbtn.setText("Run")
        addbtn.setObjectName("btn")
        addbtn.setStyleSheet(btnStyle)
        addbtn.move(400,100)
        addbtn.clicked.connect(self.edit_files)

        #Add more textbox
        addMoreTextBoxbtn = QPushButton(self)
        addMoreTextBoxbtn.setText("+")
        addMoreTextBoxbtn.setObjectName("btn")
        addMoreTextBoxbtn.setStyleSheet(btnStyle)
        addMoreTextBoxbtn.move(400,150)
        addMoreTextBoxbtn.clicked.connect(self.addMoretxtBoxes)

        # Color Picker button
        self.colorPicketBtn = QPushButton("Color",self)
        self.colorPicketBtn.move(304,404)
        self.colorPicketBtn.setObjectName("btn")
        self.colorPicketBtn.setStyleSheet(btnStyle)
        self.colorPicketBtn.clicked.connect(self.openColorDialog)
        self.colorPicketBtn.setFixedSize(160,27)

        self.fontColor = (0,0,0)

        showBtn = QPushButton(self)
        showBtn.setText("Show")
        showBtn.setObjectName("btn")
        showBtn.setStyleSheet(btnStyle)
        showBtn.move(500,50)
        showBtn.clicked.connect(self.showmsg)

        #Preview the image
        self.previewlbl = QLabel(self)
        self.previewlbl.setText("Empty")
        self.previewlbl.setFixedSize(480,230)
        self.previewlbl.move(44,93)
        self.previewlbl.setStyleSheet("background-color: #003f74;" \
        "text-align: justify")
    

        
        #Style for all lists in program
        listStyle = "QListWidget#list{background-color: #003f74;color:white;border:none;font:16px;}"

        #list of selected files
        self.listOfSelectedFiles = QListWidget(self)
        self.listOfSelectedFiles.setFixedSize(301,143)
        self.listOfSelectedFiles.setObjectName("list")
        self.listOfSelectedFiles.setStyleSheet(listStyle)
        self.listOfSelectedFiles.move(548,137)
        self.listOfSelectedFiles.itemClicked.connect(self.on_item_clicked)
        
        #Style for all tables in program
        tableStyle = "QTableWidget#table{background-color: #003f74;color:white;border:none;font:16px;}"

        #Loaded data table
        self.listOfloadedData = QTableWidget(self)
        self.listOfloadedData.setFixedSize(300,143)
        self.listOfloadedData.setObjectName("table")
        self.listOfloadedData.setStyleSheet(tableStyle)
        self.listOfloadedData.move(548,352)
        self.listOfloadedData.show()

        #Load Fonts on system
        allFonts = QFontDatabase().families()

        #ComboOfLoadedFonts
        self.cmboFont = QComboBox(self)
        self.cmboFont.move(304,366)
        self.cmboFont.setFixedWidth(160)

        # self.cmboFont.addItems(allFonts) # add fonts to combobox
        for font in allFonts:
           self.cmboFont.addItem(font)
           # Make each item styled in its own font
           index = self.cmboFont.count() - 1
           self.cmboFont.setItemData(index, QFont(font), role=Qt.FontRole)

        self.cmboFont.currentTextChanged.connect(self.get_text)
        
        # Checkbox to Add pictures to a file
        enableAddPictureToTemplate = QCheckBox(self)
        enableAddPictureToTemplate.setText("enable to add pitures to Templae ")
        enableAddPictureToTemplate.move(0,0)
        enableAddPictureToTemplate.stateChanged.connect(self.checkToEnableAddToTemplate)

        # list for template Picture
        self.lblForTemplatePictures = QLabel(self)
        self.lblForTemplatePictures.setText("Null")
        self.lblForTemplatePictures.setFixedSize(182,24)
        self.lblForTemplatePictures.move(551,93)
        self.lblForTemplatePictures.setStyleSheet("background-color: #003f74;color: white;")
        self.lblForTemplatePictures.setDisabled(True)


        
    def checkToEnableAddToTemplate(self,checked):
        if checked:
            self.lblForTemplatePictures.setEnabled(True)
        else:
            self.lblForTemplatePictures.setDisabled(True)

    def get_text(self,fontname):
        from matplotlib import font_manager
        self.font_path = font_manager.findfont(fontname, fallback_to_default=False)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorPicketBtn.setStyleSheet(f"background-color: rgb{color.getRgb()[:3]};")
            self.fontColor = color.getRgb()[:3]

    def loadListOfNamesFile(self):
        file_path = "C:\\Users\\Reza\\Desktop\\sampleData.txt"
        file = open(file_path,'r')
        lines = file.readlines()
        return lines
    

    def showmsg(self):
        lines = self.loadListOfNamesFile() #Seperated the loading procces into another function for better clarity
        listOfHeaders = [] #this var will be used to store column name
        numberOfColumns = 0
        row = 0
        column = 0
        lookingForHeader = True #at first function tries to look for header name in first lines so it's True by default
        for line in lines:
            if lookingForHeader == True:
                if line == "--\n": # of you reached the end of header section
                    lookingForHeader = False
                    self.listOfloadedData.setColumnCount(column)
                    self.listOfloadedData.setHorizontalHeaderLabels(listOfHeaders)
                column += 1
                listOfHeaders.append(line)
            if lookingForHeader == False:
                self.listOfloadedData.setRowCount(row+1)
                if (line != "==\n") and (line != "--\n"):
                    if numberOfColumns < len(listOfHeaders):
                        self.listOfloadedData.setItem(row,numberOfColumns,QTableWidgetItem(line))
                        numberOfColumns += 1
                if line == "==\n":
                    row += 1
                    numberOfColumns = 0
        self.listOfloadedData.resizeRowsToContents()

   

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
                        pixmap = QPixmap(f"C:\\Users\\Reza\\Desktop\\temp\\thumbnail-{item.text()}")
                        self.previewlbl.setPixmap(pixmap)
                    finally: #if the thumbnail was not created,tries to create it
                        image = Image.open(address[1])
                        copy = image.copy()
                        max_size = (256,256)
                        image.thumbnail(max_size,Image.Resampling.LANCZOS)
                        image.save(f"C:\\Users\\Reza\\Desktop\\temp\\thumbnail-{item.text()}")
        

    
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
        listOfPositions = [[89,43],[97,105],[114,169],[296,44]] #position of text to draw
        numberOfTableRows = self.listOfloadedData.rowCount()
        numberOfTableColumns = self.listOfloadedData.columnCount()
        addressOfPicture = self.fileNameAndAddress[0][1] #load first line of addressbox
        for row in range(0,numberOfTableRows):
            img = Image.open(addressOfPicture)
            draw = ImageDraw.Draw(img)
            for column in range(0,numberOfTableColumns):
                cellData = self.listOfloadedData.item(row,column).text()
                x = listOfPositions[column][0]
                y = listOfPositions[column][1]
                draw.text((x,y),cellData,font=ImageFont.truetype(self.font_path,15),fill=self.fontColor,align="center")
            img.save((f"C:\\Users\\Reza\\Desktop\\result\\res{row}{column}-{self.fileNameAndAddress[0][0]}"))
                

        


            