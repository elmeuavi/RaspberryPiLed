#PER INICIAR EL SERVIDOR TCP/IP
#sudo python3 servidor.py

#PER ATACAR EL SERVIDOR VIA SHELL
#exec 3<>/dev/tcp/hostname/port
#echo "request" 1>&3
#response="$(cat <&3)"
#TANCAR LA CONNEXIO:
#exec 3<&-

#PER ATACAR EL SERVIDOR VIA COMPADA WINDOWS
#curl -H "Host:" -H "User-Agent:" -H "Accept:" -H "Content-Length:" -H "Content-Type:" -d "hola" -X POST --max-time 0,1 192.168.1.144:10000  


#PER ATACAR EL SERVIDOR VIA PYTHON
#import socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (sys.argv[1], 10000)
#sock.connect(server_address)
#sock.sendall(bytearray('|color A|theaterChaseIteracions 200 10', 'utf-8'))


import socket
import sys

from AnimacioLed import *
from TiraRGB import *
from multiprocessing import Process  #, Value, Array

import traceback

debug=False


class args:
    color = "'W'"
    colorR = ''
    colorB = ''
    colorG = ''
    intensitat = 0
    pin = 18


if __name__ == '__main__':
    COLOR_LEDS=Color(255, 255, 255)
    TIRES=(0,1,2,3,4,5)
        
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    pca = InitTiraRGB() # de xeviTiraRGB.py
        

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 10000)
    sock.bind(server_address)
    if debug: print  ('starting up on ' , sock.getsockname())
    sock.listen(1)

    
    while True:
        print  ('Waiting for a new connection')
        connection, client_address = sock.accept()
        try:
            if debug: print  ('client connected:', client_address)
            while True:

                try:
                    data = connection.recv(65535).decode("utf-8") 
                except:
                    print("Error amb la connexio mentre esperavem noves instruccions")
                    #traceback.print_exc(file=sys.stdout)
                    data = ""
                    
                if data:
                    llista_linies_comandes=data.split("|")
                    for linia_comanda in llista_linies_comandes:
                        if linia_comanda:
                            
                            if len(linia_comanda) > 0 :  print  ('Comanda rebuda: %s ' % linia_comanda.replace('\n', ''))
                            
                            #Retornar al client la mateixa informació (no ho fem)
                            #if debug: connection.sendall(bytearray(linia_comanda, 'utf-8'))
                            comanda = linia_comanda.split()


                            
                            ######################################################################################################
                            #           CONFIGURACIONS
                            ######################################################################################################
                            if comanda[0] == "color":  #R G B W-White A-aleatori
                                args.color="'"+comanda[1]+"'"
                                COLOR_LEDS=ParametresLlegirColor(args)

                            elif comanda[0] == "colorRGB":  #0-255
                                args.colorR=int(comanda[1])+1
                                args.colorG=int(comanda[2])+1
                                args.colorB=int(comanda[3])+1
                                args.color=''
                                COLOR_LEDS=ParametresLlegirColor(args)

                                
                            elif comanda[0] == "intensitat":  #0-255
                                args.intensitat=int(comanda[1])+1
                                ParametresLlegirIntensitat(args,strip) # definir la intensitat per la tira de leds adressables 1-256
                                
                                args.intensitat=int(comanda[1]) # definir la intensitat per la tira de leds NO adressables 0-255

                            elif comanda[0] == "PIN":  #pin de la raspberry on esta conectada la tira de leds addressables
                                args.pin=int(comanda[1])
                                LED_PIN,LED_CHANNEL = ParametresLlegirPin(args)
                                
                                #reinicialitzem la tira de leds amb el nou pin
                                strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
                                strip.begin()

                            elif comanda[0] == "NetejarDespresEvent":
                                bNetejarTiraRGBDespresEvent=True
                                bNetejarTiraAdresablesDespresEvent=True
                            elif comanda[0] == "NoNetejarDespresEvent":
                                bNetejarTiraRGBDespresEvent=False
                                bNetejarTiraAdresablesDespresEvent=False
                                
                                
                                
                                
                            ######################################################################################################
                            #           TOT OBERT / TOT TANCAT
                            ######################################################################################################                            
                            #obrim tires de leds adressables a color blanc i intensitat 255
                            #obrim 2 tires de leds canal 0-2 i 3-5 de protocol I2C a color blanc i intensitat 255
                            #obrim canal 15 de protocol I2C
                            elif comanda[0] == "PanicBlanc":
                                args.color="'W'"
                                COLOR_LEDS=ParametresLlegirColor(args)

                                args.intensitat=256
                                ParametresLlegirIntensitat(args,strip) # definir la intensitat per la tira de leds adressables 1-256
                                
                                args.intensitat=255 # definir la intensitat per la tira de leds NO adressables 0-255
                                
                                TIRES = eval('[0,1,2,3,4,5]')
                                
                                if 'p' in locals() and p and p.is_alive():   p.terminate()
                                if len(comanda) > 1:   
                                    p = Process(target=omplirTemps, args=(strip, COLOR_LEDS,   int(comanda[1])))
                                    p.start()
                                else:                  omplir(strip, COLOR_LEDS)
                                
                                
                                if 'pRGB' in locals() and pRGB and pRGB.is_alive():   pRGB.terminate();
                                if len(comanda) > 1:   
                                    pRGB = Process(target=pintarTiraRGBTemps, args=(pca, TIRES,   COLOR_LEDS,  args.intensitat, int(comanda[1])))
                                    pRGB.start()
                                else:                  pintarTiraRGB(pca, TIRES,   COLOR_LEDS,  args.intensitat)
                                
                                
                                pca.channels[15].duty_cycle = 65534
                                pca.channels[14].duty_cycle = 65534
                                pca.channels[13].duty_cycle = 65534

                                
                            #taquem tires de leds adressables
                            #tanquem 2 tires de leds canal 0-2 i 3-5 de protocol I2C
                            #tanquem canal 15 de protocol I2C
                            elif comanda[0] == "PanicBlack":
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                netejar(strip)
                                
                                TIRES = eval('[0,1,2,3,4,5]')
                                if 'pRGB' in locals() and pRGB and pRGB.is_alive():   pRGB.terminate();
                                pRGB = Process(target=netejarTiraRGB, args=(pca, TIRES))
                                pRGB.start()
                                
                                pca.channels[15].duty_cycle = 0
                                pca.channels[14].duty_cycle = 0
                                pca.channels[13].duty_cycle = 0
                                
                                
                                
                                
                                
                            ######################################################################################################
                            #           TIRA LED ADRESSABLE
                            ######################################################################################################
                            elif comanda[0] == "omplir":
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                omplir(strip, COLOR_LEDS	)

                            elif comanda[0] == "netejar":
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                netejar(strip)

                                
                            elif comanda[0] == "creixer":  #PARM1:temps total milisegons  
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                strip.setBrightness(0)
                                omplir(strip, COLOR_LEDS)
                                p = Process(target=creixer, args=(strip, float(comanda[1])))
                                p.start()
                                
                            elif comanda[0] == "decreixer":  #PARM1:temps total milisegons  
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                strip.setBrightness(255)
                                omplir(strip, COLOR_LEDS)
                                p = Process(target=creixer, args=(strip, float(comanda[1]),True))
                                p.start()
                                
                            elif comanda[0] == "incremental":  # (o rellotge de sorra)   PARM1:temps de salt de un pixel en milisegons  PAR2: Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=incrementalParts, args=(strip,COLOR_LEDS, int(comanda[1]), int(comanda[2])))
                                p.start()


                            elif comanda[0] == "vano":  #   PARM1:temps total ms  PAR2: Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=colorWipeTempsTotal, args=(strip,COLOR_LEDS, int(comanda[1]), int(comanda[2])))
                                p.start()


                                
                            elif comanda[0] == "theaterChaseIteracions":  #   PARM1:temps de salt de un pixel en milisegons  PAR2: longitud
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=theaterChaseIteracions, args=(strip, COLOR_LEDS, int(comanda[1]), int(comanda[2])))
                                p.start()
                            elif comanda[0] == "theaterChaseTempsTotal":  #   PARM1:temps de salt de un pixel en milisegons  PAR2: longitud     PAR3:Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=theaterChaseTempsTotal, args=(strip, COLOR_LEDS, int(comanda[1]), int(comanda[2]), int(comanda[3])))
                                p.start()
                                
                                
                                
                                
                            elif comanda[0] == "rainbowIteracions":  #   PARM1:temps de salt de un pixel en milisegons  PAR2: Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=rainbowIteracions, args=(strip, int(comanda[1]), int(comanda[2])))
                                p.start()
                            elif comanda[0] == "rainbowTempsTotal":  #   PARM1:temps de salt de un pixel en milisegons  PAR2:Temps total
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=rainbowTempsTotal, args=(strip, int(comanda[1]), int(comanda[2])))
                                p.start()
                            elif comanda[0] == "rainbowCycleIteracions":  #   PARM1:temps de salt de un pixel en milisegons  PAR2: Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=rainbowCycleIteracions, args=(strip, int(comanda[1]), int(comanda[2])))
                                p.start()
                            elif comanda[0] == "rainbowCycleTempsTotal":  #   PARM1:temps de salt de un pixel en milisegons  PAR2: Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=rainbowCycleTempsTotal, args=(strip, int(comanda[1]), int(comanda[2])))
                                p.start()
                            elif comanda[0] == "theaterChaseRainbow":  #   PARM1:temps de salt de un pixel en milisegons  PAR2: Parts o subconjunts
                                if 'p' in locals() and p and p.is_alive():   p.terminate();
                                p = Process(target=theaterChaseRainbow, args=(strip, int(comanda[1]), int(comanda[2])))
                                p.start()

                                
                                

                            ######################################################################################################
                            #           TIRES LED PROTOCOL I2C (de tres en tres RGB)
                            ######################################################################################################
                            elif comanda[0] == "seleccionarTiraRGB":
                                TIRES = eval('[' +  comanda[1] + ']')
                                
                            elif comanda[0] == "pintarTiraRGB":  
                                if 'pRGB' in locals() and pRGB and pRGB.is_alive():   pRGB.terminate();
                                
                                if len(comanda) > 1:   pRGB = Process(target=pintarTiraRGBTemps, args=(pca, TIRES,   COLOR_LEDS,  args.intensitat,int(comanda[1])))
                                else:                  pRGB = Process(target=pintarTiraRGB, args=(pca, TIRES,   COLOR_LEDS,  args.intensitat))
                                
                                pRGB.start()
                            
                            elif comanda[0] == "netejarTiraRGB":
                                if 'pRGB' in locals() and pRGB and pRGB.is_alive():   pRGB.terminate();
                                pRGB = Process(target=netejarTiraRGB, args=(pca, TIRES))
                                pRGB.start()

                            elif comanda[0] == "creixerTiraRGB":          #PARM1:temps total ms
                                if 'pRGB' in locals() and pRGB and pRGB.is_alive():   pRGB.terminate();
                                pRGB = Process(target=creixerTiraRGB, args=(pca, TIRES,   COLOR_LEDS,  int(comanda[1])))
                                pRGB.start()
                            
                            elif comanda[0] == "decreixerTiraRGB":          #PARM1:temps total ms
                                if 'pRGB' in locals() and pRGB and pRGB.is_alive():   pRGB.terminate();
                                pRGB = Process(target=creixerTiraRGB, args=(pca, TIRES,   COLOR_LEDS,  int(comanda[1]), True))
                                pRGB.start()


                                
                                
                            ######################################################################################################
                            #           SWITCH PROTOCOL I2C (un canal en concret)
                            ######################################################################################################
                            elif comanda[0] == "activarCanalI2C":          
                                pca.channels[int(comanda[1])].duty_cycle = 65534
                                
                            elif comanda[0] == "desactivarCanalI2C":          
                                pca.channels[int(comanda[1])].duty_cycle = 0
                                
                            
                            else:
                                break
                else:
                    break  
        finally:
            connection.close()
