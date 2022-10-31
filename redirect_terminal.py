# -*- coding: utf-8 -*-
# @Time    : 2019/11/17 20:08
# @Author  : dailinqing
# @Email   : dailinqing@126.com
# @File    : print_to_ui.py
# @Software: PyCharm

import sys
import time
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, QTimer


class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class QMyWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

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

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def initUI(self):
        """Creates UI window on launch."""
        # Button for generating the master list.
        btn = QPushButton('Run', self)
        btn.move(450, 100)
        btn.resize(100, 100)
        btn.clicked.connect(self.OnBtnClicked)

        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(150)
        self.process.move(30, 100)

        # Set window size and title, then show the window.
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('print to ui')
        self.show()

    def OnBtnClicked(self):
        """Runs the main function."""

        print('Running...')
        self.timer.start(1000)
        # time.sleep (5) # time.sleep () is a blocking task that does not allow the Qt event loop to run, thereby preventing signals from working properly and GUI updates. The solution is to use QTimer and QEventLoop to replace the GUI sleep.
        print('Done.')


if __name__ == '__main__':
    # Run the application.
    app = QApplication(sys.argv)
    # app.aboutToQuit.connect(app.deleteLater)
    gui = QMyWindow()
    print("main")
    print("teka defar")
    sys.exit(app.exec_())