from TekaUi import Ui_TekaUI
from PyQt5 import QtCore , QtWidgets , QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import pyttsx3

import sys



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate',170)


def Speak(Text):
    print("   ")
    print(f": {Text}")
    engine.say(Text)
    print("    ")
    engine.runAndWait()


class MainThread(QThread):

    def __init__(self): 

        super(MainThread,self).__init__()

    def run(self):
        self.Task_Gui()



    def Task_Gui(self):

        Speak("Hello Sir")
        Speak("Welcome Back Sir")


startFunctions = MainThread()

class Gui_Start(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Teka_ui = Ui_TekaUI()
        self.Teka_ui.setupUi(self)
        self.Teka_ui.pushButton.clicked.connect(self.startFunc)
        self.Teka_ui.pushButton_2.clicked.connect(self.close)

    def startFunc(self):

        self.Teka_ui.movies_2 = QtGui.QMovie("audio.gif")
        self.Teka_ui.label_2.setMovie(self.Teka_ui.movies_2)
        self.Teka_ui.movies_2.start()


        self.Teka_ui.movies_3 = QtGui.QMovie("__1.gif")
        self.Teka_ui.label_3.setMovie(self.Teka_ui.movies_3)
        self.Teka_ui.movies_3.start()

        self.Teka_ui.movies_4 = QtGui.QMovie("initial.gif")
        self.Teka_ui.label_4.setMovie(self.Teka_ui.movies_4)
        self.Teka_ui.movies_4.start()

        self.Teka_ui.movies_5 = QtGui.QMovie("Health_Template.gif")
        self.Teka_ui.label_5.setMovie(self.Teka_ui.movies_5)
        #self.Teka_ui.movies_5.start()


        self.Teka_ui.movies_6 = QtGui.QMovie("B.G_Template_1.gif")
        self.Teka_ui.label_6.setMovie(self.Teka_ui.movies_6)
        self.Teka_ui.movies_6.start()

        startFunctions.start()

Gui_App = QApplication(sys.argv)
Gui_Teka = Gui_Start()
Gui_Teka.show()
print("teka defar")
exit(Gui_App.exec_())