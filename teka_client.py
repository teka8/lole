from __future__ import print_function
import webbrowser
import requests
from playsound import playsound
import wave
import pyaudio
import time
import os
import cv2
from bs4 import BeautifulSoup
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pyttsx3
import pytz
from random import random
import pyautogui
import smtplib

from TekaUi import Ui_TekaUI
from PyQt5.QtGui import *
import pyttsx3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, QTimer
import sys
from PyQt5.QtCore import *




# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# server url
URL = "http://127.0.0.1:5000/predict"

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)


def speak(text):
    print("   ")
    print(f": {text}")
    engine.say(text)
    print("    ")
    engine.runAndWait()


#def wish():


    # speak("what can i help you")


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    # print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        playsound('minm evevt yelotim.wav')
    else:
        if len(events) == 1:
            playsound('zare and event.wav')
        elif len(events) == 2:
            playsound('zare hulet event.wav')
        elif len(events) == 3:
            playsound('3 event.wav')
        elif len(events) == 4:
            playsound('arat event.wav')
        elif len(events) == 5:
            playsound('amist event.wav')

        else:
            speak(f"you have {len(events)} events on this day")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time1 = str(int(start_time.split(":")[0]) - 12)
                mi = str(int(start_time.split(":")[1]))
                start_time = start_time1 + mi + "pm"

            speak(event["summary"] + " at " + start_time)
            print(event["summary"]+" " + start_time)
            time.sleep(3)


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('danielniguse7@gmail.com', 'danielNiguse12')
    server.sendmail('your email id', to, content)
    server.close()


def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=c68471b9f5c846d9950c418a56b298b8'
    main_page = requests.get(main_url).json()
    article = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in article:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


def launch_app(path_of_app):
    try:
        subprocess.call([path_of_app])
        return True
    except Exception as e:
        print(e)
        return False




class MainThread(QThread):

    def __init__(self):

        super(MainThread,self).__init__()

    def run(self):
        self.Task_Gui()

    def listening(self):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 8000  # Record at 44100 samples per second
        seconds = 3
        filename = "output.wav"

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording...')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Recognizing...')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    # the running part
    def Task_Gui(self):
        while True:
            self.listening()
            FILE_PATH = "output.wav"
            file = open(FILE_PATH, "rb")
            values = {"file": (FILE_PATH, file, "audio/wav")}
            response = requests.post(URL, files=values)
            data = response.json()
            if 'lole' in data["keyword"]:
                playsound('QR-[2021.08.25]-123103.wav')
                #speak("min lirdah?")
                self.listening()
                FILE_PATH = "output.wav"
                file = open(FILE_PATH, "rb")
                values = {"file": (FILE_PATH, file, "audio/wav")}
                response = requests.post(URL, files=values)
                data = response.json()


                if 'chrome kifet' in data["keyword"]:
                    print("ክሮም ክፈት")

                    url = "google.com"
                    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
                    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                    webbrowser.get('chrome').open_new_tab(url)

                elif 'musika kifet' in data["keyword"]:
                    print("ሙዚቃ ክፈት")
                    music_dir = "C:\\Users\\tesfa\\Desktop\\project\\amharic ai voice assistant\\music"
                    songs = os.listdir(music_dir)
                    for song in songs:
                        if song.endswith('.mp3'):
                            webbrowser.open(os.path.join(music_dir, song))

                elif 'camera kifet' in data["keyword"]:
                    print("ካሜራ ክፈት")
                    cam = cv2.VideoCapture(0)

                    cv2.namedWindow("test")

                    img_counter = 0

                    while True:
                        ret, frame = cam.read()
                        if not ret:
                            print("failed to grab frame")
                            break
                        cv2.imshow("test", frame)

                        k = cv2.waitKey(1)
                        if k % 256 == 27:
                            # ESC pressed
                            print("Escape hit, closing...")
                            break
                        elif k % 256 == 32:
                            # SPACE pressed
                            img_name = "opencv_frame_{}.png".format(img_counter)
                            cv2.imwrite(img_name, frame)
                            print("{} written!".format(img_name))
                            img_counter += 1

                    cam.release()

                elif 'video kifet' in data["keyword"]:
                    print("ቪድዮ ክፈት")
                    music_dir = "C:\\Users\\tesfa\\Videos"
                    songs = os.listdir(music_dir)
                    for song in songs:
                        if song.endswith('.mkv'):
                            webbrowser.open(os.path.join(music_dir, song))

                elif 'alarm mula' in data["keyword"]:
                    print("አላርም ሙላ")
                    #playsound('ebako seat yasgebu.wav')
                    #speak("enter the time !")
                    #time = input(": Enter the time :")

                    #while True:
                     #   Time_Ac = datetime.datetime.now()
                      #  now = Time_Ac.strftime("%H:%M:%S")

                       # if now == time:
                        #    #speak("time to wake up sir")
                         #   playsound('Lauren.mp3')
                          #  #speak("Alarm Closed!")
                        #elif now > time:
                         #   break

                elif 'photo ansa' in data["keyword"]:
                    print("ፎቶ አንሳ")
                    camera = cv2.VideoCapture(0)
                    for i in range(2):
                        return_value, image = camera.read()
                        cv2.imwrite('opencv' + str(i) + '.png', image)
                    del (camera)

                elif 'video kirets' in data["keyword"]:
                    print("ቪድዮ ቅረፅ")
                    # This will return video from the first webcam on your computer.
                    cap = cv2.VideoCapture(0)

                    # Define the codec and create VideoWriter object
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

                    # loop runs if capturing has been initialized.
                    while True:
                        # reads frames from a camera
                        # ret checks return at each frame
                        ret, frame = cap.read()

                        # Converts to HSV color space, OCV reads colors as BGR
                        # frame is converted to hsv
                        #    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                        # output the frame
                        out.write(frame)

                        # The original input frame is shown in the window
                        cv2.imshow('Original', frame)

                        # The window showing the operated video stream
                        # cv2.imshow('frame', hsv)

                        # Wait for 'a' key to stop the program
                        if cv2.waitKey(1) & 0xFF == ord('a'):
                            break

                    # Close the window / Release webcam
                    cap.release()

                    # After we release our webcam, we also release the output
                    out.release()

                    # De-allocate any associated memory usage
                    cv2.destroyAllWindows()

                elif 'zena asayegn' in data["keyword"]:
                    print("ዜና አሳየኝ")

                    url = "https://www.bbc.com/amharic"
                    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
                    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                    webbrowser.get('chrome').open_new_tab(url)




                elif 'ye ayer huneta asayegn' in data["keyword"]:
                    print("የአየር ሁኔታ አሳየኝ")
                    try:
                        ipAdd = requests.get('https://api.ipify.org').text
                        print(ipAdd)
                        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                        geo_requests = requests.get(url)
                        geo_data = geo_requests.json()
                        # print(geo_data)
                        city = geo_data['city']
                        search = f"temperature in {city}"
                        url = f"https://www.google.com/search?q={search}"
                        chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
                        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                        webbrowser.get('chrome').open_new_tab(url)

                    except Exception as e:
                        playsound('be network chigr.wav')



                elif 'event asayegn' in data["keyword"]:
                    print("ኢቨንት አሳየኝ")


                    service = authenticate_google()
                    day = datetime.date.today()
                    get_events(day, service)


                elif 'message lak' in data["keyword"]:
                    print("ሚሴጅ ላክ")
                    try:
                        to = input(": Enter the email address :")
                        playsound('ebako melikton yasgebu.wav')
                        #speak("what should i say?")
                        content = input(": Enter the message :")
                        sendEmail(to, content)
                        playsound('melikto telikuwal.wav')
                        #speak("email has been sent")

                    except Exception as e:
                        print(e)
                        playsound('yikirta melikton melak alchalkum.wav')
                        #speak("sorry sir, i am not able to sent this mail")

                elif 'computer ziga' in data["keyword"]:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

                elif 'screen ansa' in data["keyword"]:
                    import time

                    name = random()
                    playsound('esrino eyetenesa new.wav')
                    #speak("please sir hold the screen for few seconds, i am taking screenshot")
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(f"{name}.png")
                    playsound('tizazo tetenakwal.wav')
                    #speak("i am done sir")

                elif 'yet negn' in data["keyword"]:
                    playsound('tinish yitebiku bemefeleg lay negn.wav')
                    #speak("wait sir, let me check")
                    try:
                        ipAdd = requests.get('https://api.ipify.org').text
                        print(ipAdd)
                        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                        geo_requests = requests.get(url)
                        geo_data = geo_requests.json()
                        # print(geo_data)
                        city = geo_data['city']
                        # state = geo_data['state']
                        country = geo_data['country']
                        playsound('erso ahun yemigegnut be.wav')
                        speak(f"{city}")
                        playsound('ketema.wav')

                        speak(f"{country} ")
                    except Exception as e:
                        playsound('be network chigr.wav')
                        #speak("sorry sir, due to network issue i am not able to find where we are.")
                        pass

                else:
                    print(data["keyword"])

            else:
                print("...")
                print(" ")





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


        self.Teka_ui.movies_4 = QtGui.QMovie("initial.gif")
        self.Teka_ui.label_4.setMovie(self.Teka_ui.movies_4)
        self.Teka_ui.movies_4.start()



        startFunctions.start()

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()
        self.process.setFont(QFont('Arial', 20))
        self.process.setAlignment(Qt.AlignCenter)

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
        self.process.setLineWrapColumnOrWidth(250)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(300)
        self.process.setFixedHeight(100)
        self.process.move(420, 380)
        self.process.setStyleSheet("background-color: transparent; color: rgb(53, 252, 3); border: 1px solid black;")
        self.process.setAlignment(Qt.AlignCenter)

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
print("ሎሌ")
exit(Gui_App.exec_())

