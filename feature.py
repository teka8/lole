import pyttsx3
import smtplib


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('danielniguse7@gmail.com', 'danielNiguse12')
    server.sendmail('your email id', to, content)
    server.close()



try:
    to = input(": Enter the email address :")
    speak("what should i say?")
    content = input(": Enter the message :")
    sendEmail(to, content)
    speak("email has been sent")

except Exception as e:
    print(e)
    speak("sorry sir, i am not able to sent this mail")