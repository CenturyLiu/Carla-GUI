# -*- coding: utf-8 -*-

"""

@author: Weixin Feng
"""
# Purely front end code 
# Mainly Autocode Created by: PyQt5 UI code generator 5.15.0.
#



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import pyqtSignal


class ExtendedQLabel(QLabel):
    '''
    The extended Label support click
    '''
    def __init__(self, parent):
        QLabel.__init__(self, parent)

    clicked=pyqtSignal()
    def mouseReleaseEvent(self, ev):
        self.clicked.emit()

class QHSeperationLine(QtWidgets.QFrame):
    '''
    a horizontal seperation line
    '''
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)

    def set_position(self, x, y, width, height):
        self.setGeometry(QtCore.QRect(x, y, width, height))






class Ui_Form(QWidget):
    '''
        
        
    Main pages for front end containing five pages: front page, intersection page, Traffic light page, vehicle spawning page and vehicle setting page.
    Parameters
    ----------
    Qwidget : QtWidgets.QWidget
        only defines the front end data type


    '''


    # additional lists for front end use
    widgets = []
    label_num = []

    def setupUi(self):
        self.setObjectName("Form")


        ### Front ### all front page items have label end with [Fro]
        # over all widget for whole front page
        self.widgetFrontAll = QtWidgets.QWidget(self)
        self.widgetFrontAll.setObjectName("widgetFrontAll")
        self.widgetFrontAll.setMinimumSize(QtCore.QSize(2000, 971))
        
        #set the layout for front page
        self.horizontalLayoutFront = QtWidgets.QHBoxLayout(self.widgetFrontAll)
        self.horizontalLayoutFront.setObjectName("horizontalLayoutFront")
        
        
        #set left most widget which containg the labels
        self.widget1Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget1Fro.setMinimumSize(QtCore.QSize(600, 951))
        self.widget1Fro.setMaximumSize(QtCore.QSize(600, 951))
        self.widget1Fro.setObjectName("widget1Fro")

        #small label for collision 
        self.SLColFro = QtWidgets.QLabel(self.widget1Fro)
        self.SLColFro.setGeometry(QtCore.QRect(40, 150, 220, 83))
        self.SLColFro.setMinimumSize(QtCore.QSize(220, 83))
        self.SLColFro.setMaximumSize(QtCore.QSize(220, 83))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLColFro.setFont(font)
        self.SLColFro.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLColFro.setObjectName("SLColFro")

        #small label for max speed(navigation speed)
        self.SLMaxVFro = QtWidgets.QLabel(self.widget1Fro)
        self.SLMaxVFro.setGeometry(QtCore.QRect(40, 273, 260, 83))
        self.SLMaxVFro.setAlignment(QtCore.Qt.AlignLeft)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLMaxVFro.setFont(font)
        self.SLMaxVFro.setObjectName("SLMaxVFro")

        #small label for safety distance
        self.SLSafDisFro = QtWidgets.QLabel(self.widget1Fro)
        self.SLSafDisFro.setGeometry(QtCore.QRect(40, 493, 260, 83))
        self.SLSafDisFro.setAlignment(QtCore.Qt.AlignLeft)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLSafDisFro.setFont(font)
        self.SLSafDisFro.setObjectName("SLSafDisFro")

        #small label for number of intersection
        self.SLNumInterFro = QtWidgets.QLabel(self.widget1Fro)
        self.SLNumInterFro.setGeometry(QtCore.QRect(40, 383, 340, 83))
        self.SLNumInterFro.setAlignment(QtCore.Qt.AlignLeft)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLNumInterFro.setFont(font)
        self.SLNumInterFro.setObjectName("SLNumInterFro")

        #start simulation button
        self.StartSimFro = QtWidgets.QPushButton(self.widget1Fro)
        self.StartSimFro.setGeometry(QtCore.QRect(40, 690, 220, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.StartSimFro.setFont(font)
        self.StartSimFro.setObjectName("StartSimFro")

        #big label for front page
        self.BLFro = QtWidgets.QLabel(self.widget1Fro)
        self.BLFro.setGeometry(QtCore.QRect(40, 30, 250, 74))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.BLFro.setFont(font)
        self.BLFro.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BLFro.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.BLFro.setObjectName("BLFro")

        #backbutton
        self.backButtonFro = QtWidgets.QPushButton(self.widget1Fro)
        self.backButtonFro.setGeometry(QtCore.QRect(10, 0, 100, 38))
        self.backButtonFro.setMinimumSize(QtCore.QSize(100, 30))
        self.backButtonFro.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButtonFro.setIcon(icon)
        self.backButtonFro.setIconSize(QtCore.QSize(30, 30))
        self.backButtonFro.setObjectName("backButtonFro")
        self.horizontalLayoutFront.addWidget(self.widget1Fro)

        #checkbox for collision
        self.checkBoxColFro = QtWidgets.QCheckBox(self.widget1Fro)
        self.checkBoxColFro.setGeometry(QtCore.QRect(350, 187, 60, 13))
        self.checkBoxColFro.setMinimumSize(QtCore.QSize(60, 13))
        self.checkBoxColFro.setMaximumSize(QtCore.QSize(80, 13))
        self.checkBoxColFro.setText("")
        self.checkBoxColFro.setObjectName("checkBoxColFro")
        self.checkBoxColFro.toggle()

        #spinbox for max speed
        self.spinBoxMaxVFro = QtWidgets.QSpinBox(self.widget1Fro)
        self.spinBoxMaxVFro.setGeometry(QtCore.QRect(350, 282, 60, 20))
        self.spinBoxMaxVFro.setMinimumSize(QtCore.QSize(60, 20))
        self.spinBoxMaxVFro.setMaximumSize(QtCore.QSize(60, 20))
        self.spinBoxMaxVFro.setObjectName("spinBoxMaxVFro")

        #spinbox for safety distance
        self.spinBoxSafDisFro = QtWidgets.QSpinBox(self.widget1Fro)
        self.spinBoxSafDisFro.setGeometry(QtCore.QRect(350, 502, 60, 20))
        self.spinBoxSafDisFro.setMinimumSize(QtCore.QSize(60, 20))
        self.spinBoxSafDisFro.setMaximumSize(QtCore.QSize(60, 20))
        self.spinBoxSafDisFro.setObjectName("spinBoxSafDisFro")
        self.spinBoxSafDisFro.setValue(0)

        #spinbox for number of intersection
        self.spinBoxNumIntFro = QtWidgets.QSpinBox(self.widget1Fro)
        self.spinBoxNumIntFro.setGeometry(QtCore.QRect(370, 392, 60, 20))
        self.spinBoxNumIntFro.setMinimumSize(QtCore.QSize(60, 20))
        self.spinBoxNumIntFro.setMaximumSize(QtCore.QSize(60, 20))
        self.spinBoxNumIntFro.setMinimum(1)
        self.spinBoxNumIntFro.setObjectName("spinBoxNumIntFro")
        self.spinBoxNumIntFro.setValue(4)

        #spacer for layout using
        self.spacerItemFro1 = QtWidgets.QSpacerItem(500, 200, QtWidgets.QSizePolicy.MinimumExpanding)
        self.horizontalLayoutFront.addItem(self.spacerItemFro1)
        
        #button to go to the left most
        self.LeftMostFro = QtWidgets.QPushButton(self.widgetFrontAll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LeftMostFro.sizePolicy().hasHeightForWidth())
        self.LeftMostFro.setSizePolicy(sizePolicy)
        self.LeftMostFro.setMinimumSize(QtCore.QSize(41, 111))
        self.LeftMostFro.setMaximumSize(QtCore.QSize(41, 111))
        self.LeftMostFro.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/double_arrow_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LeftMostFro.setIcon(icon1)
        self.LeftMostFro.setIconSize(QtCore.QSize(50, 50))
        self.LeftMostFro.setObjectName("LeftMostFro")
        self.horizontalLayoutFront.addWidget(self.LeftMostFro)

        #button to go to one left
        self.LeftFro = QtWidgets.QPushButton(self.widgetFrontAll)
        self.LeftFro.setMinimumSize(QtCore.QSize(41, 111))
        self.LeftFro.setMaximumSize(QtCore.QSize(41, 111))
        self.LeftFro.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/next_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LeftFro.setIcon(icon2)
        self.LeftFro.setIconSize(QtCore.QSize(50, 50))
        self.LeftFro.setObjectName("LeftFro")
        self.horizontalLayoutFront.addWidget(self.LeftFro)

        #widget for 1st intersection part
        self.widget3Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget3Fro.setMinimumSize(QtCore.QSize(110, 455)) 
        self.widget3Fro.setMaximumSize(QtCore.QSize(110, 455)) 
        self.widget3Fro.setObjectName("widget3Fro")
        
        #1st intersection's button
        self.Int1Fro = QtWidgets.QPushButton(self.widget3Fro)
        self.Int1Fro.setGeometry(QtCore.QRect(34, 214, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.Int1Fro.sizePolicy().hasHeightForWidth())
        self.Int1Fro.setSizePolicy(sizePolicy)
        self.Int1Fro.setMinimumSize(QtCore.QSize(34, 34))
        self.Int1Fro.setMaximumSize(QtCore.QSize(34, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Int1Fro.setFont(font)
        self.Int1Fro.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Int1Fro.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Int1Fro.setIconSize(QtCore.QSize(30, 30))
        self.Int1Fro.setObjectName("Int1Fro")

        #1st intersection's picture
        self.Pic1Fro = QtWidgets.QLabel(self.widget3Fro)
        self.Pic1Fro.setGeometry(QtCore.QRect(0, -4, 110, 455))
        self.Pic1Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.Pic1Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.Pic1Fro.setText("")
        self.Pic1Fro.setPixmap(QtGui.QPixmap("images/Intersection 1_cut.png"))
        self.Pic1Fro.setObjectName("Pic1Fro")
        self.Pic1Fro.raise_()
        self.Int1Fro.raise_()
        self.horizontalLayoutFront.addWidget(self.widget3Fro)

        #widget for 2nd intersection part
        self.widget4Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget4Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.widget4Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.widget4Fro.setObjectName("widget4Fro")

        #2nd intersection's button
        self.Int2Fro = QtWidgets.QPushButton(self.widget4Fro)
        self.Int2Fro.setGeometry(QtCore.QRect(34, 214, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.Int2Fro.sizePolicy().hasHeightForWidth())
        self.Int2Fro.setSizePolicy(sizePolicy)
        self.Int2Fro.setMinimumSize(QtCore.QSize(34, 34))
        self.Int2Fro.setMaximumSize(QtCore.QSize(34, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Int2Fro.setFont(font)
        self.Int2Fro.setIconSize(QtCore.QSize(30, 30))
        self.Int2Fro.setObjectName("Int2Fro")

        #2nd intersection's picture
        self.Pic2Fro = QtWidgets.QLabel(self.widget4Fro)
        self.Pic2Fro.setGeometry(QtCore.QRect(0, -4, 110, 455))
        self.Pic2Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.Pic2Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.Pic2Fro.setText("")
        self.Pic2Fro.setPixmap(QtGui.QPixmap("images/Intersection 1_cut.png"))
        self.Pic2Fro.setObjectName("Pic2Fro")
        self.Pic2Fro.raise_()
        self.Int2Fro.raise_()
        self.horizontalLayoutFront.addWidget(self.widget4Fro)

        #widget for 3rd intersection part
        self.widget5Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget5Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.widget5Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.widget5Fro.setObjectName("widget5Fro")

        #3rd intersection's button
        self.Int3Fro = QtWidgets.QPushButton(self.widget5Fro)
        self.Int3Fro.setGeometry(QtCore.QRect(34, 214, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.Int3Fro.sizePolicy().hasHeightForWidth())
        self.Int3Fro.setSizePolicy(sizePolicy)
        self.Int3Fro.setMinimumSize(QtCore.QSize(34, 34))
        self.Int3Fro.setMaximumSize(QtCore.QSize(34, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Int3Fro.setFont(font)
        self.Int3Fro.setText("")
        self.Int3Fro.setIconSize(QtCore.QSize(30, 30))
        self.Int3Fro.setObjectName("Int3Fro")

        #3rd intersection's picture
        self.Pic3Fro = QtWidgets.QLabel(self.widget5Fro)
        self.Pic3Fro.setGeometry(QtCore.QRect(0, -4, 110, 455))
        self.Pic3Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.Pic3Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.Pic3Fro.setText("")
        self.Pic3Fro.setPixmap(QtGui.QPixmap("images/Intersection 1_cut.png"))
        self.Pic3Fro.setObjectName("Pic3Fro")
        self.Pic3Fro.raise_()
        self.Int3Fro.raise_()
        self.horizontalLayoutFront.addWidget(self.widget5Fro)

        #widget for 4th intersection part
        self.widget6Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget6Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.widget6Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.widget6Fro.setObjectName("widget6Fro")

        #4th intersection's button
        self.Int4Fro = QtWidgets.QPushButton(self.widget6Fro)
        self.Int4Fro.setGeometry(QtCore.QRect(34, 214, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.Int4Fro.sizePolicy().hasHeightForWidth())
        self.Int4Fro.setSizePolicy(sizePolicy)
        self.Int4Fro.setMinimumSize(QtCore.QSize(34, 34))
        self.Int4Fro.setMaximumSize(QtCore.QSize(34, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Int4Fro.setFont(font)
        self.Int4Fro.setText("")
        self.Int4Fro.setIconSize(QtCore.QSize(30, 30))
        self.Int4Fro.setObjectName("Int4Fro")

        #4th intersection's picture
        self.Pic4Fro = QtWidgets.QLabel(self.widget6Fro)
        self.Pic4Fro.setGeometry(QtCore.QRect(0, -4, 110, 455))
        self.Pic4Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.Pic4Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.Pic4Fro.setText("")
        self.Pic4Fro.setPixmap(QtGui.QPixmap("images/Intersection 1_cut.png"))
        self.Pic4Fro.setObjectName("Pic4Fro")
        self.Pic4Fro.raise_()
        self.Int4Fro.raise_()
        self.horizontalLayoutFront.addWidget(self.widget6Fro)
        
        #widget for 5th intersection part
        self.widget7Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget7Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.widget7Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.widget7Fro.setObjectName("widget7Fro")

        #5th intersection's button
        self.Int5Fro = QtWidgets.QPushButton(self.widget7Fro)
        self.Int5Fro.setGeometry(QtCore.QRect(34, 214, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.Int5Fro.sizePolicy().hasHeightForWidth())
        self.Int5Fro.setSizePolicy(sizePolicy)
        self.Int5Fro.setMinimumSize(QtCore.QSize(34, 34))
        self.Int5Fro.setMaximumSize(QtCore.QSize(34, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Int5Fro.setFont(font)
        self.Int5Fro.setText("")
        self.Int5Fro.setIconSize(QtCore.QSize(30, 30))
        self.Int5Fro.setObjectName("Int5Fro")

        #5th intersection's picture
        self.Pic5Fro = QtWidgets.QLabel(self.widget7Fro)
        self.Pic5Fro.setGeometry(QtCore.QRect(0, -4, 110, 455))
        self.Pic5Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.Pic5Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.Pic5Fro.setText("")
        self.Pic5Fro.setPixmap(QtGui.QPixmap("images/Intersection 1_cut.png"))
        self.Pic5Fro.setObjectName("Pic5Fro")
        self.Pic5Fro.raise_()
        self.Int5Fro.raise_()
        self.horizontalLayoutFront.addWidget(self.widget7Fro)

        #widget for 6th intersection part
        self.widget8Fro = QtWidgets.QWidget(self.widgetFrontAll)
        self.widget8Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.widget8Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.widget8Fro.setObjectName("widget8Fro")

        #6th intersection's button
        self.Int6Fro = QtWidgets.QPushButton(self.widget8Fro)
        self.Int6Fro.setGeometry(QtCore.QRect(34, 214, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.Int6Fro.sizePolicy().hasHeightForWidth())
        self.Int6Fro.setSizePolicy(sizePolicy)
        self.Int6Fro.setMinimumSize(QtCore.QSize(34, 34))
        self.Int6Fro.setMaximumSize(QtCore.QSize(34, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Int6Fro.setFont(font)
        self.Int6Fro.setText("")
        self.Int6Fro.setIconSize(QtCore.QSize(30, 30))
        self.Int6Fro.setObjectName("Int6Fro")

        #5th intersection's picture
        self.Pic6Fro = QtWidgets.QLabel(self.widget8Fro)
        self.Pic6Fro.setGeometry(QtCore.QRect(0, -4, 110, 455))
        self.Pic6Fro.setMinimumSize(QtCore.QSize(110, 455))
        self.Pic6Fro.setMaximumSize(QtCore.QSize(110, 455))
        self.Pic6Fro.setText("")
        self.Pic6Fro.setPixmap(QtGui.QPixmap("images/Intersection 1_cut.png"))
        self.Pic6Fro.setObjectName("Pic6Fro")
        self.Pic6Fro.raise_()
        self.Int6Fro.raise_()
        self.horizontalLayoutFront.addWidget(self.widget8Fro)

        #button to go to one left
        self.RightFro = QtWidgets.QPushButton(self.widgetFrontAll)
        self.RightFro.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RightFro.sizePolicy().hasHeightForWidth())
        self.RightFro.setSizePolicy(sizePolicy)
        self.RightFro.setMinimumSize(QtCore.QSize(41, 111))
        self.RightFro.setMaximumSize(QtCore.QSize(41, 111))
        self.RightFro.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RightFro.setIcon(icon4)
        self.RightFro.setIconSize(QtCore.QSize(50, 50))
        self.RightFro.setObjectName("RightFro")
        self.horizontalLayoutFront.addWidget(self.RightFro)

        #button to go to the left most
        self.RightMostFro = QtWidgets.QPushButton(self.widgetFrontAll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RightMostFro.sizePolicy().hasHeightForWidth())
        self.RightMostFro.setSizePolicy(sizePolicy)
        self.RightMostFro.setMinimumSize(QtCore.QSize(41, 111))
        self.RightMostFro.setMaximumSize(QtCore.QSize(41, 111))
        self.RightMostFro.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/double_arrow_512x768.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RightMostFro.setIcon(icon5)
        self.RightMostFro.setIconSize(QtCore.QSize(50, 50))
        self.RightMostFro.setObjectName("RightMostFro")       
        self.horizontalLayoutFront.addWidget(self.RightMostFro)
        
        #spacer for layout using
        self.spacerItemFro2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding)
        self.horizontalLayoutFront.addItem(self.spacerItemFro2)

        #save buttons in a list
        self.label_num.append(self.Int1Fro)
        self.label_num.append(self.Int2Fro)
        self.label_num.append(self.Int3Fro)
        self.label_num.append(self.Int4Fro)
        self.label_num.append(self.Int5Fro)
        self.label_num.append(self.Int6Fro)
        

        ### intersection ### all intersection page items have label end with [Int]
        # over all widget for whole intersection page(including car map)
        self.widgetIntAll = QtWidgets.QWidget(self)
        self.widgetIntAll.setGeometry(QtCore.QRect(0, 0, 2000, 971))
        self.widgetIntAll.setObjectName("widgetIntAll")

        #set the layout for intersection page
        self.horizontalLayoutInt = QtWidgets.QHBoxLayout(self.widgetIntAll)
        self.horizontalLayoutInt.setObjectName("horizontalLayoutInt")
        self.widgetInt = QtWidgets.QWidget(self.widgetIntAll)
        self.widgetInt.setMinimumSize(QtCore.QSize(600, 951))
        self.widgetInt.setMaximumSize(QtCore.QSize(600, 951))
        self.widgetInt.setObjectName("widgetInt")

        #back button
        self.backButtonInt = QtWidgets.QPushButton(self.widgetInt)
        self.backButtonInt.setGeometry(QtCore.QRect(10, 0, 100, 38))
        self.backButtonInt.setMinimumSize(QtCore.QSize(100, 30))
        self.backButtonInt.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButtonInt.setIcon(icon)
        self.backButtonInt.setIconSize(QtCore.QSize(30, 30))
        self.backButtonInt.setObjectName("backButtonInt")

        #big label for intersection page
        self.BLInt = QtWidgets.QLabel(self.widgetInt)
        self.BLInt.setGeometry(QtCore.QRect(40, 30, 160, 74))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.BLInt.setFont(font)
        self.BLInt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BLInt.setAlignment(QtCore.Qt.AlignLeft)
        self.BLInt.setObjectName("BLInt")

        #small label for intersection ID
        self.SLIDInt = QtWidgets.QLabel(self.widgetInt)
        self.SLIDInt.setGeometry(QtCore.QRect(40, 170, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLIDInt.setFont(font)
        self.SLIDInt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLIDInt.setObjectName("SLIDInt")

        #combo box for intersection ID
        self.cobBoxIDInt = QtWidgets.QComboBox(self.widgetInt)
        self.cobBoxIDInt.setGeometry(QtCore.QRect(350, 178, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxIDInt.setFont(font)
        self.cobBoxIDInt.setEditable(False)
        self.cobBoxIDInt.setObjectName("cobBoxIDInt")
        self.cobBoxIDInt.addItem("")
        self.cobBoxIDInt.addItem("")
        self.cobBoxIDInt.addItem("")
        self.cobBoxIDInt.addItem("")

        #combo box for intersection import
        self.cobBoxImportInt = QtWidgets.QComboBox(self.widgetInt)
        self.cobBoxImportInt.setGeometry(QtCore.QRect(350, 328, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxImportInt.setFont(font)
        self.cobBoxImportInt.setEditable(False)
        self.cobBoxImportInt.setObjectName("cobBoxImportInt")
        self.cobBoxImportInt.addItem("")
        self.cobBoxImportInt.setCurrentIndex(0)

        #small label for traffic light
        self.SLTrafLightInt = QtWidgets.QLabel(self.widgetInt)
        self.SLTrafLightInt.setGeometry(QtCore.QRect(40, 620, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLTrafLightInt.setFont(font)
        self.SLTrafLightInt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLTrafLightInt.setObjectName("SLTrafLightInt")


        #button for traffic light
        self.TrafLightInt = QtWidgets.QPushButton(self.widgetInt)
        self.TrafLightInt.setGeometry(QtCore.QRect(350, 620, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.TrafLightInt.setFont(font)
        self.TrafLightInt.setObjectName("TrafLightInt")

        #small label for add vehicle 
        self.SLAddVehInt = QtWidgets.QLabel(self.widgetInt)
        self.SLAddVehInt.setGeometry(QtCore.QRect(40, 470, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLAddVehInt.setFont(font)
        self.SLAddVehInt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLAddVehInt.setObjectName("SLAddVehInt")

        #button for add vehicle
        self.AddVehInt = QtWidgets.QPushButton(self.widgetInt)
        self.AddVehInt.setGeometry(QtCore.QRect(350, 470, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.AddVehInt.setFont(font)
        self.AddVehInt.setObjectName("AddVehInt")

        #small label for intersection import
        self.SLImportInt = QtWidgets.QLabel(self.widgetInt)
        self.SLImportInt.setGeometry(QtCore.QRect(40, 320, 171, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLImportInt.setFont(font)
        self.SLImportInt.setObjectName("SLImportInt")
        
        self.horizontalLayoutInt.addWidget(self.widgetInt)

        ##Traffic Light Setting page(containing in intersection widget)##all traffic light page items have label end with [Lit]
        #widget light
        self.widgetLit = QtWidgets.QWidget(self.widgetIntAll)
        self.widgetLit.setGeometry(QtCore.QRect(10, 10, 600, 951))
        self.widgetLit.setMinimumSize(QtCore.QSize(600, 951))
        self.widgetLit.setMaximumSize(QtCore.QSize(600, 951))
        self.widgetLit.setObjectName("widgetLit")

        #back button
        self.backButtonLit = QtWidgets.QPushButton(self.widgetLit)
        self.backButtonLit.setGeometry(QtCore.QRect(10, 0, 100, 38))
        self.backButtonLit.setMinimumSize(QtCore.QSize(100, 30))
        self.backButtonLit.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButtonLit.setIcon(icon)
        self.backButtonLit.setIconSize(QtCore.QSize(30, 30))
        self.backButtonLit.setObjectName("backButtonLit")

        #big label for light page
        self.BLLit = QtWidgets.QLabel(self.widgetLit)
        self.BLLit.setGeometry(QtCore.QRect(40, 30, 260, 74))
        self.BLLit.setMinimumSize(QtCore.QSize(240, 74))
        self.BLLit.setMaximumSize(QtCore.QSize(240, 74))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.BLLit.setFont(font)
        self.BLLit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BLLit.setAlignment(QtCore.Qt.AlignCenter)
        self.BLLit.setObjectName("BLLit")

        #1st small label
        self.SL1Lit = QtWidgets.QLabel(self.widgetLit)
        self.SL1Lit.setGeometry(QtCore.QRect(40, 170, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SL1Lit.setFont(font)
        self.SL1Lit.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SL1Lit.setObjectName("SL1Lit")
        self.SL1Lit.setStyleSheet("background:rgb({},{},{}); color:{};".format(204,0,0,(0,0,0)))

        #2nd small label
        self.SL2Lit = QtWidgets.QLabel(self.widgetLit)
        self.SL2Lit.setGeometry(QtCore.QRect(40, 320, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SL2Lit.setFont(font)
        self.SL2Lit.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SL2Lit.setObjectName("SL2Lit")
        self.SL2Lit.setStyleSheet("background:rgb({},{},{}); color:{};".format(0,102,204,(0,0,0)))

        #3rd small label
        self.SL3Lit = QtWidgets.QLabel(self.widgetLit)
        self.SL3Lit.setGeometry(QtCore.QRect(40, 470, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SL3Lit.setFont(font)
        self.SL3Lit.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SL3Lit.setObjectName("SL3Lit")
        self.SL3Lit.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,51,(0,0,0)))

        #4th small label
        self.SL4Lit = QtWidgets.QLabel(self.widgetLit)
        self.SL4Lit.setGeometry(QtCore.QRect(40, 620, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SL4Lit.setFont(font)
        self.SL4Lit.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SL4Lit.setObjectName("SL4Lit")
        self.SL4Lit.setStyleSheet("background:rgb({},{},{}); color:{};".format(0,204,0,(0,0,0)))

        #1st light button
        self.set1Lit = QtWidgets.QPushButton(self.widgetLit)
        self.set1Lit.setGeometry(QtCore.QRect(350, 170, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.set1Lit.setFont(font)
        self.set1Lit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.set1Lit.setObjectName("set1Lit")

        #2nd light button
        self.set2Lit = QtWidgets.QPushButton(self.widgetLit)
        self.set2Lit.setGeometry(QtCore.QRect(350, 320, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.set2Lit.setFont(font)
        self.set2Lit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.set2Lit.setObjectName("set2Lit")

        #3rd light button
        self.set3Lit = QtWidgets.QPushButton(self.widgetLit)
        self.set3Lit.setGeometry(QtCore.QRect(350, 470, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.set3Lit.setFont(font)
        self.set3Lit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.set3Lit.setObjectName("set3Lit")

        #4th light button
        self.set4Lit = QtWidgets.QPushButton(self.widgetLit)
        self.set4Lit.setGeometry(QtCore.QRect(350, 620, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.set4Lit.setFont(font)
        self.set4Lit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.set4Lit.setObjectName("set4Lit")
        
        self.horizontalLayoutInt.addWidget(self.widgetLit)
        self.widgetLit.hide()

        ##spawn vehicle page(containing in intersection widget)##all spawn vehicle page items have label end with [Spa]
        self.widgetSpa = QtWidgets.QWidget(self.widgetIntAll)
        self.widgetSpa.setGeometry(QtCore.QRect(10, 10, 600, 951))
        self.widgetSpa.setMinimumSize(QtCore.QSize(600, 951))
        self.widgetSpa.setMaximumSize(QtCore.QSize(600, 951))
        self.widgetSpa.setObjectName("widgetSpa")

        #back button
        self.backButtonSpa = QtWidgets.QPushButton(self.widgetSpa)
        self.backButtonSpa.setGeometry(QtCore.QRect(10, 0, 100, 38))
        self.backButtonSpa.setMinimumSize(QtCore.QSize(100, 30))
        self.backButtonSpa.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButtonSpa.setIcon(icon)
        self.backButtonSpa.setIconSize(QtCore.QSize(30, 30))
        self.backButtonSpa.setObjectName("backButtonSpa")

        #big label for spawn page
        self.BLSpa = QtWidgets.QLabel(self.widgetSpa)
        self.BLSpa.setGeometry(QtCore.QRect(40, 30, 190, 74))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.BLSpa.setFont(font)
        self.BLSpa.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BLSpa.setAlignment(QtCore.Qt.AlignLeft)
        self.BLSpa.setObjectName("BLSpa")

        #small label for subject lane spawn
        self.SLSubSpa = QtWidgets.QLabel(self.widgetSpa)
        self.SLSubSpa.setGeometry(QtCore.QRect(40, 170, 150, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLSubSpa.setFont(font)
        self.SLSubSpa.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SLSubSpa.setObjectName("SLSubSpa")
        self.SLSubSpa.setStyleSheet("background:rgb({},{},{}); color:{};".format(204,0,0,(0,0,0)))

        #small label for left lane spawn
        self.SLLeftSpa = QtWidgets.QLabel(self.widgetSpa)
        self.SLLeftSpa.setGeometry(QtCore.QRect(40, 320, 150, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLLeftSpa.setFont(font)
        self.SLLeftSpa.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SLLeftSpa.setObjectName("SLLeftSpa")
        self.SLLeftSpa.setStyleSheet("background:rgb({},{},{}); color:{};".format(0,102,204,(0,0,0)))

        #button for subject lane spawn
        self.AddSubSpa = QtWidgets.QPushButton(self.widgetSpa)
        self.AddSubSpa.setGeometry(QtCore.QRect(350, 170, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.AddSubSpa.setFont(font)
        self.AddSubSpa.setObjectName("AddSubSpa")
        
        #button for left lane spawn
        self.AddLeftSpa = QtWidgets.QPushButton(self.widgetSpa)
        self.AddLeftSpa.setGeometry(QtCore.QRect(350, 320, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.AddLeftSpa.setFont(font)
        self.AddLeftSpa.setObjectName("AddLeftSpa")

        #button for ahead lane spawn
        self.AddAheadSpa = QtWidgets.QPushButton(self.widgetSpa)
        self.AddAheadSpa.setGeometry(QtCore.QRect(350, 470, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.AddAheadSpa.setFont(font)
        self.AddAheadSpa.setObjectName("AddAheadSpa")

        #small label for ahead lane spawn
        self.SLAheadSpa = QtWidgets.QLabel(self.widgetSpa)
        self.SLAheadSpa.setGeometry(QtCore.QRect(40, 470, 150, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLAheadSpa.setFont(font)
        self.SLAheadSpa.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SLAheadSpa.setObjectName("SLAheadSpa")
        self.SLAheadSpa.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,51,(0,0,0)))

        #button for right lane spawn
        self.AddRightSpa = QtWidgets.QPushButton(self.widgetSpa)
        self.AddRightSpa.setGeometry(QtCore.QRect(350, 620, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.AddRightSpa.setFont(font)
        self.AddRightSpa.setObjectName("AddRightSpa")

        #small label for right lane spawn
        self.SLRightSpa = QtWidgets.QLabel(self.widgetSpa)
        self.SLRightSpa.setGeometry(QtCore.QRect(40, 620, 150, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLRightSpa.setFont(font)
        self.SLRightSpa.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SLRightSpa.setObjectName("SLRightSpa")
        self.SLRightSpa.setStyleSheet("background:rgb({},{},{}); color:{};".format(0,204,0,(0,0,0)))
        
        self.horizontalLayoutInt.addWidget(self.widgetSpa)
        self.widgetSpa.hide()

        ##Vehicle setting page(containing in intersection widget)##all vehicle setting page items have label end with [Veh]
        #pre-set vehicle model list
        self.model_list = ["audi a2", "audi etron", "audi tt", "bh crossbike", "bmw grandtourer", \
        "bmw isetta", "carlamotors carlacola", "chevrolet impala", "citroen c3", "diamondback century", \
        "dodge_charger police", "gazelle omafiets", "harley-davidson low_rider", \
        "jeep wrangler_rubicon", "kawasaki ninja", "lincoln mkz2017", "mercedes-benz coupe", \
        "mini cooperst", "mustang mustang", "nissan micra", "nissan patrol", "seat leon", \
        "tesla cybertruck", "tesla model3", "toyota prius", "volkswagen t2", "yamaha yzf"]

        #widget vehicle setting
        self.widgetVeh = QtWidgets.QWidget(self.widgetIntAll)
        self.widgetVeh.setGeometry(QtCore.QRect(10, 10, 600, 951))
        self.widgetVeh.setMinimumSize(QtCore.QSize(600, 951))
        self.widgetVeh.setMaximumSize(QtCore.QSize(600, 951))
        self.widgetVeh.setObjectName("widgetVeh")
        
        #horizontal line
        self.HlineVeh = QtWidgets.QFrame(self.widgetVeh)
        self.HlineVeh.setFrameShape(QtWidgets.QFrame.HLine)
        self.HlineVeh.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HlineVeh.setGeometry(QtCore.QRect(40, 700, 495, 40))

        #back button
        self.backButtonVeh = QtWidgets.QPushButton(self.widgetVeh)
        self.backButtonVeh.setGeometry(QtCore.QRect(10, 0, 100, 38))
        self.backButtonVeh.setMinimumSize(QtCore.QSize(100, 30))
        self.backButtonVeh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButtonVeh.setIcon(icon)
        self.backButtonVeh.setIconSize(QtCore.QSize(30, 30))
        self.backButtonVeh.setObjectName("backButtonVeh")
        
        #car name
        self.CarNameVeh = QtWidgets.QLabel(self.widgetVeh)
        self.CarNameVeh.setGeometry(QtCore.QRect(40, 30, 300, 74))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.CarNameVeh.setFont(font)
        self.CarNameVeh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CarNameVeh.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.CarNameVeh.setObjectName("CarNameVeh")

        #small label for turn setting
        self.SLTurnVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLTurnVeh.setGeometry(QtCore.QRect(40, 108, 180, 83))
        self.SLTurnVeh.setMinimumSize(QtCore.QSize(180, 83))
        self.SLTurnVeh.setMaximumSize(QtCore.QSize(180, 83))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLTurnVeh.setFont(font)
        self.SLTurnVeh.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLTurnVeh.setObjectName("SLTurnVeh")
             
        #small label for stop setting
        self.SLStopVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLStopVeh.setGeometry(QtCore.QRect(40, 178, 180, 83))
        self.SLStopVeh.setMinimumSize(QtCore.QSize(180, 83))
        self.SLStopVeh.setMaximumSize(QtCore.QSize(180, 83))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLStopVeh.setFont(font)
        self.SLStopVeh.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLStopVeh.setObjectName("SLStopVeh")
        
        #small label for color setting
        self.SLColorVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLColorVeh.setGeometry(QtCore.QRect(40, 315, 180, 83))
        self.SLColorVeh.setMinimumSize(QtCore.QSize(180, 83))
        self.SLColorVeh.setMaximumSize(QtCore.QSize(180, 83))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLColorVeh.setFont(font)
        self.SLColorVeh.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLColorVeh.setObjectName("SLColorVeh")

        #edit box for color R
        self.lineEditRVeh = QtWidgets.QLineEdit(self.widgetVeh)
        self.lineEditRVeh.setGeometry(QtCore.QRect(100,390, 61, 31))
        self.lineEditRVeh.setObjectName("lineEditRVeh")

        #small label for color R
        self.SLcolRVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLcolRVeh.setGeometry(QtCore.QRect(60, 383, 47, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLcolRVeh.setFont(font)
        self.SLcolRVeh.setObjectName("SLcolRVeh")

        #edit box for color G
        self.lineEditGVeh = QtWidgets.QLineEdit(self.widgetVeh)
        self.lineEditGVeh.setGeometry(QtCore.QRect(285, 390, 61, 31))
        self.lineEditGVeh.setObjectName("lineEditGVeh")

        #small label for color G
        self.SLcolGVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLcolGVeh.setGeometry(QtCore.QRect(245, 383, 47, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLcolGVeh.setFont(font)
        self.SLcolGVeh.setObjectName("SLcolGVeh")

        #edit box for color B
        self.lineEditBVeh = QtWidgets.QLineEdit(self.widgetVeh)
        self.lineEditBVeh.setGeometry(QtCore.QRect(469, 390, 61, 31))
        self.lineEditBVeh.setObjectName("lineEditBVeh")

        #small label for color B
        self.SLcolBVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLcolBVeh.setGeometry(QtCore.QRect(430, 383, 47, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLcolBVeh.setFont(font)
        self.SLcolBVeh.setObjectName("SLcolBVeh")

        #radio box for obey traffic light
        self.radButObeyVeh = QtWidgets.QRadioButton(self.widgetVeh)
        self.radButObeyVeh.setGeometry(QtCore.QRect(39, 605, 491, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.radButObeyVeh.setFont(font)
        self.radButObeyVeh.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radButObeyVeh.setObjectName("radButObeyVeh")

        #delete button
        self.DeleteVeh = QtWidgets.QPushButton(self.widgetVeh)
        self.DeleteVeh.setGeometry(QtCore.QRect(40, 800, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.DeleteVeh.setFont(font)
        self.DeleteVeh.setObjectName("DeleteVeh")

        #confirm button
        self.confirmVeh = QtWidgets.QPushButton(self.widgetVeh)
        self.confirmVeh.setGeometry(QtCore.QRect(40, 890, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.confirmVeh.setFont(font)
        self.confirmVeh.setObjectName("confirmVeh")

        #combo box for stop
        self.cobBoxStopVeh = QtWidgets.QComboBox(self.widgetVeh)
        self.cobBoxStopVeh.setGeometry(QtCore.QRect(350, 205, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxStopVeh.setFont(font)
        self.cobBoxStopVeh.setObjectName("cobBoxStopVeh")
        self.cobBoxStopVeh.addItem("")
        self.cobBoxStopVeh.addItem("")
        self.cobBoxStopVeh.addItem("")

        #combo box for turn
        self.cobBoxTurnVeh = QtWidgets.QComboBox(self.widgetVeh)
        self.cobBoxTurnVeh.setGeometry(QtCore.QRect(350, 135, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxTurnVeh.setFont(font)
        self.cobBoxTurnVeh.setObjectName("cobBoxTurnVeh")
        self.cobBoxTurnVeh.addItem("")
        self.cobBoxTurnVeh.addItem("")
        self.cobBoxTurnVeh.addItem("")

        #small label for safe distance
        self.SLsafeDisVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLsafeDisVeh.setGeometry(QtCore.QRect(40, 530, 181, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLsafeDisVeh.setFont(font)
        self.SLsafeDisVeh.setObjectName("SLsafeDisVeh")

        #spin box for gap
        self.spinBoxGapVeh = QtWidgets.QSpinBox(self.widgetVeh)
        self.spinBoxGapVeh.setGeometry(QtCore.QRect(470, 470, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.spinBoxGapVeh.setFont(font)
        self.spinBoxGapVeh.setObjectName("spinBoxGapVeh")
        self.spinBoxGapVeh.setValue(10)

        #small label for gap
        self.SLGapVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLGapVeh.setGeometry(QtCore.QRect(40, 460, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLGapVeh.setFont(font)
        self.SLGapVeh.setObjectName("SLGapVeh")

        #spin box for safety distance
        self.spinBoxSafeDisVeh = QtWidgets.QSpinBox(self.widgetVeh)
        self.spinBoxSafeDisVeh.setGeometry(QtCore.QRect(470, 545, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.spinBoxSafeDisVeh.setFont(font)
        self.spinBoxSafeDisVeh.setObjectName("spinBoxSafeDisVeh")
        self.spinBoxSafeDisVeh.setValue(0)

        #small label for model
        self.SLModVeh = QtWidgets.QLabel(self.widgetVeh)
        self.SLModVeh.setGeometry(QtCore.QRect(40, 265, 160, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLModVeh.setFont(font)
        self.SLModVeh.setObjectName("SLModVeh")

        #combo box for model
        self.cobBoxModVeh = QtWidgets.QComboBox(self.widgetVeh)
        self.cobBoxModVeh.setGeometry(QtCore.QRect(350, 275, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxModVeh.setFont(font)
        self.cobBoxModVeh.setObjectName("cobBoxModVeh")
        for i in range(27):
            self.cobBoxModVeh.addItem("")

        self.horizontalLayoutInt.addWidget(self.widgetVeh)
        self.widgetVeh.hide()
        

        #Widget Map(do not change in all intersection pages)
        #spacer for layout using
        self.spacerItemInt1 = QtWidgets.QSpacerItem(500, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutInt.addItem(self.spacerItemInt1)

        #map widget
        self.widgetMap = QtWidgets.QWidget(self.widgetIntAll)
        self.widgetMap.setMinimumSize(QtCore.QSize(641, 0))
        self.widgetMap.setMaximumSize(QtCore.QSize(641, 16777215))
        self.widgetMap.setObjectName("widgetMap")

        #label to show map
        self.CarMap = QtWidgets.QLabel(self.widgetMap)
        self.CarMap.setGeometry(QtCore.QRect(0, 50, 641, 751))
        self.CarMap.setText("")
        self.CarMap.setPixmap(QtGui.QPixmap("images/intersection.jpg"))
        self.CarMap.setObjectName("CarMap")

        #label to number the light1 with color
        self.Light1 = QLabel(self.widgetMap)
        self.Light1.setGeometry(QtCore.QRect(420, 270, 40, 40))
        self.Light1.setObjectName("CarSub")
        self.Light1.setStyleSheet("background:rgb({},{},{}); color:{};".format(204,0,0,(0,0,0)))
        self.Light1.setText("1")
        self.Light1.setAlignment(QtCore.Qt.AlignCenter)

        #label to number the light2 with color
        self.Light2 = QLabel(self.widgetMap)
        self.Light2.setGeometry(QtCore.QRect(420, 500, 40, 40))
        self.Light2.setObjectName("Light2")
        self.Light2.setStyleSheet("background:rgb({},{},{}); color:{};".format(0,102,204,(0,0,0)))
        self.Light2.setText("2")
        self.Light2.setAlignment(QtCore.Qt.AlignCenter)
        
        #label to number the light3 with color
        self.Light3 = QLabel(self.widgetMap)
        self.Light3.setGeometry(QtCore.QRect(180, 500, 40, 40))
        self.Light3.setObjectName("Light3")
        self.Light3.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,51,(0,0,0)))
        self.Light3.setText("3")
        self.Light3.setAlignment(QtCore.Qt.AlignCenter)

        #label to number the light4 with color
        self.Light4 = QLabel(self.widgetMap)
        self.Light4.setGeometry(QtCore.QRect(180, 270, 40, 40))
        self.Light4.setObjectName("Light4")
        self.Light4.setStyleSheet("background:rgb({},{},{}); color:{};".format(0,204,0,(0,0,0)))
        self.Light4.setText("4")
        self.Light4.setAlignment(QtCore.Qt.AlignCenter)

        #init sublane cars(extended label)
        for i in range (4):
            self.CarSub = ExtendedQLabel(self.widgetMap)
            self.CarSub.setGeometry(QtCore.QRect(334, 455 + i * 80, 35, 45))
            self.CarSub.setObjectName("CarSub" + str(i + 1))
            self.CarSub.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,255,(0,0,0)))
            self.CarSub.setText(str(i + 1))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(8)
            self.CarSub.setFont(font)
            self.CarSub.setAlignment(QtCore.Qt.AlignCenter)
            self.CarSub.hide()

        #init leftlane cars(extended label)
        for i in range (4):
            self.CarLeft = ExtendedQLabel(self.widgetMap)
            self.CarLeft.setGeometry(QtCore.QRect(228 - i * 70, 413, 45, 35))
            self.CarLeft.setObjectName("CarLeft" + str(i + 1))
            self.CarLeft.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,255,(0,0,0)))
            self.CarLeft.setText(str(i + 1))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(8)
            self.CarLeft.setFont(font)
            self.CarLeft.setAlignment(QtCore.Qt.AlignCenter)
            self.CarLeft.hide()

        #init aheadlane cars(extended label)
        for i in range (4):
            self.CarAhead = ExtendedQLabel(self.widgetMap)
            self.CarAhead.setGeometry(QtCore.QRect(282, 321 - i * 80, 35, 45))
            self.CarAhead.setObjectName("CarAhead" + str(i + 1))
            self.CarAhead.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,255,(0,0,0)))
            self.CarAhead.setText(str(i + 1))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(8)
            self.CarAhead.setFont(font)
            self.CarAhead.setAlignment(QtCore.Qt.AlignCenter)
            self.CarAhead.hide()

        #init rightlane cars(extended label)
        for i in range (4):
            self.CarRight = ExtendedQLabel(self.widgetMap)
            self.CarRight.setGeometry(QtCore.QRect(374 + i * 70, 368, 45, 35))
            self.CarRight.setObjectName("CarRight" + str(i + 1))
            self.CarRight.setStyleSheet("background:rgb({},{},{}); color:{};".format(255,255,255,(0,0,0)))
            self.CarRight.setText(str(i + 1))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(8)
            self.CarRight.setFont(font)
            self.CarRight.setAlignment(QtCore.Qt.AlignCenter)
            self.CarRight.hide()

        self.horizontalLayoutInt.addWidget(self.widgetMap)
        
        #spacer item for layout using
        self.spacerItemInt2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutInt.addItem(self.spacerItemInt2)

        self.retranslateUi()
        self.cobBoxIDInt.setCurrentIndex(0)
        self.cobBoxImportInt.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        #save widgets other than vehicle setting in list for changing page to vehicle setting page
        self.widgets.append(self.widgetInt)
        self.widgets.append(self.widgetLit)
        self.widgets.append(self.widgetSpa)
        self.widgetIntAll.hide()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate        
        # Front Translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.SLColFro.setText(_translate("Form", "Allow Collisions"))
        self.SLMaxVFro.setText(_translate("Form", "Max Speed (km/h)"))
        self.SLSafDisFro.setText(_translate("Form", "Safety Distance (m)"))
        self.SLNumInterFro.setText(_translate("Form", "Number of Intersections"))
        self.StartSimFro.setText(_translate("Form", "Start Simulation"))
        self.BLFro.setText(_translate("Form", "General Settings"))
        self.Int1Fro.setText(_translate("Form", "1"))
        self.Int2Fro.setText(_translate("Form", "2"))
        self.Int3Fro.setText(_translate("Form", "3"))
        self.Int4Fro.setText(_translate("Form", "4"))
        # self.Int5Fro.setText(_translate("Form", "5"))
        # self.Int6Fro.setText(_translate("Form", "6"))
        #Intersection Translate 

        self.setWindowTitle(_translate("Form", "Form"))
        self.BLInt.setText(_translate("Form", "Intersection"))
        self.SLIDInt.setText(_translate("Form", "Intersection ID"))
        self.SLTrafLightInt.setText(_translate("Form", "Traffic Light"))
        self.SLAddVehInt.setText(_translate("Form", "Vehicles"))
        self.cobBoxIDInt.setItemText(0, _translate("Form", "Intersection 1"))
        self.cobBoxIDInt.setItemText(1, _translate("Form", "Intersection 2"))
        self.cobBoxIDInt.setItemText(2, _translate("Form", "Intersection 3"))
        self.cobBoxIDInt.setItemText(3, _translate("Form", "Intersection 4"))
        self.TrafLightInt.setText(_translate("Form", "Setting"))
        self.AddVehInt.setText(_translate("Form", "Setting"))
        self.SLImportInt.setText(_translate("Form", "Import Settings"))
        self.cobBoxImportInt.setItemText(0, _translate("Form", ""))        

        #Traffic Light Translate 
        self.BLLit.setText(_translate("Form", "Traffic Light Settings"))
        self.SL1Lit.setText(_translate("Form", "Light 1"))
        self.SL2Lit.setText(_translate("Form", "Light 2"))
        self.SL3Lit.setText(_translate("Form", "Light 3"))
        self.SL4Lit.setText(_translate("Form", "Light 4"))
        self.set1Lit.setText(_translate("Form", "Setting"))
        self.set2Lit.setText(_translate("Form", "Setting"))
        self.set3Lit.setText(_translate("Form", "Setting"))
        self.set4Lit.setText(_translate("Form", "Setting"))

        #Spawn Translate 
        self.BLSpa.setText(_translate("Form", "Spawn Vehicle"))
        self.SLSubSpa.setText(_translate("Form", "Subject Lane"))
        self.SLLeftSpa.setText(_translate("Form", "Left Lane"))
        self.AddSubSpa.setText(_translate("Form", "Add Vehicle"))
        self.AddLeftSpa.setText(_translate("Form", "Add Vehicle"))
        self.AddRightSpa.setText(_translate("Form", "Add Vehicle"))
        self.SLRightSpa.setText(_translate("Form", "Right Lane"))
        self.AddAheadSpa.setText(_translate("Form", "Add Vehicle"))
        self.SLAheadSpa.setText(_translate("Form", "Ahead Lane"))

        #Vehicle Setting Translate 
        for i in range(27):
            self.cobBoxModVeh.setItemText(i, _translate("AddVehicle", self.model_list[i]))
        self.SLModVeh.setText(_translate("Form", "Vehicle Model"))
        self.CarNameVeh.setText(_translate("Form", "Car_name"))
        self.SLTurnVeh.setText(_translate("Form", "Turn"))
        self.SLStopVeh.setText(_translate("Form", "Stop"))
        self.SLColorVeh.setText(_translate("Form", "Color"))
        self.SLcolRVeh.setText(_translate("Form", "R:"))
        self.SLcolGVeh.setText(_translate("Form", "G:"))
        self.SLcolBVeh.setText(_translate("Form", "B:"))
        self.radButObeyVeh.setText(_translate("Form", "Obey traffic Light                                         "))
        self.DeleteVeh.setText(_translate("Form", "Delete"))
        self.confirmVeh.setText(_translate("Form", "Confirm"))
        self.cobBoxStopVeh.setItemText(0, _translate("Form", "Normal Stop"))
        self.cobBoxStopVeh.setItemText(1, _translate("Form", "Abrupt Stop"))
        self.cobBoxStopVeh.setItemText(2, _translate("Form", "Penetrate Stop"))
        self.cobBoxTurnVeh.setItemText(0, _translate("Form", "Straight"))
        self.cobBoxTurnVeh.setItemText(1, _translate("Form", "Left"))
        self.cobBoxTurnVeh.setItemText(2, _translate("Form", "Right"))
        self.SLsafeDisVeh.setText(_translate("Form", "Safety Distance"))
        self.SLGapVeh.setText(_translate("Form", "Gap"))





###Traffic light dialogue###all traffic light dialogue page items have label end with [TLDia]
class Ui_TrafLightSet(QDialog):
    def setupUi(self):
        self.setObjectName("TrafLightSet")
        self.resize(492, 327)
        self.move(578, 300)

        #button box 
        self.buttonBoxTLDia = QtWidgets.QDialogButtonBox(self)
        self.buttonBoxTLDia.setGeometry(QtCore.QRect(320, 290, 156, 23))
        self.buttonBoxTLDia.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxTLDia.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxTLDia.setObjectName("buttonBoxTLDia")

        #spin box for 1st light duration
        self.SpinBox1TLDia = QtWidgets.QDoubleSpinBox(self)
        self.SpinBox1TLDia.setGeometry(QtCore.QRect(420, 25, 62, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.SpinBox1TLDia.setFont(font)
        self.SpinBox1TLDia.setObjectName("SpinBox1TLDia")

        #spin box for 2nd light duration
        self.SpinBox2TLDia = QtWidgets.QDoubleSpinBox(self)
        self.SpinBox2TLDia.setGeometry(QtCore.QRect(420, 100, 62, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.SpinBox2TLDia.setFont(font)
        self.SpinBox2TLDia.setObjectName("SpinBox2TLDia")

        #spin box for 3rd light duration
        self.SpinBox3TLDia = QtWidgets.QDoubleSpinBox(self)
        self.SpinBox3TLDia.setGeometry(QtCore.QRect(420, 184, 62, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.SpinBox3TLDia.setFont(font)
        self.SpinBox3TLDia.setObjectName("SpinBox3TLDia")

        #combo box for 1st light duration
        self.cobBox1TLDia = QtWidgets.QComboBox(self)
        self.cobBox1TLDia.setGeometry(QtCore.QRect(180, 20, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBox1TLDia.setFont(font)
        self.cobBox1TLDia.setObjectName("cobBox1TLDia")
        self.cobBox1TLDia.addItem("")
        self.cobBox1TLDia.addItem("")
        self.cobBox1TLDia.addItem("")

        #combo box for 2nd light duration
        self.cobBox2TLDia = QtWidgets.QComboBox(self)
        self.cobBox2TLDia.setGeometry(QtCore.QRect(180, 95, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBox2TLDia.setFont(font)
        self.cobBox2TLDia.setObjectName("cobBox2TLdia")
        self.cobBox2TLDia.addItem("")
        self.cobBox2TLDia.addItem("")
        self.cobBox2TLDia.addItem("")

        #combo box for 2nd light duration
        self.cobBox3TLDia = QtWidgets.QComboBox(self)
        self.cobBox3TLDia.setGeometry(QtCore.QRect(180, 178, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBox3TLDia.setFont(font)
        self.cobBox3TLDia.setObjectName("cobBox3TLDia")
        self.cobBox3TLDia.addItem("")
        self.cobBox3TLDia.addItem("")
        self.cobBox3TLDia.addItem("")

        #1st big label for traffic light dialogue
        self.BL1TLDia = QtWidgets.QLabel(self)
        self.BL1TLDia.setGeometry(QtCore.QRect(40, 18, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.BL1TLDia.setFont(font)
        self.BL1TLDia.setObjectName("BL1TLDia")

        #2nd big label for traffic light dialogue
        self.BL2TLDia = QtWidgets.QLabel(self)
        self.BL2TLDia.setGeometry(QtCore.QRect(40, 92, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.BL2TLDia.setFont(font)
        self.BL2TLDia.setObjectName("BL2TLDia")

        #3rd big label for traffic light dialogue
        self.BL3TLDia = QtWidgets.QLabel(self)
        self.BL3TLDia.setGeometry(QtCore.QRect(40, 176, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.BL3TLDia.setFont(font)
        self.BL3TLDia.setObjectName("BL3TLDia")

        self.retranslateUi()
        self.cobBox1TLDia.setCurrentIndex(0)
        self.cobBox2TLDia.setCurrentIndex(1)
        self.cobBox3TLDia.setCurrentIndex(2)
        self.buttonBoxTLDia.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("TrafLightSet", "Dialog"))
        self.cobBox1TLDia.setItemText(0, _translate("TrafLightSet", "Red Light Duration"))
        self.cobBox1TLDia.setItemText(1, _translate("TrafLightSet", "Yellow Light Duration"))
        self.cobBox1TLDia.setItemText(2, _translate("TrafLightSet", "Green Light Duration"))
        self.cobBox2TLDia.setItemText(0, _translate("TrafLightSet", "Red Light Duration"))
        self.cobBox2TLDia.setItemText(1, _translate("TrafLightSet", "Yellow Light Duration"))
        self.cobBox2TLDia.setItemText(2, _translate("TrafLightSet", "Green Light Duration"))
        self.cobBox3TLDia.setItemText(0, _translate("TrafLightSet", "Red Light Duration"))
        self.cobBox3TLDia.setItemText(1, _translate("TrafLightSet", "Yellow Light Duration"))
        self.cobBox3TLDia.setItemText(2, _translate("TrafLightSet", "Green Light Duration"))
        self.BL1TLDia.setText(_translate("TrafLightSet", "First"))
        self.BL2TLDia.setText(_translate("TrafLightSet", "Second"))
        self.BL3TLDia.setText(_translate("TrafLightSet", "Third"))

###Add vehicle dialogue###all Add vehicle dialogue page items have label end with [AdDia]
class Ui_AddVehicle(QDialog):
    def setupUi(self):
        self.model_list = ["audi a2", "audi etron", "audi tt", "bh crossbike", "bmw grandtourer", \
        "bmw isetta", "carlamotors carlacola", "chevrolet impala", "citroen c3", "diamondback century", \
        "dodge_charger police", "gazelle omafiets", "harley-davidson low_rider", \
        "jeep wrangler_rubicon", "kawasaki ninja", "lincoln mkz2017", "mercedes-benz coupe", \
        "mini cooperst", "mustang mustang", "nissan micra", "nissan patrol", "seat leon", \
        "tesla cybertruck", "tesla model3", "toyota prius", "volkswagen t2", "yamaha yzf"]
        self.setObjectName("AddVehicle")
        self.resize(492, 327)
        self.move(578, 300)

        #buttom box
        self.buttonBoxAdDia = QtWidgets.QDialogButtonBox(self)
        self.buttonBoxAdDia.setGeometry(QtCore.QRect(320, 290, 156, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.buttonBoxAdDia.setFont(font)
        self.buttonBoxAdDia.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxAdDia.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxAdDia.setObjectName("buttonBoxAdDia")

        #label for model
        self.ModAdDia = QtWidgets.QLabel(self)
        self.ModAdDia.setGeometry(QtCore.QRect(20, 6, 160, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.ModAdDia.setFont(font)
        self.ModAdDia.setObjectName("ModAdDia")

        #combo box for model
        self.cobBoxModAdDia = QtWidgets.QComboBox(self)
        self.cobBoxModAdDia.setGeometry(QtCore.QRect(300, 18, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxModAdDia.setFont(font)
        self.cobBoxModAdDia.setObjectName("cobBoxModAdDia")
        for i in range(27):
            self.cobBoxModAdDia.addItem("")
        
        #label for type 
        self.TypeAdDia = QtWidgets.QLabel(self)
        self.TypeAdDia.setGeometry(QtCore.QRect(20, 60, 56, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.TypeAdDia.setFont(font)
        self.TypeAdDia.setObjectName("TypeAdDia")

        #spin box for gap
        self.spinBoxGapAdDia = QtWidgets.QSpinBox(self)
        self.spinBoxGapAdDia.setGeometry(QtCore.QRect(420, 135, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.spinBoxGapAdDia.setFont(font)
        self.spinBoxGapAdDia.setObjectName("spinBoxGapAdDia")
        self.spinBoxGapAdDia.setValue(10)

        #label for gap
        self.GapAdDia = QtWidgets.QLabel(self)
        self.GapAdDia.setGeometry(QtCore.QRect(20, 115, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.GapAdDia.setFont(font)
        self.GapAdDia.setObjectName("GapAdDia")

        #combo box for type
        self.cobBoxTypeAdDia = QtWidgets.QComboBox(self)
        self.cobBoxTypeAdDia.setGeometry(QtCore.QRect(300, 70, 180, 30))
        self.cobBoxTypeAdDia.setObjectName("cobBoxTypeAdDia")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxTypeAdDia.setFont(font)
        self.cobBoxTypeAdDia.addItem("")
        self.cobBoxTypeAdDia.addItem("")
        self.cobBoxTypeAdDia.setCurrentIndex(1)

        #small label for color
        self.SLColorDia = QtWidgets.QLabel(self)
        self.SLColorDia.setGeometry(QtCore.QRect(20, 145, 180, 83))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLColorDia.setFont(font)
        self.SLColorDia.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SLColorDia.setObjectName("SLColorDia")

        #edit box for color R
        self.lineEditRDia = QtWidgets.QLineEdit(self)
        self.lineEditRDia.setGeometry(QtCore.QRect(80, 220, 60, 30))
        self.lineEditRDia.setObjectName("lineEditRDia")

        #small label for color R
        self.SLcolRDia = QtWidgets.QLabel(self)
        self.SLcolRDia.setGeometry(QtCore.QRect(40, 213, 47, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLcolRDia.setFont(font)
        self.SLcolRDia.setObjectName("SLcolRDia")

        #edit box for color G
        self.lineEditGDia = QtWidgets.QLineEdit(self)
        self.lineEditGDia.setGeometry(QtCore.QRect(250, 220, 60, 30))
        self.lineEditGDia.setObjectName("lineEditGDia")

        #small label for color G
        self.SLcolGDia = QtWidgets.QLabel(self)
        self.SLcolGDia.setGeometry(QtCore.QRect(220, 213, 47, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLcolGDia.setFont(font)
        self.SLcolGDia.setObjectName("SLcolGDia")
        
        #edit box for color B
        self.lineEditBDia = QtWidgets.QLineEdit(self)
        self.lineEditBDia.setGeometry(QtCore.QRect(420, 220, 60, 30))
        self.lineEditBDia.setObjectName("lineEditBDia")

        #small label for color B
        self.SLcolBDia = QtWidgets.QLabel(self)
        self.SLcolBDia.setGeometry(QtCore.QRect(390, 215, 47, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.SLcolBDia.setFont(font)
        self.SLcolBDia.setObjectName("SLcolBDia")

        self.retranslateUi()

        #default link for button box
        self.buttonBoxAdDia.accepted.connect(self.accept)
        self.buttonBoxAdDia.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AddVehicle", "Dialog"))
        self.ModAdDia.setText(_translate("AddVehicle", "Vehicle Model"))
        for i in range(27):
            self.cobBoxModAdDia.setItemText(i, _translate("AddVehicle", self.model_list[i]))
        self.SLColorDia.setText(_translate("Form", "Color"))
        self.SLcolRDia.setText(_translate("Form", "R:"))
        self.SLcolGDia.setText(_translate("Form", "G:"))
        self.SLcolBDia.setText(_translate("Form", "B:"))
        self.TypeAdDia.setText(_translate("AddVehicle", "Type"))
        self.GapAdDia.setText(_translate("AddVehicle", "Gap"))
        self.cobBoxTypeAdDia.setItemText(0, _translate("AddVehicle", "Ego"))
        self.cobBoxTypeAdDia.setItemText(1, _translate("AddVehicle", "Other"))


###error message dialogue###all error message dialogue page items have label end with [Err]
class Ui_ErrMes(QDialog):
    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(492,327)
        self.move(578, 300)

        #button box
        self.buttonBoxErr = QtWidgets.QDialogButtonBox(self)
        self.buttonBoxErr.setGeometry(QtCore.QRect(0, 285, 475, 32))
        self.buttonBoxErr.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxErr.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxErr.setObjectName("buttonBoxErr")

        #label for error message
        self.labelErr = QtWidgets.QLabel(self)
        self.labelErr.setGeometry(QtCore.QRect(0, 0, 492, 300))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.labelErr.setFont(font)
        self.labelErr.setAlignment(QtCore.Qt.AlignCenter)
        self.labelErr.setObjectName("labelErr")

        self.retranslateUi()
        self.buttonBoxErr.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelErr.setText(_translate("Dialog", "Error Message"))

###simulation dialogue###all simulation dialogue page items have label end with [SimDia]
class Ui_Simulation(QDialog):
    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(492, 327)
        self.move(578, 300)

        #button box
        self.buttonBoxSimDia = QtWidgets.QDialogButtonBox(self)
        self.buttonBoxSimDia.setGeometry(QtCore.QRect(320, 290, 156, 23))
        self.buttonBoxSimDia.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxSimDia.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxSimDia.setObjectName("buttonBoxSimDia")

        #big label for view
        self.BLViewSimDia = QtWidgets.QLabel(self)
        self.BLViewSimDia.setGeometry(QtCore.QRect(40, 10, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.BLViewSimDia.setFont(font)
        self.BLViewSimDia.setObjectName("BLViewSimDia")

        #combo box for view
        self.cobBoxViewSimDia = QtWidgets.QComboBox(self)
        self.cobBoxViewSimDia.setGeometry(QtCore.QRect(300, 20, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxViewSimDia.setFont(font)
        self.cobBoxViewSimDia.setObjectName("cobBoxViewSimDia")
        self.cobBoxViewSimDia.addItem("")
        self.cobBoxViewSimDia.addItem("")
        self.cobBoxViewSimDia.addItem("")

        #Big label for condition
        self.BLConSimDia = QtWidgets.QLabel(self)
        self.BLConSimDia.setGeometry(QtCore.QRect(40, 140, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.BLConSimDia.setFont(font)
        self.BLConSimDia.setObjectName("BLConSimDia")

        #combo box for condition
        self.cobBoxConSimDia = QtWidgets.QComboBox(self)
        self.cobBoxConSimDia.setGeometry(QtCore.QRect(300, 150, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.cobBoxConSimDia.setFont(font)
        self.cobBoxConSimDia.setObjectName("cobBoxConSimDia")
        self.cobBoxConSimDia.addItem("")
        self.cobBoxConSimDia.addItem("")

        self.retranslateUi()
        self.buttonBoxSimDia.accepted.connect(self.accept)
        self.buttonBoxSimDia.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BLViewSimDia.setText(_translate("Dialog", "View Type"))
        self.cobBoxViewSimDia.setItemText(0, _translate("Dialog", "First Person"))
        self.cobBoxViewSimDia.setItemText(1, _translate("Dialog", "Left"))
        self.cobBoxViewSimDia.setItemText(2, _translate("Dialog", "Human Driving"))
        self.BLConSimDia.setText(_translate("Dialog", "Control Type"))
        self.cobBoxConSimDia.setItemText(0, _translate("Dialog", "Drive automatically"))
        self.cobBoxConSimDia.setItemText(1, _translate("Dialog", "Drive manually"))

###penetrate dialogue###all simulation dialogue page items have label end with [PenDia]
class Ui_Penetrate(QDialog):
    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(492, 327)

        #button box
        self.buttonBoxPenDia = QtWidgets.QDialogButtonBox(self)
        self.buttonBoxPenDia.setGeometry(QtCore.QRect(320, 290, 156, 23))
        self.buttonBoxPenDia.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxPenDia.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxPenDia.setObjectName("buttonBoxPenDia")

        #big label for penetration distance
        self.BLPenDisDia = QtWidgets.QLabel(self)
        self.BLPenDisDia.setGeometry(QtCore.QRect(40, 120, 240, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.BLPenDisDia.setFont(font)
        self.BLPenDisDia.setObjectName("BLPenDisDia")

        #spin box for penetration distance
        self.spinBoxDisDia = QtWidgets.QSpinBox(self)
        self.spinBoxDisDia.setGeometry(QtCore.QRect(420, 130, 60, 20))
        self.spinBoxDisDia.setObjectName("spinBoxDisDia")
        self.spinBoxDisDia.setValue(5)

        self.retranslateUi()
        self.buttonBoxPenDia.accepted.connect(self.accept)
        self.buttonBoxPenDia.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BLPenDisDia.setText(_translate("Dialog", "Penetrate distance(m)"))