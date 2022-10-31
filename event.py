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
            print(event["summary"])




service = authenticate_google()
day = datetime.date.today()
get_events(day, service)