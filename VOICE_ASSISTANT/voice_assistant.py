import speech_recognition as sr 
import pyttsx3 as pt
import wikipedia as wiki
import datetime
import asyncio
import os
import requests as rs
import xml.etree.ElementTree as et
from newsapi import NewsApiClient
engine = pt.Engine("sapi5")
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,0.5)
        print("Listening...")
        audio = r.listen(source,timeout=10,phrase_time_limit=15)
        try:
            print("Recognizing...")
            u_text = r.recognize_google(audio,language="en-US")
            print(f"User has said this : {u_text}")
            return u_text
        except sr.WaitTimeoutError as e:
            speak("Say that again...")
        except Exception as e:
            speak("Pardon Sir... Please say that again !!")
            u_text = takecommand()
            return u_text
    
def speak(command):
    engine.say(command)
    engine.runAndWait()

def wish(state):
    t = int(datetime.datetime.now().hour)
    if(state == "last"):
        if(t>20 or (t>=0 and t<4)):
            speak("Good Night Sir!!")
        else:
            speak("Have a great day Sir !!")
    else:
        if(t>=0 and t<=3):
            speak("Its Mid Night Sir... You should go to sleep !!")
            cm = takecommand().lower()
            if(cm == "i don't want to"):
                speak("As your wish sir!!")
            else:
                return
        elif(t >= 4 and t<=11):
            speak("Good Morning Sir !! ")
        elif(t>11 and t<=16):
            speak("Good Afternoon Sir !!")
        elif(t==12):
            speak("Good Noon Sir !!")
        elif(t>16 and t<=22):
            speak("Good Night Sir !!")
def search_wiki(command):
    if(command == "search on wikipedia"):
        speak("Search about what sir !!")
        cm = takecommand().lower()
        cm = cm.replace("about","")
    print("Searching on Wikipedia..")
    command = command.replace("search on wikipedia","")
    res = wiki.summary(command,sentences=2)
    print(res)
    speak(res)
def tell_date():
    month = {"01":"January","02":"Februray","03":"March","04":"April","05":"May","06":"June","07":"July","08":"August","09":"September","10":"October","11":"November","12":"December"}
    t = str(datetime.datetime.now().date()).split("-")
    speak(f"Today is {t[2]} of {month[str(t[1])]} {t[0]}")
def tell_time():
    stand = ""
    t = str(datetime.datetime.now().time()).split(":")
    if(int(t[0])>=0 and int(t[0])<12):
        if(t[0][0]=="0"):
            t[0] = t[1:]
        stand = "AM"
    elif(int(t[0])==12):
        stand == "Noon"
    else:
        t[0] = str(int(t[0])-12)
        stand = "PM"
    speak(f"Its {t[0]} {t[1]} {stand}")
def weather(location):
    api_key = "5b2174165cf64cf598e95646240402"
    t_f = ''
    t_c = ''
    cond = ''
    humidity = ''
    try:
        xml = rs.get(f"http://api.weatherapi.com/v1/current.xml?key={api_key}&q={location}")
        with open(r"OASIS_INTERN\VOICE_ASSISTANT\weather.xml","wb") as f:
            f.write(xml.content)
        obj = et.parse(r"OASIS_INTERN\VOICE_ASSISTANT\weather.xml")
        obj = obj.getroot()
        obj = obj.findall('*')
        t_f = obj[1].find('temp_f').text
        t_c = obj[1].find('temp_c').text
        cond = obj[1].find('condition')
        cond = cond.find("text").text
        humidity = obj[1].find('humidity').text
        return (1,[location,t_c,t_f,cond,humidity])
    except Exception as e:
        return (0,e)
def news(topic):
    client = NewsApiClient(api_key="f41fe70709864ac6a63f532f01d8854c")
    con = client.get_everything(q=topic,page_size=5)
    for i in con["articles"]:
        title = i["title"]
        author = i["author"]
        speak(f"According to {author} {title}")
async def set_reminder(command):
    command = command.split(" ")
    ind_for = command.index("for")
    Time = int(command[ind_for+1])
    if(command[ind_for+2] == "minute"):
        Time = Time*60
    elif(command[ind_for+2] == "hours"):
        Time = Time*3600
    elif(command[ind_for+2] == "day"):
        Time = Time*24*3600          ##set a reminder for 10 seconds title greetings
    rem_name = command.index("title")
    title = command[rem_name+1:]
    speak(f"Reminder setted successfully")
    await asyncio.sleep(Time)
    print(f"Sir.. it is an reminder for {title}")
    speak(f"Sir.. it is an reminder for {title}")

async def call_rem(command):
    task = asyncio.create_task(set_reminder(command))
    return await main()
def search_file(path,file_name):
    found = False
    search_path = path
    files = os.listdir(search_path)
    if(file_name in files):
        for i in files:
            if(file_name in i):
                search_path += file_name
                found = True
            elif(file_name.capitalize() in i):
                search_path += file_name.capitalize()
                found = True
    else:
        for i in files:
            if("." not in i and not i.startswith("System")):
                search_path = f"{path}{i}/"
                try:
                    found,search_path = search_file(search_path,file_name)
                except Exception as e:
                    continue
                if(found):
                    break
    return (found,search_path)

async def main():
    while(True):
        cm = takecommand().lower()
        if("wikipedia" in cm):
            search_wiki(cm)
        elif("wish me" in cm):
            wish("not last")
        elif("date" in cm):
            tell_date()
        elif("time" in cm):
            tell_time()
        elif("reminder" in cm):
           state = await call_rem(cm)
           if(not state):
               break
        elif("sleep" in cm):
            cm = cm.split(" ")
            f_ind = cm.index("for")
            Time = int(cm[f_ind+1])
            speak(f"Sleeping for {Time} seconds")
            await asyncio.sleep(Time)

        elif("close" in cm and "assistant" in cm):
            speak("Closing the assistant")
            wish("last")
            return False
        elif("hello" in cm and "jarvis" in cm):
            speak("Ohh Hello Sir... How are you ?")
        elif("open" in cm):
            cm = cm.replace("open","")
            cm = cm.replace("dot",".")
            cm = cm.split(".")
            cm[0] = cm[0].rstrip()
            cm[1] = cm[1].lower().lstrip()
            cm = ".".join(cm)
            print(cm)
            f,p = search_file("C:/",cm.lstrip())
            if(f):
                os.startfile(p)
            else:
                f,p = search_file("D:/",cm)
                if(f):
                    os.startfile(p)
                else:
                    speak("Sorry Sir.. Specified file is not found !!")
        elif("weather" in cm):
            cm = cm.split('of')
            data = weather(cm[1])
            if(data[0]==0):
                print(f"{data[1]}")
            else:
                speak(f"The weather condition of {data[1][0]} are as follows")
                speak(f"Has a Temperature of {data[1][1]} degree celcius")
                speak(f"Has a humidity of {data[1][4]}")
                speak(f"The weather condition in {data[1][0]} is {data[1][3]}")
                speak(f"Any further query sir !!")
                c = takecommand().lower()
                if(c=="no"):
                    continue
                elif("fahrenheit" in c.split('in')[1].lower()):
                    speak(f"The temperature in Fahrenheit is {data[1][2]} degree fahrenheit")
                os.remove(r"OASIS_INTERN\VOICE_ASSISTANT\weather.xml")
        elif("news" in cm):
            cm = cm.split("about")
            news(cm[1])
        else:
            speak("No command found ..")
        cm = "" 
if __name__ == "__main__":
    asyncio.run(main())