# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#
#  Title:  CONTROL-SWITCH-RF- TERMINAL TEST
#  Code :  scm.py  
#  Author: Sequeira Andres
#  gitHub: https://github.com/scm_sw_cnt.py
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from inc import suppress_qt_warnings
from modules import Comunication,Switch
from config import*
from msj import*

__author__ = 'sequera@andres'
__title__ = 'CNT_SW_RF_SC1000M1_RS32'

class scm(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi(SCR_UI,self)                      # Load RadarGuiApp  -- configurations --
        self.setWindowTitle(TITLTE_WND)             # Title of app
        self.setWindowIcon(QIcon(PATHFILE_LOGO))    # set Icon of app
        self.addPortCOM()                           # search and add Port-com 
        self.switch = Switch(0,0)                   # build swtich
        self.portcom = Comunication(COM_PORT,COM_SPEED,COM_BITS,COM_PARITY) 
        self.portcom.port = self.PortComRS.currentText()
        self.addActions()
        self.setUp()

    def addActions(self):
        self.ButtonConnect.clicked.connect(self.buttonConnect)
        self.ButtonOnOff.clicked.connect(self.buttonTurnOn)
        self.ButtonExit.clicked.connect(self.scmClose)
        self.ButtonSwtch1.clicked.connect(self.buttonA)
        self.ButtonSwtch2.clicked.connect(self.buttonB)
        self.ButtonSwtch3.clicked.connect(self.buttonC)
        self.ButtonSwtch4.clicked.connect(self.buttonD)
        self.SwitchSelect.currentTextChanged.connect(self.chooseSwitch)
        self.ButtonRefresh.clicked.connect(self.refresh)

    def setUp(self):  
        self.PortSpeed.setCurrentIndex(3)
        self.PortBits.setCurrentIndex(1)
        self.PortParity.setCurrentIndex(0)
        # Init all down
        self.BoxCnt.setEnabled(False)
        self.BoxSwitch.setEnabled(False)
        self.BoxChannel.setEnabled(False)
        
        if self.portcom.port:
            self.ButtonConnect.setEnabled(True)
            self.ButtonRefresh.setEnabled(False)
            self.terminal.setText(TERMINAL+'Init SCM')
        else:
            self.ButtonConnect.setEnabled(False)
            #self.PortSpeed.setEnabled(False)
            self.ButtonRefresh.setEnabled(True)
            self.terminal.setText(TERMINAL +'NO COM PORT')

    def refresh(self):
        self.addPortCOM()
        self.portcom.port = self.PortComRS.currentText()
        

        self.setUp()

    def buttonTurnOn(self):
        if self.switch.status !=True:
            self.switch.status = True
            self.ButtonOnOff.setText(MJE_ON)
            self.BoxSwitch.setEnabled(True)
            self.terminal.setText(TERMINAL+'SCM Turn ON')
        else:
            self.ButtonOnOff.setText(MJE_OFF)
            self.switch.status=False
            self.BoxSwitch.setEnabled(False)
            self.lcd_sw_x.display(0)
            self.lcd_sw_x_ch.display(0)
            self.SwitchSelect.setCurrentIndex(0)
            self.terminal.setText(TERMINAL+'SCM Turn OFF')
        self.switch.power(self.portcom.session)

    def buttonConnect(self):
        if self.portcom.status != True:
            self.ButtonConnect.setText(MJE_DCON)
            self.portcom.status = True
            self.BoxCnt.setEnabled(True)
            self.portcom.connect()
            self.PortComRS.setEnabled(False)
            self.PortSpeed.setEnabled(False)
            self.PortBits.setEnabled(False)
            self.PortParity.setEnabled(False)

        else:
            self.ButtonConnect.setText(MJE_CON)
            self.portcom.status = False
            self.BoxCnt.setEnabled(False)
            self.BoxSwitch.setEnabled(False)
            self.portcom.desconect()
            self.PortComRS.setEnabled(True)
            self.PortSpeed.setEnabled(True)
            self.PortBits.setEnabled(True)
            self.PortParity.setEnabled(True)

    def update(self):
        self.terminal.setText(TERMINAL +'Select  SW:'+ str(self.switch.switch)+ ' CH:' + str(self.switch.channel) )
        self.switch.select(self.portcom.session) 
        self.lcd_sw_x_ch.display(self.switch.channel)

    def buttonA(self):
        self.switch.channel = 1
        self.update()

    def buttonB(self):
        self.switch.channel = 2 
        self.update()

    def buttonC(self):
        self.switch.channel = 3 
        self.update()
      
    def buttonD(self):
        self.switch.channel = 4 
        self.update()
       
    def chooseSwitch(self):
        self.switch.switch = self.SwitchSelect.currentIndex()
        self.lcd_sw_x.display(self.switch.switch)
        if self.switch.switch !=0:
            self.BoxChannel.setEnabled(True)
        else:
            self.BoxChannel.setEnabled(False)
            self.switch.channel = 0                         # cierra el canal 
            self.lcd_sw_x_ch.display(self.switch.channel)

    def scmClose(self):
        # exit before close up comunication 
        if self.portcom.status:
            self.portcom.desconect()
        else:
            pass
        self.close()

    def PortConnect(self):
        print('Btn Conect COM-N')
        if (self.port_status==False): # try to connect to port COM A
            try:
                self.usb_serial_com = serial.Serial(self.PORT_CON.currentText(),baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
                self.Button_CON.setText('Desconectar')
                self.port_status=True
            except: print('No se pudo conectar al puerto COM')
        elif (self.port_status==True):
            print('Cerrar conexion')
        
        else:
            pass

    def addPortCOM(self):
        list_port_com = [comport.device for comport in serial.tools.list_ports.comports()]
        if list_port_com:
            self.PortComRS.addItems(list_port_com )
            #self.portcom.port = self.PortComRS.currentText() # puerto seleccionado
            #list_switch = ['None','SWTCH-01','SWTCH-02', 'SWTCH-03','SWTCH-04','SWTCH-05','SWTCH-06']
            self.SwitchSelect.addItems(LIST_OF_SWITCH) # list of port com 
            self.PortSpeed.addItems(COM_BAUD_RATE_ITEM)
            self.PortBits.addItems(COM_BIT_DATA)
            self.PortParity.addItems(COM_BIT_PARITY)
        else:
            pass

"scr.__main__"
if __name__ == "__main__":
    suppress_qt_warnings()
    scr_ = QApplication(sys.argv)
    module = scm()
    module.show()
    scr_.exec_()

