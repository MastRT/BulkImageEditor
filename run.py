from PyQt5.QtWidgets import QApplication,QMainWindow
import sys
from main_window import Form

app = QApplication(sys.argv)

window = Form()
window.show()
app.exec_()