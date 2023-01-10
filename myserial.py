import serial
from serial.serialutil import to_bytes
import serial.tools.list_ports

BAND = 9600
DATABIT = 8
PARITY = 'N'
STOPBIT = 1

class serialconnection:
    def __init__(self):
        self.port = None
        self.port_list = list(serial.tools.list_ports.comports())
        self.output = " "

        if(len(self.port_list) == 0):
            print("Bağlantı kurulacak serial port bulunamadı!")
            self.output = "Bağlantı kurulacak serial port bulunamadı!"
        pass
    def getPortlist(self):
        return self.port_list

    def getOutput(self):
        return self.output

    def open_port(self,port):
        if self.port is not None:
            print(port + " bağlantınız bulunmaktadır.")
            self.output = port + " bağlantınız bulunmaktadır."

        else:
            self.port = serial.Serial(port,BAND,DATABIT,PARITY,STOPBIT)
            if self.port.is_open:
                print("Bağlantı Kuruldu")
                self.output = "Bağlantı Kuruldu"

    def send_data(self,data):
        if(self.port is not None):
            if self.port.is_open == False:
                print("Serial Port Bağlantısı Yok!")
                self.output = "Serial Port Bağlantısı Yok!"
            else:
                self.port.write(to_bytes(data)) 
                print(data)
                a = to_bytes(data)
                print(a)
        else:
            print("Lütfen port seçiniz!")
            self.output = "Lütfen port bağlantınızı seçin!"

            

    def close_port(self):
        if self.port != None and self.port.is_open != False:
            self.port.close()
            print("Bağlantı Koparıldı")
            self.output = "Bağlantı Koparıldı"
            self.port = None
        else:
            print("Bağlantınız bulunmamaktadır!")
            self.output = "Bağlantınız bulunmamaktadır!"
            

    
           
            
