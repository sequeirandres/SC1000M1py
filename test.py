
import serial
import serial.tools.list_ports

try:
    jj = serial.Serial('COM5',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)       
    print(jj.name) 
    jj.write('hola')
    print('Conection OK !')
    jj.close()
except:
    print('No se pudo conectar')


