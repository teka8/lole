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







