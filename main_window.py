from PyQt5.QtWidgets import QLabel,QMainWindow,QLineEdit,QPushButton \
    ,QFileDialog,QListWidget,QMessageBox,QTableWidget,QTableWidgetItem \
    ,QComboBox,QColorDialog,QCheckBox,QGraphicsOpacityEffect,QVBoxLayout \
    ,QHBoxLayout,QWidget
from PyQt5.QtGui import QPixmap,QFontDatabase,QFont
from PyQt5.QtCore import Qt,QPoint
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from ruler import ImageView,Ruler
import os
import sys


class ExitSystem(QLabel):
    
    def __init__(self,parent=None):
        super(ExitSystem,self).__init__(parent)

    def enterEvent(self, QEvent):
        self.setStyleSheet("background-color: #05131f;" \
        "color: white")
        pass

    def leaveEvent(self, QEvent):
        self.setStyleSheet("color: white")
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            sys.exit()

class Minimize(QLabel):
    
    def __init__(self,parent=None):
        super(Minimize,self).__init__(parent)

    def enterEvent(self, QEvent):
        self.setStyleSheet("background-color: #05131f;" \
        "color: white")
        pass
    
    def leaveEvent(self, QEvent):
        self.setStyleSheet("color: white")
        pass
        


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
        titleBarlbl.setFixedSize(900,24)
        titleBarlbl.move(0,0)
        titleBarlbl.setText("    Image Editor")
        titleBarlbl.mousePressEvent = self.PressEvent
        titleBarlbl.mouseMoveEvent = self.MoveEvent
        titleBarlbl.show()


        lblStyle = "QLabel#lbl{color:white;border:none;font:16px;font-family: B Koodak;}" \
        "QLabel#addressBar{background-color: #003f74}"

        tempPicturelbl = QLabel(self)
        tempPicturelbl.setText("تصویر الگو ")
        tempPicturelbl.setObjectName("lbl")
        tempPicturelbl.setStyleSheet(lblStyle)
        tempPicturelbl.move(734,91)

        minimizelbl = Minimize(self)
        minimizelbl.setText("\u005F")
        minimizelbl.installEventFilter(self)
        minimizelbl.setFixedSize(30,24)
        minimizelbl.setAlignment(Qt.AlignCenter)
        minimizelbl.move(840,0)
        minimizelbl.setStyleSheet("color: white")
        minimizelbl.mousePressEvent = self.minimumState

        exitlbl = ExitSystem(self)
        exitlbl.setText("\u00D7")
        exitlbl.move(870,0)
        exitlbl.setFixedSize(30,24)
        exitlbl.setAlignment(Qt.AlignCenter)
        exitlbl.setStyleSheet("color: white;")

        self.saveLocationlbl = QLabel(self)
        self.saveLocationlbl.setObjectName("addressBar")
        self.saveLocationlbl.setStyleSheet(lblStyle)
        self.saveLocationlbl.move(44,369)
        self.saveLocationlbl.setFixedSize(230,24)


        fontlbl = QLabel(self)
        fontlbl.setText("فونت")
        fontlbl.move(488,369)
        fontlbl.setFixedSize(30,28)
        fontlbl.setObjectName("lbl")
        fontlbl.setStyleSheet(lblStyle)
        

        colorlbl = QLabel(self)
        colorlbl.setText("رنگ")
        colorlbl.move(484,408)
        colorlbl.setFixedSize(30,28)
        colorlbl.setObjectName("lbl")
        colorlbl.setStyleSheet(lblStyle)

        sizelbl = QLabel(self)
        sizelbl.setText("اندازه")
        sizelbl.move(495,447)
        sizelbl.setFixedSize(30,28)
        sizelbl.setObjectName("lbl")
        sizelbl.setStyleSheet(lblStyle)

        sizeTxtBox = QLineEdit(self)
        sizeTxtBox.setFixedSize(160,27)
        sizeTxtBox.move(304,443)
        sizeTxtBox.setStyleSheet("background-color: #003f74;color: white;border: none")



        #Style for all functional buttons in program
        btnStyle = "QPushButton#btn{background-color: #003f74;color:white;border:none;font:16px;font-family: B Koodak;}"
        
        #directory Dialog
        dialog = QFileDialog(self)
        dialog.setNameFilter("Images (*.png *.jpg)")

        #button for adding to picture list
        addPicturebtn = QPushButton(self)
        addPicturebtn.setText("اضافه کردن تصویر")
        addPicturebtn.setFixedSize(300,27)
        addPicturebtn.setObjectName("btn")
        addPicturebtn.setStyleSheet(btnStyle)
        addPicturebtn.move(548,295)
        addPicturebtn.clicked.connect(self.open_file_dialog)

        #button for adding data to list
        addDatabtn = QPushButton(self)
        addDatabtn.setText("اضافه کردن اطلاعات")
        addDatabtn.setFixedSize(300,27)
        addDatabtn.setObjectName("btn")
        addDatabtn.setStyleSheet(btnStyle)
        addDatabtn.move(548,509)
        addDatabtn.clicked.connect(self.loadData)


        #Choose Save Location Button
        saveLocationbtn = QPushButton(self)
        saveLocationbtn.setText("انتخاب محل ذخیره")
        saveLocationbtn.setFixedSize(230,24)
        saveLocationbtn.move(44,408)
        saveLocationbtn.setObjectName("btn")
        saveLocationbtn.setStyleSheet(btnStyle)
        saveLocationbtn.clicked.connect(self.saveLocation)
        
        #Add Text
        addbtn = QPushButton(self)
        addbtn.setText("ذخیره")
        addbtn.setObjectName("btn")
        addbtn.setStyleSheet(btnStyle)
        addbtn.move(100,500)
        addbtn.clicked.connect(self.edit_files)

        #Add more textbox
        addMoreTextBoxbtn = QPushButton(self)
        addMoreTextBoxbtn.setText("+")
        addMoreTextBoxbtn.setObjectName("btn")
        addMoreTextBoxbtn.setStyleSheet(btnStyle)
        addMoreTextBoxbtn.move(100,450)
        addMoreTextBoxbtn.clicked.connect(self.addMoretxtBoxes)

        # Color Picker button
        self.colorPicketBtn = QPushButton("Color",self)
        self.colorPicketBtn.move(304,404)
        self.colorPicketBtn.setObjectName("btn")
        self.colorPicketBtn.setStyleSheet(btnStyle)
        self.colorPicketBtn.clicked.connect(self.openColorDialog)
        self.colorPicketBtn.setFixedSize(160,27)

        self.fontColor = (0,0,0)

        #Preview the image
        self.previewlbl = QLabel(self)
        self.previewlbl.setText("Empty")
        self.previewlbl.setAlignment(Qt.AlignCenter)
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
        self.cmboFont.setStyleSheet("background-color: #003f74 ;color: white;")

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


        centeral = QWidget(self)
        self.setCentralWidget(centeral)

        templateAddressWindow = QWidget(centeral)
        templateAddressWindow.move(551,93)
        templateAddressWindow.setFixedSize(182,24)
        templateAddressWindow.setStyleSheet("background-color: white")

        # list for template Picture
        self.lblForTemplatePictures = QLabel(templateAddressWindow)
        self.lblForTemplatePictures.setText("Null")
        # self.lblForTemplatePictures.setFixedSize(182,24)
        # self.lblForTemplatePictures.move(551,93)
        self.lblForTemplatePictures.setStyleSheet("background-color: #003f74;color: white;")
        self.lblForTemplatePictures.setDisabled(True)

        openTemplateAddressBar = QLabel(templateAddressWindow)
        openTemplateAddressBar.setText("...")

        templateAddressHolder = QHBoxLayout()
        templateAddressHolder.setContentsMargins(0,0,0,0)
        templateAddressHolder.addWidget(self.lblForTemplatePictures)
        templateAddressHolder.addWidget(openTemplateAddressBar)


        templateAddressWindow.setLayout(templateAddressHolder)
        

        

    def PressEvent(self, event):
        self.oldPos = event.globalPos()

    def MoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


        
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
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Files",
            "D://",
            "Txt (*.txt)"
        )
        file_path = filename
        if file_path:
            file = open(file_path,'r')
            lines = file.readlines()
            return lines
    

    def loadData(self):
        lines = self.loadListOfNamesFile() #Seperated the loading procces into another function for better clarity
        if lines:
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
        file = ""
        for address in self.fileNameAndAddress: # looking to find the location of corespondong selected image
            # if item.text() != "":
                if item.text() == address[0]:   #check if the file names are Same
                    try: #Try opening the thumbnail if it was created before
                        pixmap = QPixmap(f"C:\\Users\\Reza\\Desktop\\temp\\thumbnail-{item.text()}")
                        file = pixmap
                        self.previewlbl.setPixmap(pixmap)
                    finally: #if the thumbnail was not created,tries to create it
                        image = Image.open(address[1])
                        copy = image.copy()
                        max_size = (256,256)
                        image.thumbnail(max_size,Image.Resampling.LANCZOS)
                        image.save(f"C:\\Users\\Reza\\Desktop\\temp\\thumbnail-{item.text()}")
        
        imageView = ImageView()
        imageView.loadImage(file)
        # Rulers
        topRuler = Ruler(Qt.Horizontal)
        leftRuler = Ruler(Qt.Vertical)

        layout = QVBoxLayout()
        layout.addWidget(topRuler)
        hLayout = QHBoxLayout()
        hLayout.addWidget(leftRuler)
        hLayout.addWidget(self.imageView)
        layout.addLayout(hLayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        

    
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
        try:
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
        except:
            message = QMessageBox(self)
            message.setIcon(QMessageBox.Critical)
            message.setWindowTitle("خطا")
            message.setText("محل ذخیره انتخاب نشده است")
            message.setStandardButtons(QMessageBox.Close)
            message.exec()
                
    def minimumState(self,event):
        self.showMinimized()

    def saveLocation(self):
        location = QFileDialog.getExistingDirectory(self,"select directory")
        self.saveLocationlbl.setText(location)

        


            