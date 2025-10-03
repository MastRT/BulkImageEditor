from PyQt5.QtWidgets import QWidget,QGraphicsScene,QGraphicsView,QGraphicsPixmapItem
from PyQt5.QtGui import QPainter,QColor,QPixmap,QPen
from PyQt5.QtCore import Qt,QPoint

class Ruler(QWidget):
    def __init__(self,orientation=Qt.Horizontal,parent=None):
        super(Ruler,self).__init__(parent)
        self.orientation = orientation
        self.setFixedHeight(20) if orientation == Qt.Horizontal else self.setFixedWidth(20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(240, 240, 240))  # light gray bg
        painter.setPen(Qt.black)

        step = 50  # pixels per tick
        length = self.width() if self.orientation == Qt.Horizontal else self.height()

        for i in range(0, length, step):
            if self.orientation == Qt.Horizontal:
                painter.drawLine(i, 0, i, 10)
                painter.drawText(i+2, 18, str(i))
            else:
                painter.drawLine(0, i, 10, i)
                painter.drawText(2, i+10, str(i))

class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.guides = []

    def loadImage(self, path):
        pixmap = QPixmap(path)
        self.scene.clear()
        self.imageItem = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.imageItem)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.pos())
            # Add a guide line
            self.guides.append(pos)
            self.update()
        super().mousePressEvent(event)

    def drawForeground(self, painter, rect):
        pen = QPen(Qt.red, 1, Qt.DashLine)
        painter.setPen(pen)
        for pos in self.guides:
            painter.drawLine(QPoint(int(pos.x()), 0), QPoint(int(pos.x()), self.height()))
            painter.drawLine(QPoint(0, int(pos.y())), QPoint(self.width(), int(pos.y())))
