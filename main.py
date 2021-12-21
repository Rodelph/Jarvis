import pyttsx3 as jarv
import datetime
import speech_recognition as sr

engine = jarv.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I Hours : %M Minutes : %S Seconds")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("" + str(day) + " " + str(month) + " " + str(year))

def morningGreeting():
    speak("Good morning sir !")
    speak("The current time is ")
    time()
    speak("and the current day is")
    date()
    speak("Do you need anything sir ?")


def recog():
    r = sr.Recognizer()
    with sr.Microphone() as source :
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try :
        print("Recognizing...")
        query = r.recognize_google(audio, language="fr-FR")
        if query == "date":
            date()

    except Exception as e:
        print(e)
        speak("Couldn't understand what you meant sir !")
        recog()

        return "None"
    return query

recog()