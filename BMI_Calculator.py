import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import mysql.connector as sql
from tkinter import *
window = Tk()
menu = Menu(window)
window.geometry("500x300")
window.title("BMI CALCULATOR")
height_var = StringVar()
weight_var = StringVar()
user_name = StringVar()
pass_user = StringVar()
per_name = StringVar()
def database(type,b):
    p_name = per_name.get()
    found = False
    con = sql.connect(host="localhost",user=user_name.get(),password=pass_user.get(),database="bmi_calculator")
    c = con.cursor()
    c.execute("show tables;")
    tables = c.fetchall()
    for i in tables:
        if(p_name.lower() in i):
            found = True
    if(not found):
        c.execute(f"create table {p_name}(Height_in_m float(5),Weight_in_kg float(5),Bmi_Metric float(24),Height_in_Inch float(5),Weight_in_lbs float(5),Bmi_Imperial float(24));")
    if(type=='metric'):
        c.execute(f"insert into {p_name}(Height_in_m,Weight_in_kg,Bmi_Metric)values({height_var.get()},{weight_var.get()},{b})")
    else:
        c.execute(f"insert into {p_name}(Height_in_Inch,Weight_in_lbs,Bmi_Imperial)values({height_var.get()},{weight_var.get()},{b})")

    con.commit()
def history():
    con = sql.connect(host='localhost',user=user_name.get(),password=pass_user.get(),database='bmi_calculator')
    c = con.cursor()
    window_his = Tk()
    window_his.geometry("500x300")
    window_his.title("BMI HISTORY")
    table = Frame(window_his)
    table.pack()
    my_table = ttk.Treeview(table)
    my_table['columns'] = ('Height_in_m','Weight_in_kg','Bmi_Metric','Height_in_Inch','Weight_in_lbs','Bmi_Imperial')
    my_table.column("#0", width=0,  stretch=NO)
    my_table.column("Height_in_m",anchor=CENTER, width=80)
    my_table.column("Weight_in_kg",anchor=CENTER,width=80)
    my_table.column("Bmi_Metric",anchor=CENTER,width=80)
    my_table.column("Height_in_Inch",anchor=CENTER,width=80)
    my_table.column("Weight_in_lbs",anchor=CENTER,width=80)
    my_table.column("Bmi_Imperial",anchor=CENTER,width=80)
    my_table.heading("#0",text="",anchor=CENTER)
    my_table.heading("Height_in_m",text="Height(in m)",anchor=CENTER)
    my_table.heading("Weight_in_kg",text="Weight(in kg)",anchor=CENTER)
    my_table.heading("Bmi_Metric",text="BMI(in Metric)",anchor=CENTER)
    my_table.heading("Height_in_Inch",text="Height(in Inchs)",anchor=CENTER)
    my_table.heading("Weight_in_lbs",text="Weight(in lbs)",anchor=CENTER)
    my_table.heading("Bmi_Imperial",text="BMI(in Imperial)",anchor=CENTER)
    c.execute(f"select * from {per_name.get()};")
    values = c.fetchall()
    j=0
    x_met = []
    y_met = []
    x_imp = []
    y_imp = []
    for i in values:
        my_table.insert(parent='',index='end',iid=j,text='',values=i)
        j+=1

    my_table.pack()
    for i in values:
        if(i[0]!= None):
            x_met.append(i[0])
        if(i[3]!=None):
            x_imp.append(i[3])
        if(i[1]!=None):
            y_met.append(i[1])
        if(i[4]!=None):
            y_imp.append(i[4])
    plt.plot(x_met,y_met)
    plt.show()
    plt.plot(x_imp,y_imp)
    plt.show()
    window_his.mainloop()
    
def calculate_imperial():
    height = float(height_var.get())
    weight = float(weight_var.get())
    bmi = 703*(weight/(height*height))
    res = Label(window,text= f"BMI : {bmi}",font=('algeian',10))
    res.grid(row=8,column=1)
    database('imperial',bmi)
    condition(bmi)
def calculate_metric():    
    height = float(height_var.get())
    weight = float(weight_var.get())
    bm = weight/(height*height)
    res = Label(window,text= f"BMI : {bm}",font=('algeian',10))
    res.grid(row=8,column=1)
    database('metric',bm)
    condition(bm)
    
def metric():    
    l = Label(window,text="Person Info",font=('algerian',10,'bold'))
    height_label = Label(window,text="Height(in m)",font=('ariel',10,'bold'))
    height_val = Entry(window,textvariable= height_var)
    weight_label = Label(window,text="Weight(in kg)",font=('ariel',10,'bold'))
    weight_val = Entry(window,textvariable= weight_var)
    submit_button = Button(window,text="Calculate",command=calculate_metric,font=('ariel',10,'bold'))
    l.grid(row=4,column=1)
    height_label.grid(row=5,column=0)
    height_val.grid(row=5,column=1)
    weight_label.grid(row=6,column=0)
    weight_val.grid(row=6,column=1)
    submit_button.grid(row=7,column=1)

def imperial():
    l = Label(window,text="Person Info",font=('algerian',10,'bold'))
    height_label = Label(window,text="Height(in in)",font=('ariel',10,'bold'))
    height_val = Entry(window,textvariable= height_var)
    weight_label = Label(window,text="Weight(in lbs)",font=('ariel',10,'bold'))
    weight_val = Entry(window,textvariable= weight_var)
    submit_button = Button(window,text="Calculate",command=calculate_imperial,font=('ariel',10,'bold'))
    l.grid(row=4,column=1)
    height_label.grid(row=5,column=0)
    height_val.grid(row=5,column=1)
    weight_label.grid(row=6,column=0)
    weight_val.grid(row=6,column=1)
    submit_button.grid(row=7,column=1)

def condition(b):
    state = ""
    if(b < 15):
        state = "Very severly underweight"
    elif(b>=15 and b<16):
        state = "Severly underweight"
    elif(b>=16 and b<18.5):
        state = "Underweight"
    elif(b>=18.5 and b<25):
        state = "Nomal (healthy weight)"
    elif(b>=25 and b<30):
        state = "Overweight"
    elif(b>=30 and b<35):
        state = "Moderately obese"
    elif(b>=35 and b<40):
        state = "Severly obese"
    elif(b>=40):
        state = "Very severly obese"
    
    con_label = Label(window,text=state,font=('algerian',10,'bold'))
    con_label.grid(row=9,column=1)


d_label = Label(window,text="Database Info",font=('algerian',10,'bold'))
user_label = Label(window,text="User Name",font=('ariel',10,'bold'))
pass_label = Label(window,text="Password",font=('ariel',10,'bold'))
user_val = Entry(window,textvariable=user_name)
pass_val = Entry(window,textvariable=pass_user,show="*")
per_label = Label(window,text="Person Name",font=('ariel',10,'bold'))
per_val = Entry(window,textvariable=per_name)
dis_menu = Menu(menu,tearoff=0)
menu.add_cascade(label= "Select Type",menu=dis_menu,font=('areial',10,'bold'))
dis_menu.add_command(label="Imperial",command=imperial)
dis_menu.add_command(label="Metric",command=metric)
his_button = Button(window,text="Show History",command=history,font=('areial',10,'bold'))
user_label.grid(row=1,column=0)
user_val.grid(row=1,column=1)
pass_label.grid(row=2,column=0)
pass_val.grid(row=2,column=1)
per_label.grid(row=3,column=0)
per_val.grid(row=3,column=1)
d_label.grid(row=0,column=1)
his_button.grid(row=10,column=1)
window.config(menu=menu)
window.mainloop()