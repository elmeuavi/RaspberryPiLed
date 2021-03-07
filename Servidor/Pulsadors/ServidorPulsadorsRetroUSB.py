# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
PinCanal1 = 17
PinCanal2 = 27 
PinCanal3 = 22 
PinCanal4 = 23 
PinCanals=(PinCanal1,PinCanal2,PinCanal3,PinCanal4)
NomsCanals=("Canal 1","Canal 2","Canal 3","Canal 4")

NomBotons = ("INEXISTENT",  "Groc",          "Vermell",      "qwe",    
             "Negre",       "INEXISTENT",    "Blau",         "jkg",    
             "Verd",         "Pulsometre",   "INEXISTENT",   "vbbn", 
             "234",         "545",          "344",          "INEXISTENT")

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

EstatActualBotons= [False] * 12


def ObtenirIndex(i,j):
    return (i*3)+j+i

def InicialitzarPins():
    global PinCanals
    for x in PinCanals: 
        print("inicialitzant canal ",x)
        #GPIO.setup(x, GPIO.OUT) 
        #GPIO.output(x, GPIO.LOW)
        GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def  ComprobarButo(pOutput,pEntrada):

    if pOutput != pEntrada:  # and NomBotons[ObtenirIndex(pOutput,pEntrada)].find("Desassignat") == -1:
        
        print("Mirant Boto", NomBotons[ObtenirIndex(pOutput,pEntrada)], pOutput, pEntrada, ObtenirIndex(pOutput,pEntrada))
        
        if pOutput == 0: print("ara estem enviant per el canal 1", pEntrada)
        
        GPIO.setup(PinCanals[pOutput], GPIO.OUT) 
        GPIO.setup(PinCanals[pEntrada], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
        
        GPIO.output(PinCanals[pOutput], GPIO.LOW)
        time.sleep(1)
        if not GPIO.input(PinCanals[pEntrada]):
            print (GPIO.input(PinCanals[pEntrada]))
            print("El Boto ",NomBotons[ObtenirIndex(pOutput,pEntrada)],"-",pOutput,")",NomsCanals[pOutput],"-",PinCanals[pOutput],"-",pEntrada," contra ",NomsCanals[pEntrada],")",PinCanals[pEntrada]," esta APRETAT!!!")
        else:
            None
            #print("El Boto ",NomBotons[pOutput*3+pEntrada],"-",pOutput,")",NomsCanals[pOutput],"-",PinCanals[pOutput],"-",pEntrada," contra ",NomsCanals[pEntrada],")",PinCanals[pEntrada]," no esta esta apretat")
        #GPIO.output(PinCanals[pOutput], GPIO.LOW)
        GPIO.setup(PinCanals[pOutput], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up





    
#
# Main program logic follows:
#
if __name__ == '__main__':


    try:
        #inicialitzem tots a sortida i a zero
        InicialitzarPins()

        while True:
            for i in range(3):
                for j in range(3):
                    ComprobarButo(i,j) #
            time.sleep(1)


    #pwm.start(dc)
    #
    #print("Here we go! Press CTRL+C to exit")
    #
    #    while 1:
    #        if GPIO.input(butPin): # button is released
    #            pwm.ChangeDutyCycle(dc)
    #            GPIO.output(ledPin, GPIO.LOW)
    #        else: # button is pressed:
    #            pwm.ChangeDutyCycle(100-dc)
    #            
    #            time.sleep(0.075)
    #            GPIO.output(ledPin, GPIO.LOW)
    #            time.sleep(0.075)
    
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print("Sortim!! ")
    finally:
       GPIO.cleanup() # cleanup all GPIO 
