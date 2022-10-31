from TekaUi import Ui_TekaUI
from PyQt5.QtGui import *
import pyttsx3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, QTimer
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

    # the running part
    def Task_Gui(self):

        Speak("Hello Sir")
        Speak("Welcome Back Sir")


startFunctions = MainThread()


class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class Gui_Start(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Teka_ui = Ui_TekaUI()
        self.Teka_ui.setupUi(self)
        self.Teka_ui.pushButton.clicked.connect(self.startFunc)
        self.Teka_ui.pushButton_2.clicked.connect(self.close)

        self.initUI()

        # Note that this sentence can be printed to the console for easy debugging
        sys.stdout = Stream(newText=self.onUpdateText)

        # Initialize a timer
        self.timer = QTimer(self)
        # Connect the timer timeout signal to the slot function showTime ()
        self.timer.timeout.connect(self.fun)

        self.num = 0

    def fun(self):
        self.num += 2
        print(self.num)

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
        # self.Teka_ui.movies_5.start()

        self.Teka_ui.movies_6 = QtGui.QMovie("B.G_Template_1.gif")
        self.Teka_ui.label_6.setMovie(self.Teka_ui.movies_6)
        self.Teka_ui.movies_6.start()

        startFunctions.start()

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()
        self.process.setFont(QFont('Arial', 20))

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def initUI(self):
        """Creates UI window on launch."""
        # Button for generating the master list.
        # btn = QPushButton('Run', self)
        # btn.move(450, 100)
        # btn.resize(100, 100)
        # btn.clicked.connect(self.OnBtnClicked)

        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(150)
        self.process.move(640, 450)

        # Set window size and title, then show the window.
        self.setGeometry(100, 30, 1150, 700)
        self.setWindowTitle('amharic ai voice assistant')
        self.show()

    def OnBtnClicked(self):
        """Runs the main function."""

        print('Running...')
        self.timer.start(1000)
        # time.sleep (5) # time.sleep () is a blocking task that does not allow the Qt event loop to run, thereby preventing signals from working properly and GUI updates. The solution is to use QTimer and QEventLoop to replace the GUI sleep.
        print('Done.')


Gui_App = QApplication(sys.argv)
Gui_Teka = Gui_Start()
Gui_Teka.show()
print("teka defar")
exit(Gui_App.exec_())

