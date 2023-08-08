import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import random
import winreg as reg
import win32gui
import win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide, win32con.SW_HIDE)


print('Loading your AI personal assistant - Grey')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')

rate = engine.getProperty('rate')
print(rate)
engine.setProperty('rate', 160)

volume = engine.getProperty('volume')
hour = datetime.datetime.now().hour
if hour >= 0 and hour < 6:
    engine.setProperty('volume', 0.5)
else:
    engine.setProperty('volume', 1.0)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Hello,Good Morning , sir")
    elif hour >= 12 and hour < 18:
        speak("Hello,Good, Afternoon, sir")
    elif hour >= 0 and hour < 6:
        speak("Hello, Good night, sir")
    else:
        speak("Hello,Good Evening, sir")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        engine.runAndWait()

        try:
            statement = r.recognize_google(audio, language='en-EN')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Could you please say that again")
            return "None"
        return statement


speak("I am your personal assistant Gray")
wishMe()


if __name__ == '__main__':

    while True:
        speak("")
        statement = takeCommand().lower()
        if statement == 0:
            continue

        if "goodbye" in statement or "shutdown" in statement or "stop" in statement:
            speak('Im shutting down sir')
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif "weather" in statement:
            api_key = "4fd1ffcc86710872af1b1bc5a350c920"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Grey your personal asistant, you made me, dont you remember?')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            possible_results = [1, 2, 3, 4, 5, 6]
            sonuc = random.choice(possible_results)
            if sonuc == 1:
                speak('I dont know')
            elif sonuc == 2:
                speak('Zenkai made me, so i can help him')
            elif sonuc == 3:
                speak('I dont have any religous believe')
            elif sonuc == 4:
                speak('I told you i dont have any religous believe')
            elif sonuc == 5:
                speak('Zenkai made me, so i can help him')
            elif sonuc == 6:
                speak('Zenkai made me, so i can help him')

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'news' in statement:
            news = webbrowser.open_new_tab(
                "")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "close my pc" in statement or "sign out" in statement:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
        elif "I will go for a walk" in statement or "Go for sleep mode" in statement:
            speak("Ok, i will set your pc to sleep mode")
            os.system("shutdown.exe /h")
        elif "system off" in statement:
            speak("Ok, i will set your pc to sleep mode")
            os.system("shutdown /s /t 1")


time.sleep(3)
