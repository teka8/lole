from __future__ import print_function
import webbrowser
import requests
from playsound import playsound
import wave
import pyaudio
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



SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# server url
URL = "http://127.0.0.1:5000/predict"

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)


def speak(text):
    engine.say(text)
    engine.runAndWait()


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
        speak('No upcoming events found.')
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

#to record audio file and save
def listening():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

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

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def launch_app(path_of_app):
    try:
        subprocess.call([path_of_app])
        return True
    except Exception as e:
        print(e)
        return False


def start():
    listening()
    FILE_PATH = "output.wav"
    file = open(FILE_PATH, "rb")
    values = {"file": (FILE_PATH, file, "audio/wav")}
    response = requests.post(URL, files=values)
    data = response.json()
    print("Predicted keyword: {}".format(data["keyword"]))
    if 'chrome kifet' in data["keyword"]:
        print("opning browser")
        url = "google.com"
        chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(url)

    elif 'musika kifet' in data["keyword"]:
        music_dir = "C:\\Users\\tesfa\\Desktop\\project\\amharic ai voice assistant\\music"
        songs = os.listdir(music_dir)
        for song in songs:
            if song.endswith('.mp3'):
                webbrowser.open(os.path.join(music_dir, song))

    elif 'camera kifet' in data["keyword"]:
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

    elif 'zena asayegn' in data["keyword"]:
        news()
    elif 'video kifet' in data["keyword"]:
        music_dir = "C:\\Users\\tesfa\\Videos"
        songs = os.listdir(music_dir)
        for song in songs:
            if song.endswith('.mp4'):
                webbrowser.open(os.path.join(music_dir, song))

    elif 'ye ayer huneta asayegn' in data["keyword"]:
        search = "temperature in adama"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"current {search} is {temp}")

    elif 'alarm mula' in data["keyword"]:
        speak("enter the time !")
        time = input(": Enter the time :")

        while True:
            Time_Ac = datetime.datetime.now()
            now = Time_Ac.strftime("%H:%M:%S")

            if now == time:
                speak("time to wake up sir")
                playsound('Lauren.mp3')
                speak("Alarm Closed!")
            elif now > time:
                break

    elif 'photo ansa' in data["keyword"]:
        camera = cv2.VideoCapture(0)
        for i in range(2):
            return_value, image = camera.read()
            cv2.imwrite('opencv' + str(i) + '.png', image)
        del (camera)

    elif 'video kirets' in data["keyword"]:
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

    elif 'event asayegn' in data["keyword"]:
        service = authenticate_google()
        day = datetime.date.today()
        get_events(day, service)

    elif 'message lak' in data["keyword"]:
        try:
            to = input(": Enter the email address :")
            speak("what should i say?")
            content = input(": Enter the message :")
            sendEmail(to, content)
            speak("email has been sent")

        except Exception as e:
            print(e)
            speak("sorry sir, i am not able to sent this mail")

    elif 'computer ziga' in data["keyword"]:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif 'screen ansa' in data["keyword"]:
        import time
        name = random()
        speak("please sir hold the screen for few seconds, i am taking screenshot")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        speak("i am done sir")

    elif 'yet new yalewit' in data["keyword"]:
        speak("wait sir, let me check")
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
            speak(f"sir i am not sure, but i think we are in {city} city of {country} country")
        except Exception as e:
            speak("sorry sir, due to network issue i am not able to find where we are.")
            pass


if __name__ == "__main__":
    start()
