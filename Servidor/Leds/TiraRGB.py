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


bNetejarTiraRGBDespresEvent=False


def InitTiraRGB():
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)
    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)
    # Set the PWM frequency to 60hz.
    pca.frequency = 60
    return pca

    
    
def parametresDefinir(parser):
    parser.add_argument('-a', '--animacio',  type=ascii, help='Tipus de animacio a representar. [pintar, creixer, decreixer]')
    parser.add_argument('-c', '--color',  type=ascii)
    parser.add_argument('-r', '--colorR',  metavar='N', type=int, help='vermell 1-256')
    parser.add_argument('-g', '--colorG',  metavar='N', type=int, help='verd 1-256')
    parser.add_argument('-b', '--colorB',  metavar='N', type=int, help='blau 1-256')
    parser.add_argument('-l', '--long',  metavar='N', type=int, help='longitud total de la animacio')
    parser.add_argument('-i', '--intensitat',  metavar='N', type=int, help='intensitat')
    parser.add_argument('-e', '--esborrar', action='store_true', help='borrar the display on exit')
    parser.add_argument('-t', '--tira', type=ascii, help='bloc de tires LED a la PCA9685 ')
    
    return parser

    
def ParametresLlegirTires(args):
    if  not args.tira:
        return (1,2,3,4,5,6)
    elif args.tira == "'T'":
        return (1,2,3,4,5,6)
    elif args.tira == "'2'":
        return (4,5,6)
    elif args.tira == "'1'":
        return (1,2,3)
    elif args.tira == "'16'":
        return (15)
    
    
def ParametresLlegirColorTiraRGB(args):
    if  args.color == "'R'":
        return Color(255, 0, 0)
    elif args.color == "'G'":
        return Color(0, 255, 0)	
    elif args.color == "'B'":
        return Color(0, 0, 255)	
    elif args.color == "'W'":
        return Color(255, 255, 255)	
    elif args.color == "'A'":  #aleatori
        return wheelColor(random.randrange(256))
        
    #un dels colors sempre tindrà valor 255. La intensitat la regulo per el seu propi indicador
    if args.colorR and args.colorG and args.colorB:
        return Color( args.colorR -1 , args.colorG - 1 , args.colorB - 1 )
        
    return Color(255, 255, 255)	
    

    
def netejarTiraRGB(pca, tires):
    #start_time = time.time()
    
    if isinstance(tires, int):
         #pwm1.set_pwm(tires, 0, 4096)  #OFF de la posició en concret
         pca.channels[tires].duty_cycle = 0
    else:
        for i in range(1,len(tires),3):
            pca.channels[tires[i-1]].duty_cycle = 0
            pca.channels[tires[i]].duty_cycle = 0
            pca.channels[tires[i+1]].duty_cycle = 0
    #print(time.time() - start_time)   

    
    
    
def pintarTiraRGB(pca,  tires, pColor, intensitat=255):

    for i in range(1,len(tires),3):
        pca.channels[tires[i-1]].duty_cycle = int(ObteVermellHex(pColor) * float(intensitat) / float(255))
        pca.channels[tires[i]].duty_cycle = int(ObteVerdHex(pColor) * float(intensitat) / float(255))
        pca.channels[tires[i+1]].duty_cycle = int(ObteBlauHex(pColor) * float(intensitat) / float(255))
    


def pintarTiraRGBTemps(pca,  tires, pColor, intensitat=255, temps=1000):

    pintarTiraRGB(pca,  tires, pColor, intensitat)
    
    if temps:
        time.sleep(temps/ 1000)    
        netejarTiraRGB(pca, tires)

    
    
def creixerTiraRGB(pca, tires, pColor, temps_total=5000, invers=False):

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
        
        for j in range(1,len(tires),3):
            pca.channels[tires[j-1]].duty_cycle = ObteVermellHex(color_pintar_actual)
            pca.channels[tires[j]].duty_cycle = ObteVerdHex(color_pintar_actual)
            pca.channels[tires[j+1]].duty_cycle = ObteBlauHex(color_pintar_actual)
        
        # la última iteració no cal fer el wait
        if i < 255:
            iteracio_time = time.time()
            periode_time=iteracio_time-start_time
            #print(periode_time, "periode time")
            #print(i)
            #print ((temps_iteracio * ((i+increment)/increment)) - periode_time - 0.001, "temps a esperar")
            time.sleep (max ( 0 , (temps_iteracio * ((i+increment)/increment)) - periode_time - 0.001))
     
     
    # ens assegurem que al final quedi al màxim o al mínim dels valors
    if invers: netejarTiraRGB(pca, tires)
    else:      pintarTiraRGB(pca, tires,pColor,255)
     
    #print(time.time() - start_time)    
    
    if bNetejarTiraRGBDespresEvent: netejarTiraRGB(pca, tires)
    
    

    
    
if __name__ == '__main__':

    pca = InitTiraRGB()
    
    
    
    args =  parametresDefinir(argparse.ArgumentParser()).parse_args()
    
    tires        =   ParametresLlegirTires(args)
    color_pintar =   ParametresLlegirColorTiraRGB(args)

    
    try:
    
    
        if args.animacio == "'creixer'":
            creixerTiraRGB(pca, tires, color_pintar, args.long)
        
        elif args.animacio == "'decreixer'":
            creixerTiraRGB(pca, tires, color_pintar, args.long, True)

        elif args.animacio == "'activar'" and args.tira and args.long:
            pca.channels[tires].duty_cycle = 65534
            time.sleep(args.long / 1000)
            
            # HI HA UNA SEGONA LLIBRERIA QUE ES FARIA AIXÍ
            #pwm1 = Adafruit_PCA9685.PCA9685()
            #CORRECTE pwm1.set_pwm(tires, 4096, 0)  #ON  FULL
            #pwm1.set_pwm(tires, 0, 4096)  #OFF FULL
            
            
        
        else: #args.animacio == "'pintar'":        
        
            if not args.intensitat:
                intensitatRGB=255
            else:
                intensitatRGB =  args.intensitat - 1

            pintarTiraRGBTemps(pca, tires, color_pintar, intensitatRGB, args.long)
            
            #if args.long:
            #    time.sleep(args.long / 1000)

    
    
    except KeyboardInterrupt:
        if args.esborrar:
            netejarTiraRGB(pca,tires)
			
    if args.esborrar:
        netejarTiraRGB(pca,tires)



