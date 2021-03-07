

from rpi_ws281x import Color
import random
from funcions import *  


# LED strip configuration:
LED_COUNT = 60        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53




 
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

    

