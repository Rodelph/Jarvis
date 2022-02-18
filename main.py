import pyttsx3 as jarv
import datetime
import speech_recognition as sr
import pywhatkit as kit
import re
from bs4 import BeautifulSoup 
import requests
from pydub import AudioSegment
from pydub.playback import play
from extraPy.AudioAnalyzer import *
import random
import colorsys
from time import process_time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
engine = jarv.init()
r = sr.Recognizer()
Time = datetime.datetime.now()

def rnd_color():
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

def playInitMusic():
    start = process_time()
    filename = './music/init.wav'
    analyzer = AudioAnalyzer()
    analyzer.load(filename)
    pygame.init()
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w/2.2)
    screen_h = int(infoObject.current_w/2.2)
    screen = pygame.display.set_mode([screen_w, screen_h])
    t = pygame.time.get_ticks()
    getTicksLastFrame = t
    timeCount = 0
    avg_bass = 0
    bass_trigger = -40
    bass_trigger_started = 0
    min_decibel = -80
    max_decibel = 80
    circle_color = (40, 40, 40)
    polygon_default_color = [255, 255, 255]
    polygon_bass_color = polygon_default_color.copy()
    polygon_color_vel = [0, 0, 0]
    poly = []
    poly_color = polygon_default_color.copy()
    circleX = int(screen_w / 2)
    circleY = int(screen_h/2)
    min_radius = 100
    max_radius = 150
    radius = min_radius
    radius_vel = 0
    bass = {"start": 50, "stop": 100, "count": 12}
    heavy_area = {"start": 120, "stop": 250, "count": 40}
    low_mids = {"start": 251, "stop": 2000, "count": 50}
    high_mids = {"start": 2001, "stop": 6000, "count": 20}
    freq_groups = [bass, heavy_area, low_mids, high_mids]
    bars = []
    tmp_bars = []
    length = 0

    for group in freq_groups:
        g = []
        s = group["stop"] - group["start"]
        count = group["count"]
        reminder = s%count
        step = int(s/count)
        rng = group["start"]

        for i in range(count):
            arr = None
            if reminder > 0:
                reminder -= 1
                arr = np.arange(start=rng, stop=rng + step + 2)
                rng += step + 3
            else:
                arr = np.arange(start=rng, stop=rng + step + 1)
                rng += step + 2

            g.append(arr)
            length += 1
        tmp_bars.append(g)

    angle_dt = 360/length
    ang = 0

    for g in tmp_bars:
        gr = []
        for c in g:
            gr.append(
                RotatedAverageAudioBar(circleX+radius*math.cos(math.radians(ang - 90)), circleY+radius*math.sin(math.radians(ang - 90)), c, (255, 0, 255), angle=ang, width=8, max_height=370))
            ang += angle_dt

        bars.append(gr)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)

    running = True
    while running:
        avg_bass = 0
        poly = []
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t
        timeCount += deltaTime
        screen.fill(circle_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for b1 in bars:
            for b in b1:
                b.update_all(deltaTime, pygame.mixer.music.get_pos() / 1000.0, analyzer)

        for b in bars[0]:
            avg_bass += b.avg

        avg_bass /= len(bars[0])

        if avg_bass > bass_trigger:
            if bass_trigger_started == 0:
                bass_trigger_started = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - bass_trigger_started)/1000.0 > 2:
                polygon_bass_color = rnd_color()
                bass_trigger_started = 0
            if polygon_bass_color is None:
                polygon_bass_color = rnd_color()
            newr = min_radius + int(avg_bass * ((max_radius - min_radius) / (max_decibel - min_decibel)) + (max_radius - min_radius))
            radius_vel = (newr - radius) / 0.15
            polygon_color_vel = [(polygon_bass_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]

        elif radius > min_radius:
            bass_trigger_started = 0
            polygon_bass_color = None
            radius_vel = (min_radius - radius) / 0.15
            polygon_color_vel = [(polygon_default_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]

        else:
            bass_trigger_started = 0
            poly_color = polygon_default_color.copy()
            polygon_bass_color = None
            polygon_color_vel = [0, 0, 0]

            radius_vel = 0
            radius = min_radius

        radius += radius_vel * deltaTime

        for x in range(len(polygon_color_vel)):
            value = polygon_color_vel[x]*deltaTime + poly_color[x]
            poly_color[x] = value

        for b1 in bars:
            for b in b1:
                b.x, b.y = circleX+radius*math.cos(math.radians(b.angle - 90)), circleY+radius*math.sin(math.radians(b.angle - 90))
                b.update_rect()

                poly.append(b.rect.points[3])
                poly.append(b.rect.points[2])

        pygame.draw.polygon(screen, poly_color, poly)
        pygame.draw.circle(screen, circle_color, (circleX, circleY), int(radius))

        pygame.display.flip()
        if process_time() - start >= 8:
            break

    pygame.display.quit()
    pygame.quit()

def weatherVoice():
    with sr.Microphone() as sourceWeather: 
        print("Recognizing the city...")
        r.pause_threshold = 1
        audioWeather = r.listen(sourceWeather)

        try :
            queryWeather = str(r.recognize_google(audioWeather, language="en-UK"))
            print(queryWeather)
            speak("Searching for " + queryWeather + "'s weather !")
            weather(queryWeather + " weather")
        except Exception as e:
            print(e)
            speak("Couldn't hear the city name correctly, could please repeat ?")
            weatherVoice()

def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    speak("The weather in "+ location + " is " + info + "and the temperature is " + weather+"°C")

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

        if findWholeWord("weather")(query.lower()):
            weatherVoice()

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
    playInitMusic()
    greeting()
    while(True):
        recog()
