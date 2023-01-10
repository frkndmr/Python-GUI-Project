import tkinter as tk
from tkinter import *
from tkinter import ttk
import serial
import serial.tools.list_ports
from myserial import serialconnection

"""
HEX Command Data Set
ZOOM_WIDE  = [0xff,0x01,0x00,0x40,0x00,0x00,0x41]
STOP       = [0xff,0x01,0x00,0x00,0x00,0x00,0x01]
AUTO_FOCUS = [0xff,0x01,0x00,0x2b,0x00,0x00,0x2c]
ZOOM_TELE  = [0xff,0x01,0x00,0x20,0x00,0x00,0x21]
FOCUS_FAR  = [0xff,0x01,0x00,0x80,0x00,0x00,0x81]
FOCUS_NEAR = [0xff,0x01,0x01,0x00,0x00,0x00,0x02]
"""

PROCESS = ["   ZOOM WIDE","   ZOOM TELE","   FOCUS FAR","   FOCUS NEAR","   AUTO FOCUS","   STOP"]


class UserInterface:
    def __init__(self):
        self.port = None
        self.myConnect = None
        self.ReceDataView = " "
        self.LastProcess = " "

        #initialize interface
        self.window = tk.Tk()
        #self.window.iconbitmap('bilgem.ico')
        self.window.geometry("465x620")
        self.window.wm_title("KOWA LENS TEST YAZILIMI")
        self.window.configure(bg = "gray21")

        #Frame(external frame)
        self.frame_left = tk.Frame(self.window, width = 460, height = 600, bd = 4, bg = "gray21")
        self.frame_left.grid(row=0, column = 0)

        """self.frame_right = tk.Frame(self.window, width = 460, height = 580, bd = 4, bg = "gray21")
        self.frame_right.grid(row=0, column = 1)"""

        #Frame(internal frame)
        self.frame0 = tk.LabelFrame(self.frame_left, text = "Haberleşme Ayarı",foreground="white", width = 450, height = 180, bg = "gray21")
        self.frame0.grid(row=0, column = 0)
        self.frame1 = tk.LabelFrame(self.frame_left, text = "Arayüz Modu",foreground="white", width = 450, height = 80, bg = "gray21")
        self.frame1.grid(row=1, column = 0)
        self.frame2 = tk.LabelFrame(self.frame_left, text = "Lens Komutları",foreground="white", width = 450, height = 360, bg = "gray21")
        self.frame2.grid(row=2, column = 0)
        """self.frame2 = tk.LabelFrame(self.frame_right, text = "DSB",foreground="white", width = 450, height = 580, bg = "gray21")
        self.frame2.grid(row=1, column = 0)"""

        #Comport Selection screen background
        Frame(self.frame0,width=420,height=150,bg="white").place(x=14,y=5)

        #Comport Screen Contents
        self.l1 = Label(self.frame0, text="COM PORT :",bg="white")
        self.l1.config(font=("consolas",13))
        self.l1.place(x=100,y=25)
        self.myConnect = serialconnection()
        self.port_list = self.myConnect.getPortlist()

        self.l2 = Label(self.frame0, text="Bağlantı Durumu :",bg="white")
        self.l2.config(font=("consolas",13))
        self.l2.place(x=37,y=65)

        self.ReceDataView = tk.Text(self.window, width=30, height=1, font=("Times New Roman", 10)) 
        self.ReceDataView.place(x=206, y=90)  # display


        self.com_value = tk.StringVar()  
        self.combobox_port = ttk.Combobox(self.frame0, textvariable=self.com_value,width = 10,font = ("Times New Roman",13))
        self.combobox_port["value"] = self.port_list
        self.combobox_port.place(x = 200,y = 25)  

        Button(self.frame0,width=20,height=2,fg="white",bg="#994422",bd=0,text="BAĞLAN",command=self.sys_connect).place(x=60,y=110)
        Button(self.frame0,width=20,height=2,fg="white",bg="#994422",bd=0,text="BAĞLANTIYI KES",command=self.sys_disconnect).place(x=220,y=110)


        #Arayüz mod içerik
        self.l2 = Label(self.frame1, text="MOD :",bg="gray21", fg= "white")
        self.l2.config(font=("consolas",13))
        self.l2.place(x=40,y=15)

        self.mode_value = tk.StringVar()  
        self.combobox_mode = ttk.Combobox(self.frame1, textvariable=self.mode_value,width = 10,font = ("Times New Roman",13))
        self.combobox_mode["value"] = ["Standart Mod","Gelişmiş Mod"]
        self.combobox_mode.place(x = 100,y = 16)  

        Button(self.frame1,width=20,height=2,fg="white",bg="#994422",bd=0,text="UYGULA",command=self.sys_mode).place(x=250,y=11)


        #Lens Command Screen Contents
        self.button1 = Button(self.frame2,width=20,height=2,fg="#994422",bg="white",bd=0,text="ZOOM WIDE")

        self.button1.bind("<ButtonPress>",lambda event, a=0:self.on_press(a))
        self.button1.bind("<ButtonRelease>",lambda event, b=5: self.on_release(b))
        self.button2 = Button(self.frame2,width=20,height=2,fg="#994422",bg="white",bd=0,text="ZOOM TELE")
        self.button2.bind("<ButtonPress>",lambda event, a=1:self.on_press(a))
        self.button2.bind("<ButtonRelease>",lambda event, b=5: self.on_release(b))
        self.button3 = Button(self.frame2,width=20,height=2,fg="#994422",bg="white",bd=0,text="FOCUS FAR")
        self.button3.bind("<ButtonPress>",lambda event, a=2:self.on_press(a))
        self.button3.bind("<ButtonRelease>",lambda event, b=5: self.on_release(b))
        self.button4 = Button(self.frame2,width=20,height=2,fg="#994422",bg="white",bd=0,text="FOCUS NEAR")
        self.button4.bind("<ButtonPress>",lambda event, a=3:self.on_press(a))
        self.button4.bind("<ButtonRelease>",lambda event, b=5: self.on_release(b))
        self.button5 = Button(self.frame2,width=20,height=2,fg="#994422",bg="white",bd=0,text="AUTO FOCUS",command=lambda: self.write_data(4))
        
        self.button6 = Button(self.frame2,width=20,height=2,fg="white",bg="red",bd=0,text="STOP",command= lambda : self.write_data(5)) 
        

        """self.l3 = Label(self.frame2, text="KOMUT TİPİ :",bg="gray21",fg="white")
        self.l3.config(font=("consolas",11))
        
        self.command_value = tk.StringVar()  
        self.combobox_command = ttk.Combobox(self.frame2, textvariable=self.command_value,width = 10,font = ("Times New Roman",13))
        self.combobox_command["value"] = ["ZOOM","FOCUS"]

        self.l5 = Label(self.frame2, text="HIZ DEĞERİ :",bg="gray21",fg="white")
        self.l5.config(font=("consolas",11))
        Button(self.frame1,width=20,height=2,fg="white",bg="#994422",bd=0,text="UYGULA",command=self.sys_mode).place(x=250,y=11)
"""
        self.l4 = Label(self.frame2, text="Yapılan İşlem :",bg="gray21",fg="white")
        self.l4.config(font=("consolas",11))
        

        self.LastProcessView = tk.Text(self.frame2, width=20, height=1, font=("Times New Roman", 10)) 
        

    def sys_connect(self):
        self.port_str = self.combobox_port.get()                    #port name selected from the list is pulled
        self.parse_str = self.port_str.split(" ")                   #string is parsed
        self.port = self.parse_str[0]                               #The string in the first index is taken(COM1, COM2 etc.)
        self.myConnect.open_port(self.port)                         #The method is called to open the port
        self.readstr = self.myConnect.getOutput()                   #Information print out
        self.ReceDataView.delete("1.0","end")                       #The previously written output is deleted. 
        self.ReceDataView.insert(tk.INSERT, self.readstr)           #The new output is printed.

    def sys_disconnect(self):
        self.myConnect.close_port()                                 #The method is called to open the port
        self.readstr = self.myConnect.getOutput()                   #Information print out
        self.ReceDataView.delete("1.0","end")                       #The previously written output is deleted. 
        self.ReceDataView.insert(tk.INSERT, self.readstr)           #The new output is printed.
    
    def sys_mode(self):
        self.mode_str = self.combobox_mode.get()
        if self.mode_str == "Standart Mod":
            self.button1.place(x=60,y=60)
            self.button2.place(x=220,y=60)
            self.button3.place(x=60,y=120)
            self.button4.place(x=220,y=120)
            self.button5.place(x=60,y=180)
            self.button6.place(x=220,y=180)
            self.l4.place(x=75,y=300)
            self.LastProcessView.place(x=210, y=302)  # display

        #elif self.mode_str == "Gelişmiş Mod":

    def write_data(self,number):
        self.myConnect.send_data(self.choose_hex(number))          
        self.LastProcess = PROCESS[number]                         
        self.LastProcessView.delete("1.0","end")                    
        self.LastProcessView.insert(tk.INSERT, self.LastProcess)
        self.readstr = self.myConnect.getOutput()
        self.ReceDataView.delete("1.0","end")
        self.ReceDataView.insert(tk.INSERT, self.readstr)

    def show(self):
        self.window.mainloop()

    def on_press(self,num):
        self.write_data(num)
        
    def on_release(self,num):
        self.write_data(num)
    
    def choose_hex(self,argument):
        switcher = {
            0: [0xff,0x01,0x00,0x40,0x00,0x00,0x41],
            1: [0xff,0x01,0x00,0x20,0x00,0x00,0x21],
            2: [0xff,0x01,0x00,0x80,0x00,0x00,0x81],
            3: [0xff,0x01,0x01,0x00,0x00,0x00,0x02],
            4: [0xff,0x01,0x00,0x2b,0x00,0x00,0x2c],
            5: [0xff,0x01,0x00,0x00,0x00,0x00,0x01],
            6: [0xff,0x01,0x00,0x81,0x00,0x00,0x41],
        }
        return switcher.get(argument)

if __name__ == '__main__':
    my_ui = UserInterface()
    my_ui.show()