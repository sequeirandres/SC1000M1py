
import serial
import serial.tools.list_ports
from msj import*

class Comunication(object):
    def __init__(self, port, speed, bits, parity) -> None:
        self.port = port
        self.bits = bits
        self.speed = speed 
        self.parity = parity
        self.status = False
        self.StopBit = True

    def connect(self):
        if self.port:
            try:
                self.session=serial.Serial(self.port,baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)       
                print('Try to conection -> sussesfully ')
                self.status = True
            except:
                print('Try to conection -> Error')
        else:
            print('NOT PORT COM')

    def desconect(self):
        if self.session:
            try:
                self.session.close()
                print('Try to close conection -> sussesfully ')
            except:
                print('Try to close conection -> Error')
        else:
            print('No hay conexiones abiertas')    
        self.status = False

class Switch(object):
    def __init__(self, nswitch, channel):
        self.status = False
        self.switch = nswitch
        self.channel = channel

    def select(self,comRs232):
        print('Select -> SW-'+ str(self.switch)+ '  CH-'+str(self.channel) )
        cmdtosend = SCM_SEL_SWCH+str(self.switch)+'-'+str(self.channel)
        comRs232.write(cmdtosend.encode('UTF-8'))

    def power(self,comRs232):
        if self.status:
            print('SW power -> ON')
            comRs232.write(SCM_TURN_ON.encode('UTF-8'))
        else:
            print('SW power -> OFF')
            comRs232.write(SCM_TURN_OFF.encode('UTF-8'))
