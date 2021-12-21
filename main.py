import pyttsx3 as jarv
import datetime
import speech_recognition as sr
import pywhatkit as kit

engine = jarv.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
r = sr.Recognizer()

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
    speak("Do you need anything Sir ?")

def playMusic(audioMusic):
    kit.playonyt(audioMusic)

def voiceMusic():
 with sr.Microphone() as sourceMusic :
                speak("What type of music Sir ?")
                print("Recognizing song name...")
                r.pause_threshold = 1
                audioMusic = r.listen(sourceMusic)
                try :
                    queryMusic = str(r.recognize_google(audioMusic, language="en-UK"))
                    print(queryMusic)
                    playMusic(queryMusic)
                except Exception as e:
                    print(e)
                    speak("Couldn't hear the song name  Sir !")
                    voiceMusic()

def recog():

    with sr.Microphone() as source :
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try :
        print("Recognizing...")
        query = str(r.recognize_google(audio, language="en-UK"))
        print(query)
        if query.lower() == "what's today's date" or query.lower() == "what is today's date" :
            date()

        if query.lower() == "play music":
            voiceMusic()

        if query.lower() == "hello jarvis":
            morningGreeting()

    except Exception as e:
        print(e)
        speak("Couldn't understand what you meant Sir !")
        recog()

        return "None"
    return query

if __name__ == "__main__":
    recog()