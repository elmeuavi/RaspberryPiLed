#!/usr/bin/env python3
# EXEMPLE EXECUCIO:
#     sudo python3 xeviAnimacioLed.py --long 1000 --color R --esborrar --intensitat 64
#     sudo python3 xeviAnimacioLed.py --long 3000 --intensitat 58 --colorRini 155 --colorGini 200 --colorBini 1  --colorR 256 --colorG 1 --colorB 1 --esborrar
#     sudo python3 xeviAnimacioLed.py --long 3000 --intensitat 58 --colorRini 155 --colorGini 200 --colorBini 1  --colorR 256 --colorG 1 --colorB 1 --esborrar --pin 13
#
#     sudo python3 xeviAnimacioLed.py --animacio theaterChaseIteracions --wait_ms 200 --long 10 --subconjunt 3 --color A --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio theaterChaseTempsTotal --wait_ms 400 --long 5000 --subconjunt 3 --color A --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio rainbowIteracions --wait_ms 20 --long 5 --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio rainbowTempsTotal --wait_ms 20 --long 5000 --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio rainbowCycleIteracions --wait_ms 20 --long 5 --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio rainbowCycleTempsTotal --wait_ms 20 --long 5000 --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio theaterChaseRainbow --wait_ms 100  --long 5000 --esborrar 
#     sudo python3 xeviAnimacioLed.py --animacio creixer --color A --invers --long 3000 --esborrar
#     sudo python3 xeviAnimacioLed.py --animacio pintar --color A --long 3000 --intensitat 100 --esborrar
#     sudo python3 xeviAnimacioLed.py --animacio incrementalParts --wait_ms 40 --color A --long 2 --esborrar 

import time
from rpi_ws281x import PixelStrip, Color
import argparse

#import os
#os.system('echo ' +  str(time.time() - start_time) + ' > /tmp/hola.txt')

import random
#from parametres import *  
#from funcions import *  



#########################################################PARAMETRES ###############################################################################

# LED strip configuration:
LED_COUNT = 2*(30*5)        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


bNetejarTiraAdresablesDespresEvent=True




 
def parametresDefinir(parser):
    parser.add_argument('-a', '--animacio',  type=ascii, help='Tipus de animacio a representar. [vano, ]')
    parser.add_argument('-e', '--esborrar', action='store_true', help='borrar the display on exit')
    parser.add_argument('-l', '--long',  metavar='N', type=int, help='longitud total de la animacio')
    parser.add_argument('-w', '--wait_ms',  metavar='N', type=int, help='Milisegons entre un moviment i un altre')	
    parser.add_argument('-s', '--subconjunt',  metavar='N', type=int, help='leds en el subconjunt de la animacio')	
    parser.add_argument('-i', '--intensitat',  metavar='N', type=int, help='intensitat')
    parser.add_argument('-v', '--invers', action='store_true', help='Per al efecte creixer, de tot a res')

    parser.add_argument('-c', '--color',  type=ascii)
    parser.add_argument('-r', '--colorR',  metavar='N', type=int, help='vermell 1-256')
    parser.add_argument('-g', '--colorG',  metavar='N', type=int, help='verd 1-256')
    parser.add_argument('-b', '--colorB',  metavar='N', type=int, help='blau 1-256')

    parser.add_argument('-I', '--colorInicial',  type=ascii)
    parser.add_argument('-R', '--colorRini',  metavar='N', type=int, help='vermell inicial 1-256')
    parser.add_argument('-G', '--colorGini',  metavar='N', type=int, help='verd  inicial 1-256')
    parser.add_argument('-B', '--colorBini',  metavar='N', type=int, help='blau  inicial 1-256')

    parser.add_argument('-p', '--pin',  metavar='N', type=int, help='pin 18 (defecte, canal 0) o pin 13 (canal 1)')	
    
    
    
    return parser;
	
	
def ParametresLlegirPin(args):
    global LED_PIN,LED_CHANNEL
    if  args.pin == 13:
        return 13, 1 ;   # modifiquem el número de LED i el canal LED_PIN,LED_CHANNEL
    return LED_PIN,LED_CHANNEL;   # retornem el mateix pin i canal que ja teníem


    
def ParametresLlegirIntensitat(args, strip):
    if  args.intensitat:
        strip.setBrightness(int(args.intensitat)-1)

    
def ParametresLlegirColorInicial(args):

    if  args.colorInicial or  args.colorRini:
  
        if  args.colorInicial == "'R'":
            return Color(255,0,0);
        elif args.colorInicial == "'G'":
            return Color(0,255,0);
        elif args.colorInicial == "'B'":
            return Color(0,0,255);
        elif args.colorInicial == "'W'":
            return Color(255,255,255);

        if args.colorRini and args.colorGini and args.colorBini:
            return Color( args.colorRini -1 , args.colorGini - 1 , args.colorBini - 1 )
        

        
        
def ParametresLlegirColor(args):

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
        
    if args.colorR and args.colorG and args.colorB:
        return Color( args.colorR -1 , args.colorG - 1 , args.colorB - 1 )
        
    return Color(255, 255, 255)	


######################################################### FINAL PARAMETRES ###############################################################################






############################################### FUNCIONS GENÈRIQUES ########################################################



    
    

def wheelColor(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
    
        
        
def ObteVermell(pColor):
    return (pColor >> 16) & 0xff;

def ObteVerd(pColor):
    return (pColor >> 8) & 0xff;

def ObteBlau(pColor):
    return pColor & 0xff;   


def ObteVermellHex(pColor):
    return     int(           (float(ObteVermell(pColor))/float(0xFF))   *   float(0xFFFF)     )      

def ObteVerdHex(pColor):
    return     int(           (float(ObteVerd(pColor))/float(0xFF))   *   float(0xFFFF)     )      

def ObteBlauHex(pColor):
    return     int(           (float(ObteBlau(pColor))/float(0xFF))   *   float(0xFFFF)     )      
    
    
############################################### FINAL FUNCIONS GENÈRIQUES ########################################################





def netejar(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,  Color(0, 0, 0))
    strip.show()



def omplir(strip, color):
    if color:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,  color)
        strip.show()

        
def omplirTemps(strip,  color, temps=1000):

    omplir(strip, color)
    
    if temps:
        time.sleep(temps/ 1000)    
        netejar(strip)
        
        

def creixer(strip, temps_total=5000, invers=False):

    if not invers:
        invers=False

    if not temps_total:
        temps_total=5000

    """Wipe color across display a pixel at a time."""
    for i in range(0,255,2):
        if invers:
            strip.setBrightness(255-i-1)
        else:
            strip.setBrightness(i)
        strip.show()
        time.sleep((temps_total / 1000.0 / 128) - 0.001 )
                
    if bNetejarTiraAdresablesDespresEvent: netejar(strip)

    


	
#
# Vano amb temps total de l'animacio
#
def colorWipeTempsTotal(strip, color, temps_total=5000, subconjunt=2):
    """Wipe color across display a pixel at a time."""
    
    if not temps_total:
        temps_total=5000

    if not subconjunt:
        subconjunt=2

    #print ((temps_total / 1000.0 / strip.numPixels() )- 0.0007)
    #print ((temps_total / 1000.0 / (strip.numPixels()/subconjunt)) - 0.002)
    #start_time_tot = time.time()
    for i in range(  int(strip.numPixels()/subconjunt) ):
        #start_time = time.time()
        for j in range (subconjunt):
            strip.setPixelColor(i+ (int((strip.numPixels()/subconjunt)*j)), color)
        strip.show()
        #print("a dormir")
        #print((temps_total / 1000.0 / (strip.numPixels()/subconjunt)) - 0.002 )
        time.sleep((temps_total / 1000.0 / (strip.numPixels()/subconjunt)) - 0.002 )
    #print("--- %s seconds totals---" % (time.time() - start_time_tot))		
    
    if bNetejarTiraAdresablesDespresEvent: netejar(strip)

    
def theaterChaseIteracions(strip, color, wait_ms=50, iterations=10, pRang=3):
    """Movie theater light style chaser animation."""
    
    if not wait_ms:
        wait_ms=50

    if not iterations:
        iterations=10

    if not pRang:
        pRang=3

        
    rang = min(strip.numPixels(), pRang)
    
    for j in range(iterations):
        for q in range(rang):
            for i in range(0, strip.numPixels(), rang):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), rang):
                strip.setPixelColor(i + q, 0)

    
    if bNetejarTiraAdresablesDespresEvent: netejar(strip)
    
                
def theaterChaseTempsTotal(strip, color, wait_ms=50, temps_total=5000, pRang=3):
    """Movie theater light style chaser animation."""
    
    if not wait_ms:
        wait_ms=50

    if not temps_total:
        temps_total=5000

    if not pRang:
        pRang=3
    
    
    
    rang = min(strip.numPixels(), pRang)
    
    start_time = time.time()
    
    while True:
        for q in range(rang):
            for i in range(0, strip.numPixels(), rang):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), rang):
                strip.setPixelColor(i + q, 0)
        
        if (time.time() - start_time) > (float(temps_total - wait_ms)/1000):
            if bNetejarTiraAdresablesDespresEvent: netejar(strip)
            return;
    
    
    
            
def incremental(strip, color, wait_ms=5):
    
    if not wait_ms:
        wait_ms=5

    for j in range(strip.numPixels()):
        for i in range(strip.numPixels()-j):
            strip.setPixelColor(i, color)
            if i>0: strip.setPixelColor(i-1, Color(0,0,0))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            
    if bNetejarTiraAdresablesDespresEvent: netejar(strip)
    


def incrementalParts(strip, color, wait_ms=5, parts=1):
    
    if not wait_ms:
        wait_ms=5

    if not parts:
        parts=1

    for j in range(int(strip.numPixels()/parts)):
        for i in range(int(strip.numPixels()/parts)-j):
            for k in range(parts):
                strip.setPixelColor(int(k*int(strip.numPixels()/parts))+i, color)
                if i>0: strip.setPixelColor(int(k*int(strip.numPixels()/parts))+i-1, Color(0,0,0))

            strip.show()
            time.sleep(wait_ms / 1000.0)

    if bNetejarTiraAdresablesDespresEvent: netejar(strip)
    


def rainbowIteracions(strip, wait_ms=200, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    
    if not wait_ms:
        wait_ms=200

    if not iterations:
        iterations=1
        
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheelColor((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

    if bNetejarTiraAdresablesDespresEvent: netejar(strip)
    
    
        
        
def rainbowTempsTotal(strip, wait_ms=200, temps_total=5000):
    """Draw rainbow that fades across all pixels at once."""
    
    if not wait_ms:
        wait_ms=200

    if not temps_total:
        temps_total=5000
    
    start_time = time.time()
    while True:
        for j in range(256 ):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheelColor((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            if (time.time() - start_time) > (float(temps_total - wait_ms)/1000):
                if bNetejarTiraAdresablesDespresEvent: netejar(strip)
                return;
    
    
    
    

def rainbowCycleIteracions(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""

    if not wait_ms:
        wait_ms=20

    if not iterations:
        iterations=5

    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheelColor(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

    if bNetejarTiraAdresablesDespresEvent: netejar(strip)
    


def rainbowCycleTempsTotal(strip, wait_ms=20, temps_total=5000):
    """Draw rainbow that uniformly distributes itself across all pixels."""

    if not wait_ms:
        wait_ms=20

    if not temps_total:
        temps_total=5000

    start_time = time.time()
    while True:
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheelColor(
                    (int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)        
            if (time.time() - start_time) > (float(temps_total - wait_ms)/1000):
                if bNetejarTiraAdresablesDespresEvent: netejar(strip)
                return;

    
    
    

def theaterChaseRainbow(strip, wait_ms=50, temps_total=5000):
    """Rainbow movie theater light style chaser animation."""

    if not wait_ms:
        wait_ms=50

    if not temps_total:
        temps_total=5000

    start_time = time.time()
    while True:        
        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, wheelColor((i + j) % 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)
                if (time.time() - start_time) > (float(temps_total - wait_ms)/1000):
                    if bNetejarTiraAdresablesDespresEvent: netejar(strip)
                    return;

    




#
# Main program logic follows:
#
if __name__ == '__main__':

    #start_time_tot = time.time()


    args =  parametresDefinir(argparse.ArgumentParser()).parse_args()
    
    LED_PIN,LED_CHANNEL = ParametresLlegirPin(args)
    
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    
    ParametresLlegirIntensitat(args, strip)
    omplir(strip,    ParametresLlegirColorInicial(args)       )
    color_pintar =   ParametresLlegirColor(args)

    
    if args.esborrar: bNetejarTiraAdresablesDespresEvent=True

    
    try:
          
        if args.animacio == "'creixer'":
            #print ("animacio creixer")
            #sudo python3 xeviAnimacioLed.py --animacio creixer --color A --invers --long 3000 --esborrar
            #start_time = time.time()
            omplir(strip, color_pintar)
            creixer(strip, args.long,args.invers)
            #print(time.time() - start_time)
        
        elif args.animacio == "'pintar'":        
            #sudo python3 xeviAnimacioLed.py --animacio pintar --color A --long 3000 --esborrar
            omplirTemps(strip, color_pintar, args.long)
            #if args.long and args.esborrar:
            #    time.sleep((args.long / 1000.0)- 0.05)            
        
        
        #@Deprecated Utiltizar incrementalParts amb subconjunt 1
        elif args.animacio == "'incremental'":        
            #print ("animacio incremental")
            #sudo python3 xeviAnimacioLed.py --animacio incremental --wait_ms 200 --color A --esborrar 
            incremental(strip, color_pintar, args.wait_ms)            
        
        elif args.animacio == "'incrementalParts'":        
            #print ("animacio incrementalParts")
            #sudo python3 xeviAnimacioLed.py --animacio incrementalParts --wait_ms 40 --color A --long 2 --esborrar  
            incrementalParts(strip, color_pintar, args.wait_ms, args.subconjunt)            
        
        
        
        elif args.animacio == "'theaterChaseIteracions'":
            #print ("animacio theaterChaseIteracions")
            #sudo python3 xeviAnimacioLed.py --animacio theaterChaseIteracions --wait_ms 200 --long 10 --color A --esborrar 
            theaterChaseIteracions(strip, color_pintar, args.wait_ms, args.long)

        elif args.animacio == "'theaterChaseTempsTotal'":
            #print ("animacio theaterChaseTempsTotal")
            #sudo python3 xeviAnimacioLed.py --animacio theaterChaseTempsTotal --wait_ms 400 --long 5000 --subconjunt 3 --color A --esborrar 
            theaterChaseTempsTotal(strip, color_pintar, args.wait_ms, args.long, args.subconjunt)

            
            
            
        elif args.animacio == "'rainbowIteracions'":
            #print ("animacio rainbowIteracions")
            #sudo python3 xeviAnimacioLed.py --animacio rainbowIteracions --wait_ms 20 --long 5 --esborrar 
            rainbowIteracions(strip, args.wait_ms, args.long)

        elif args.animacio == "'rainbowTempsTotal'":
            #print ("animacio rainbowTempsTotal")
            #sudo python3 xeviAnimacioLed.py --animacio rainbowTempsTotal --wait_ms 20 --long 5000 --esborrar 
            rainbowTempsTotal(strip, args.wait_ms, args.long)

        elif args.animacio == "'rainbowCycleIteracions'":
            #print ("animacio rainbowCycleIteracions")
            #sudo python3 xeviAnimacioLed.py --animacio rainbowCycleIteracions --wait_ms 20 --long 5 --esborrar 
            rainbowCycleIteracions(strip,  args.wait_ms, args.long)

        elif args.animacio == "'rainbowCycleTempsTotal'":
            #print ("animacio rainbowCycleTempsTotal")
            #sudo python3 xeviAnimacioLed.py --animacio rainbowCycleTempsTotal --wait_ms 20 --long 5000 --esborrar 
            rainbowCycleTempsTotal(strip,  args.wait_ms, args.long)

        elif args.animacio == "'theaterChaseRainbow'":  
            #print ("animacio theaterChaseRainbow")
            #sudo python3 xeviAnimacioLed.py --animacio theaterChaseRainbow --wait_ms 100  --long 5000 --esborrar 
            theaterChaseRainbow(strip, args.wait_ms, args.long)
        
        
        
        
        else:
            #print("--- %s seconds fins al ventall---" % (time.time() - start_time_tot))		
            #start_time_tot = time.time()
            colorWipeTempsTotal(strip, color_pintar ,args.long, args.subconjunt)  
            #print("--- %s seconds totals---" % (time.time() - start_time_tot))		
            #start_time_tot = time.time()
            

    except KeyboardInterrupt:
        if args.esborrar:
            netejar(strip)
			
    #if args.esborrar:
    #    netejar(strip)
        
    #print("--- %s seconds a la sortida---" % (time.time() - start_time_tot))		
    #print(time.time())
