import requests as rs
import xml.etree.ElementTree as xp
from tkinter import *
import calendar
import datetime
import os
window = Tk()
window.title("Weather App")
menu = Menu(window)
window.minsize(150,150)
window.maxsize(350,550)
location = StringVar()
type_det = StringVar()
checkbutton = IntVar()
def fetch_det_cur():
    day_name = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
    win = Tk()
    win.minsize(350,550)
    win.maxsize(350,550)
    win.title("Weather Report")
    api_key = <API_KEY>
    bgimg = ''
    day = ""
    cond = ""
    temp = ""
    l = ''
    humid = ""
    try:
        date = []
        pg = rs.get(f"http://api.weatherapi.com/v1/forecast.xml?key={api_key}&q={location.get()}")
        with open(r"OASIS_INTERN\WEATHER_APP\Weather.xml","wb") as f:
            f.write(pg.content)
            f.close()
        obj = xp.parse(r"OASIS_INTERN\WEATHER_APP\Weather.xml")
        obj = obj.getroot()
        obj= obj.findall('*')
        l = obj[0].find('name').text
        t = obj[0].find('localtime').text
        t = t.split(' ')
        time = t[1]
        time = [int(i) for i in time.split(':')]
        t_c = obj[1].find('temp_c').text
        t_f = obj[1].find('temp_f').text
        temp = t_c if(checkbutton.get()==1)else t_f
        humid = obj[1].find('humidity').text
        cond = obj[1].find('condition')
        cond = cond.find('text').text
        date = [int(i) for i in t[0].split('-')]
        day = day_name[(calendar.weekday(date[0],date[1],date[2]))]
        if(int(time[0])>=0 and int(time[0])<4):
            bgimg = r'OASIS_INTERN\WEATHER_APP\Day.png'
        elif(int(time[0])>=4 and int(time[0])<7):
            bgimg = r'OASIS_INTERN\WEATHER_APP\Morning.png'
        elif(int(time[0])>=7 and int(time[0])<17):
            bgimg = r'OASIS_INTERN\WEATHER_APP\Day.png'
        elif(int(time[0])>=17 and int(time[0])<=23):
            bgimg = r'OASIS_INTERN\WEATHER_APP\Night.png'
            
    except Exception as e :
        e_label = Label(window,text=e,font=('ariel',8))
        e_label.pack()
    b = PhotoImage(file=bgimg,master=win)
    canvas1 = Canvas(win,width=350,height=550)
    canvas1.pack(fill=BOTH,expand=True)
    canvas1.create_image(0,0,image = b,anchor = 'nw')
    canvas1.create_text(175,40,text=l,font=('Bell MT',18,'italic'))
    canvas1.create_text(175,60,text=cond,font=('Bell MT',14,'italic'))
    canvas1.create_text(65,400,text=f"  Day : {day}",font=('Bell MT',18,'italic'))
    canvas1.create_text(65,450,text=f"Temp : {temp}{chr(176)}",font=('Bell MT',18,'italic'))
    canvas1.create_text(65,500,text=f"Humid : {humid}",font=('Bell MT',18,'italic'))
    win.mainloop()

def fetch_det_fore(): 
    win = Tk()
    win.minsize(350,550)
    win.maxsize(350,550)
    win.title("Weather Report")
    api_key = "5b2174165cf64cf598e95646240402"
    l = ''
    bgimg = ''
    cond = ""
    temp = ""
    humid = ""
    attrib = []
    try:
        date = ''
        pg = rs.get(f"http://api.weatherapi.com/v1/forecast.xml?key={api_key}&q={location.get()}&days=3")
        with open(r"OASIS_INTERN\WEATHER_APP\Weather.xml","wb") as f:
            f.write(pg.content)
        obj = xp.parse(r"OASIS_INTERN\WEATHER_APP\Weather.xml")
        obj = obj.getroot()
        obj = obj.findall('*')
        t = obj[0].find('localtime').text
        t = t.split(' ')
        time = t[1]
        time = [int(i) for i in time.split(':')]
        l = obj[0].find('name').text
        for parent in obj[2].findall('*'):
            date = parent.find('date').text
            date = get_day(date)
            day_obj = parent.find('day')
            t_c = day_obj.find('avgtemp_c').text
            t_f = day_obj.find('avgtemp_f').text
            temp = t_c if(checkbutton.get()==1) else t_f
            humid = day_obj.find('avghumidity').text
            cond = day_obj.find('condition')
            cond = cond.find('text').text
            attrib.insert(len(attrib)-1,[date,temp,humid,cond])
        if(int(time[0])>=0 and int(time[0])<4):
            bgcolor = '#0f0f0f' #onix
            bgimg = r'OASIS_INTERN\WEATHER_APP\Night.png'
        elif(int(time[0])>=4 and int(time[0])<7):
            bgcolor = '#ffbf00' #Amber
            bgimg = r'OASIS_INTERN\WEATHER_APP\Morning.png'
        elif(int(time[0])>=7 and int(time[0])<17):
            bgcolor = 'fdee00' #Aureolin
            bgimg = r'OASIS_INTERN\WEATHER_APP\Day.png'
        elif(int(time[0])>=17 and int(time[0])<=23):
            bgcolor = "#100c08" #Smoky Black
            textcolor = '#fffafa'
            bgimg = r'OASIS_INTERN\WEATHER_APP\Night.png'
            
    except Exception as e :
        e_label = Label(window,text=e,font=('ariel',8))
        e_label.pack()
    b = PhotoImage(file=bgimg,master=win)
    canvas1 = Canvas(win,width=350,height=550)
    canvas1.pack(fill=BOTH,expand=True)
    canvas1.create_image(0,0,image = b,anchor = 'nw')
    canvas1.create_text(175,40,text=l,font=('Bell MT',18,'italic'))
    canvas1.create_text(175,100,text=f"{attrib[2][0]}",font=('Bell MT',18,'italic'))
    canvas1.create_text(175,120,text=attrib[2][3],font=('Bell MT',14,'italic'))
    
    canvas1.create_line(0,390,350,390)
    canvas1.create_text(175,410,text='Day-Wise Forecast',font=('Bell MT',14,'italic'))
    canvas1.create_line(0,430,350,430)

    canvas1.create_text(55,450,text=attrib[2][0],font=('Bell MT',12,'italic'))
    canvas1.create_text(55,470,text=f"Temp : {attrib[2][1]}{chr(176)}",font=('Bell MT',12,'italic'))
    canvas1.create_text(55,490,text=f"Humid : {attrib[2][2]}",font=('Bell MT',12,'italic'))
    canvas1.create_text(55,510,text=attrib[2][3],font=('Bell MT',12,'italic'))
    canvas1.create_line(110,430,110,550)

    canvas1.create_text(160,450,text=attrib[0][0],font=('Bell MT',12,'italic'))
    canvas1.create_text(160,470,text=f"Temp : {attrib[0][1]}{chr(176)}",font=('Bell MT',12,'italic'))
    canvas1.create_text(160,490,text=f"Humid : {attrib[0][2]}",font=('Bell MT',12,'italic'))
    canvas1.create_text(160,510,text=attrib[0][3],font=('Bell MT',12,'italic'))
    canvas1.create_line(220,430,220,550)

    canvas1.create_text(280,450,text=attrib[1][0],font=('Bell MT',12,'italic'))
    canvas1.create_text(280,470,text=f"Temp : {attrib[1][1]}{chr(176)}",font=('Bell MT',12,'italic'))
    canvas1.create_text(280,490,text=f"Humid : {attrib[1][2]}",font=('Bell MT',12,'italic'))
    canvas1.create_text(280,510,text=attrib[1][3],font=('Bell MT',12,'italic'))
    # canvas1.create_line(220,430,220,550)
    win.mainloop() 
def change_c():
    type_det.set('current')
    show_fields('current')

def change_f():
    type_det.set('forecast')
    show_fields('forecast') 
def show_fields(t):
    l_label = Label(window,text="Location",font=('Ariel',10,'bold'),background=bgcolor)
    l_entry = Entry(window,textvariable=location)
    unit = Label(window,text="Unit",font=('Ariel',10,'bold'),background=bgcolor)
    unit1 = Radiobutton(window,text="Celcius",variable=checkbutton,value=1,background=bgcolor)
    unit2 = Radiobutton(window,text="Fehrenheit",variable=checkbutton,value=2,background=bgcolor)
    if(t=='current'):
        s_button = Button(window,text="GO",font=('Times',10,'bold'),command=fetch_det_cur,background=bgcolor)
    else:
        s_button = Button(window,text="GO",font=('Times',10,'bold'),command=fetch_det_fore,background=bgcolor)
    unit.pack()
    unit1.pack()
    unit2.pack()
    l_label.pack()
    l_entry.pack()
    s_button.pack()
def get_day(date):
    date = str(date).split('-')
    day_name = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
    if('-'.join(date) == str(datetime.datetime.now().date())):
        return 'Today'
    elif(int(date[2])-int(str(datetime.datetime.now().date()).split('-')[2])==1):
        return 'Tomorrow'
    elif(int(date[2])-int(str(datetime.datetime.now().date()).split('-')[2])==2):
        return day_name[calendar.weekday(int(date[0]),int(date[1]),int(date[2]))]
    elif(int(date[2])-int(str(datetime.datetime.now().date()).split('-')[2])==3):
        return day_name[calendar.weekday(int(date[0]),int(date[1]),int(date[2]))]
    elif(int(date[2])-int(str(datetime.datetime.now().date()).split('-')[2])==4):
        return day_name[calendar.weekday(int(date[0]),int(date[1]),int(date[2]))]
    elif(int(date[2])-int(str(datetime.datetime.now().date()).split('-')[2])==5):
        return day_name[calendar.weekday(int(date[0]),int(date[1]),int(date[2]))]
    elif(int(date[2])-int(str(datetime.datetime.now().date()).split('-')[2])==6):
        return day_name[calendar.weekday(int(date[0]),int(date[1]),int(date[2]))]

bgcolor = "#f0f8ff"
dis_menu = Menu(menu,tearoff=0,background=bgcolor,)
menu.add_cascade(label="Type",menu=dis_menu,)
dis_menu.add_command(label="Current",command=change_c)
dis_menu.add_command(label="Forecast",command=change_f)
window.config(menu=menu,background=bgcolor)
window.mainloop()
os.remove(r"OASIS_INTERN\WEATHER_APP\Weather.xml")
