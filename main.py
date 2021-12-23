import pyttsx3 as jarv
import datetime
import speech_recognition as sr
import pywhatkit as kit
import re

engine = jarv.init()
r = sr.Recognizer()
Time = datetime.datetime.now()

def searchGoogle(querySearch):
    kit.search(querySearch)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I Hours : %M Minutes : %S Seconds")
    speak("It is currently " + str(Time))

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("" + str(day) + " " + str(month) + " " + str(year))

def greeting():
    speak("Good morning sir ! What can i do for you ?")

def greetingBack():
    speak("Greetings sir you seem cheerful today !")

def voiceMusic():
    with sr.Microphone() as sourceMusic :
        print("Recognizing song name...")
        r.pause_threshold = 1
        audioMusic = r.listen(sourceMusic)

        try :
            queryMusic = str(r.recognize_google(audioMusic, language="en-UK"))
            print(queryMusic)
            speak("Playing " + queryMusic + " !")
            kit.playonyt(queryMusic)
        except Exception as e:
            print(e)
            speak("Couldn't hear the song name  Sir ! Could you repeat again ?")
            voiceMusic()


def sendMessageWtsp():
    minute = Time.minute + 1
    kit.sendwhatmsg("",
                    "Hello",
                    Time.hour, minute,
                    tab_close=True)

def searchVoice():
    with sr.Microphone() as sourceSearch :
        print("Listening...")
        
        r.pause_threshold = 1
        audioSearch = r.listen(sourceSearch)

        try:
            querySearch= str(r.recognize_google(audioSearch, language="en-UK"))
            print(querySearch)
            speak("Searching for " + querySearch + " !")
            searchGoogle(querySearch)
        except Exception as e:
            print(e)
            speak("Couldn't understand what you meant Sir ! Could you repeat again ?")
            searchVoice()

def recog():
    with sr.Microphone() as source :
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try :
        print("Recognizing...")
        query = str(r.recognize_google(audio, language="en-UK"))
        print(query)
        
        if findWholeWord("date")(query.lower()):
            date()

        if findWholeWord("music")(query.lower()):
            speak("What type of music Sir ?")
            voiceMusic()

        if findWholeWord("time")(query.lower()) :
            time()

        if findWholeWord("hello")(query.lower()):
            greetingBack()

        if findWholeWord("search")(query.lower()):
            speak("What are you looking for Sir ?")
            searchVoice()

        if  findWholeWord("message")(query.lower()):
            sendMessageWtsp()

    except Exception as e:
        print(e)
        speak("Couldn't understand what you meant Sir !")
        recog()

        return "None"
    return query

if __name__ == "__main__":
    greeting()
    while(True):
        recog()