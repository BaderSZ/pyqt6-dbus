# This Python file uses the following encoding: utf-8

import sys

from PySide6.QtWidgets import (QWidget, QApplication, QLabel,
                               QHBoxLayout, QGraphicsOpacityEffect)
from PySide6.QtGui import QPainter, QBrush, QColor, QScreen
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QRect


class Widget(QWidget):
    def __init__(self, text: str, parent=None):
        QWidget.__init__(self)
        self.label = QLabel(text)
        self.label.setStyleSheet("QLabel { color : white; font: 32px;}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                                Qt.AlignmentFlag.AlignVCenter)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.animation = QPropertyAnimation(self)
        eff = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(eff)
        self.animation = QPropertyAnimation(self, b"windowOpacity")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.timer = QTimer()
        self.timer.timeout.connect(self.hideAnimation)

    def paintEvent(self, event):
        self.painter = QPainter(self)

        self.rect = QRect()

        self.rect.setWidth(self.rect.width())
        self.rect.setHeight(self.rect.height())

        self.painter.setBrush(QBrush(QColor(0, 0, 0, 180)))
        self.painter.setPen(Qt.NoPen)
        self.painter.drawRoundedRect(self.rect, 10, 10)
        self.painter.end()

    def show(self):
        self.setWindowOpacity(0)
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        geo = QScreen().availableGeometry()

        self.setGeometry(geo.width() - self.width(),
                         geo.height() - self.height(),
                         self.width()/2, self.height()/3)

        QWidget.show(self)
        self.animation.start()
        self.timer.start(2000)

    def hideAnimation(self):
        self.timer.stop()
        self.timer.timeout.disconnect(self.hideAnimation)

        self.animation.setDuration(100)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)

        self.timer.timeout.connect(self.hide)
        self.timer.start(2000)
        self.animation.start()

    def hide(self):
        self.timer.stop()
        self.animation.stop()
        # QApplication.quit()


# if __name__ == "__main__":
#     app = QApplication([])
#     app.setStyle("Fusion")

#     window = Widget("This works fine")
#     window.show()

#     sys.exit(app.exec())
