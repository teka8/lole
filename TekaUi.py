# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TekaUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TekaUI(object):
    def setupUi(self, TekaUI):
        TekaUI.setObjectName("TekaUI")
        TekaUI.resize(1074, 626)
        self.centralwidget = QtWidgets.QWidget(TekaUI)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-70, 0, 1231, 701))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Black_Template.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 0, 591, 371))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("audio.gif"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, -80, 300, 200))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("initial.gif"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 500, 100, 100))
        self.pushButton.setStyleSheet("background-color: rgb(103, 110, 103); color: rgb(0, 255, 255); border-radius : 50;\n"
"font: 18pt \"MS Shell Dlg 2\";  border : 3px solid rgb(0, 255, 255)")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 500, 100, 100))
        self.pushButton_2.setStyleSheet("background-color: rgb(103, 110, 103); color: rgb(252, 53, 3); border-radius : 50;\n"
"font: 18pt \"MS Shell Dlg 2\";   border : 3px solid rgb(252, 53, 3)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        #self.label_3.raise_()
        #self.label_5.raise_()
        #self.label_6.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        TekaUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(TekaUI)
        QtCore.QMetaObject.connectSlotsByName(TekaUI)

    def retranslateUi(self, TekaUI):
        _translate = QtCore.QCoreApplication.translate
        TekaUI.setWindowTitle(_translate("TekaUI", "MainWindow"))
        self.pushButton.setText(_translate("TekaUI", "ጀምር"))
        self.pushButton_2.setText(_translate("TekaUI", "ውጣ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TekaUI = QtWidgets.QMainWindow()
    ui = Ui_TekaUI()
    ui.setupUi(TekaUI)
    TekaUI.show()
    sys.exit(app.exec_())
