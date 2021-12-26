# sudo python3 xeviTiraRGB.py --colorR 100 --colorG 256 --colorB 25 --long 3000 --esborrar
# sudo python3 xeviTiraRGB.py --color A --long 3000 --esborrar
# sudo python3 xeviTiraRGB.py --color A --long 1000  --animacio pintar --intensitat 255
# sudo python3 xeviTiraRGB.py --color A --long 1000  --animacio creixer --esborrar
# sudo python3 xeviTiraRGB.py --color A --long 1000  --animacio decreixer 
# sudo python3 xeviTiraRGB.py --long 500  --animacio activar --tira 16 --esborrar


#https://circuitpython.readthedocs.io/projects/pca9685/en/latest/
#https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/blob/master/docs/index.rst

from board import SCL, SDA
import busio
import time
import random
from lib.funcions import *  
from rpi_ws281x import Color
import argparse

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

#ALERTA QUE HI HA UNA POSSIBLE SEGONA LLIBRERIA
#import Adafruit_PCA9685





class TiraObjecte:
    def __init__(self, pPca, pVermell,pVerd, pBlau, pBlanc = None):
        self.vermell = pVermell
        self.verd = pVerd
        self.blau = pBlau
        self.blanc = pBlanc
        self.pca = pPca

    def pintarVermell(self,pValor):
        if self.vermell is not None:   self.pca.channels[self.vermell].duty_cycle = pValor
    
    def pintarVerd(self,pValor):
        if self.verd is not None:      self.pca.channels[self.verd].duty_cycle    = pValor

    def pintarBlau(self,pValor):
        if self.blau is not None:      self.pca.channels[self.blau].duty_cycle    = pValor

    def pintarBlanc(self,pValor):
        if self.blanc is not None:     self.pca.channels[self.blanc].duty_cycle   = pValor

    def pintarRGB(self,pValorR,pValorG,pValorB):
        #Si tenim una tira que té el color blanc per separat, controlem els colors per mostrar el blanc separat i no pas la conjunció de RGB
        if int(pValorR) == int(pValorG) == int(pValorB) and self.blanc is not None: 
            self.pintarVermell(0)
            self.pintarVerd(0)
            self.pintarBlau(0)
            self.pintarBlanc(pValorR)
        else: 
            if self.blanc is not None:  self.pintarBlanc(0)
            self.pintarVermell(pValorR)
            self.pintarVerd(pValorG)
            self.pintarBlau(pValorB)


    def pintarRGBColorHexIntensitat(self,pColor,pIntensitat):
            self.pintarRGB(   int(  ObteVermellHex(pColor) * float(pIntensitat) / float(255)  )   ,
                              int(  ObteVerdHex(pColor)    * float(pIntensitat) / float(255)  )   ,
                              int(  ObteBlauHex(pColor)    * float(pIntensitat) / float(255)  )   )
        



#llista de tires led
lnkTires = []



def InitTiraRGB():
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)
    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)
    # Set the PWM frequency to 60hz.
    pca.frequency = 60
    
    lnkTires.append(  TiraObjecte(pca,1,2,3)   )    #RGB
    lnkTires.append(  TiraObjecte(pca,4,5,6,7)   )  #RGBW
    
    
    return pca

    
    
    
    
def pintarTiraRGB(tires, pColor, intensitat=255):

    if isinstance(tires, int):
        if tires < len(lnkTires): 
            lnkTires[tires].pintarRGBColorHexIntensitat(pColor, intensitat)
        else:
            print("ERROR: Aquesta tira no la tinc definida: " + str(tires));
    else:
        for i in tires:
            if i < len(lnkTires): 
                lnkTires[i].pintarRGBColorHexIntensitat(pColor, intensitat)
            else:
                print("ERROR: Aquesta tira no la tinc definida: " + str(i));
    


    
def netejarTiraRGB(tires):
    pintarTiraRGB(tires, Color(0, 0, 0) )



def pintarTiraRGBTemps(tires, pColor, intensitat=255, temps=1000):

    pintarTiraRGB(tires, pColor, intensitat)
    
    if temps:
        time.sleep(temps/ 1000)    
        netejarTiraRGB(tires)

    
    
def creixerTiraRGB(tires, pColor, temps_total=5000, invers=False):

    start_time = time.time()
    if not temps_total:
        temps_total=5000

    vermell = ObteVermell(pColor)
    verd = ObteVerd(pColor)
    blau = ObteBlau(pColor)
    
    
    increment=5
    
    temps_iteracio=(temps_total / 1000.0 / (255/increment))
    #print ("temps iteracio", temps_iteracio)
    
    for i in range(0,255,increment):
        if invers:
            vermell_actual = int((float(vermell)/float(255))*float(255-i))
            verd_Actual = int((float(verd)/float(255))*float(255-i))
            blau_Actual = int((float(blau)/float(255))*float(255-i))
            
        else:
            vermell_actual = int((float(vermell)/float(255))*float(i+1))
            verd_Actual = int((float(verd)/float(255))*float(i+1))
            blau_Actual = int((float(blau)/float(255))*float(i+1))

            
        color_pintar_actual = Color(vermell_actual,verd_Actual,blau_Actual)
        
        pintarTiraRGB(tires,color_pintar_actual)
        
        
        # la última iteració no cal fer el wait
        if i < 255:
            iteracio_time = time.time()
            periode_time=iteracio_time-start_time
            time.sleep (max ( 0 , (temps_iteracio * ((i+increment)/increment)) - periode_time - 0.001))
     
     
    # ens assegurem que al final quedi al màxim o al mínim dels valors
    if invers: netejarTiraRGB(tires)
    else:      pintarTiraRGB(tires,pColor,255)
     
    


#Només a mode demostració
def AccioDemo(tires):
    pintarTiraRGB( tires, Color(255, 0, 0) )
    time.sleep(1) 
    pintarTiraRGB( tires, Color(0, 255, 0) )
    time.sleep(1) 
    pintarTiraRGB( tires, Color(0, 0, 255) )
    time.sleep(1) 
    pintarTiraRGB( tires, Color(255, 255, 255) )
    time.sleep(3) 
    
    creixerTiraRGB( tires,Color(255, 255, 255)  )
    creixerTiraRGB( tires,Color(255, 0, 0)  )
    creixerTiraRGB( tires,Color(0, 255, 0)  )
    creixerTiraRGB( tires,Color(0, 0, 255)  )
    
    creixerTiraRGB( tires,Color(255, 255, 255)  ,True)
    creixerTiraRGB( tires,Color(255, 0, 0)  ,True)
    creixerTiraRGB( tires,Color(0, 255, 0)  ,True)
    creixerTiraRGB( tires,Color(0, 0, 255)  ,True)
    
    pintarTiraRGBTemps( tires, Color(255, 255, 255), 255, 1000)
    time.sleep(1) 
    pintarTiraRGBTemps( tires, Color(255, 0, 0), 255, 1000)
    time.sleep(1) 
    pintarTiraRGBTemps( tires, Color(0, 255, 0), 255, 1000)
    time.sleep(1) 
    pintarTiraRGBTemps( tires, Color(0, 0, 255), 255, 1000)
    time.sleep(1) 
    
    netejarTiraRGB([0,1])
    
if __name__ == '__main__':

    pca = InitTiraRGB()
    
    try:
        AccioDemo([0,1])
        AccioDemo(0)
        AccioDemo(1)
    except KeyboardInterrupt:
        netejarTiraRGB([0,1])
    finally:
        netejarTiraRGB([0,1])



