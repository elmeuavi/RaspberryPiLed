import serial
import socket
import configparser
from configparser import NoOptionError, NoSectionError
import os # buscar el directori actual per trobar el fitxer de configuarció de propietats
from paramiko import SSHClient, AutoAddPolicy



            
connexioSerialUSB = None
sock = None
client = None

configBotonera = configparser.RawConfigParser()
configBotonera.read(               os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controladora.properties')              )

configControladora = configparser.RawConfigParser()
configControladora.read(       os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuracio.properties')             )


            
def InicialitzarUSB():

    global connexioSerialUSB
    
    BotoneraVelocitat = int(configControladora.get('LEDS REMOT','botonera.velocitat'))
        
    #mirem quins ports serie hi ha connectats
    #import serial.tools.list_ports    
    #myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    #print( myports)
    
    try:
        print('provem connexió al port '+PORTBOTONERA)
        connexioSerialUSB = serial.Serial(PORTBOTONERA,BotoneraVelocitat) # ,timeout = None
        print('Connexió USB amb la caixa botonera realitzada correctament al port '+PORTBOTONERA)
    except:
        None
        
    #si no ha funcionat amb l'anterior, provem amb el port usb que tinc a l'altre portàtil
    if connexioSerialUSB is None:		
        try:
            print('provem connexió al port COM6')
            connexioSerialUSB = serial.Serial('COM6',BotoneraVelocitat) # ,timeout = None
            print('Connexió USB amb la caixa botonera realitzada correctament al port COM6')
        except:
            None
    #si no ha funcionat amb l'anterior, provem amb el port usb que tinc a l'altre portàtil			
    if connexioSerialUSB is None:
        try:
            print('provem connexió al port COM5')
            connexioSerialUSB = serial.Serial('COM5',BotoneraVelocitat) # ,timeout = None
            print('Connexió USB amb la caixa botonera realitzada correctament al port COM5')
        except:
            print('ERROR: no tenim port USB on trobar la botonera')
            exit(0)

    #la primera comanda la despreciem perquè pot arribar mitja comanda
    comanda= connexioSerialUSB.readline().decode("utf-8") .rstrip("\r\n")


def InicialitzarConnexions():

    global sock
    global client
    sIpRaspberry = None
    iPort = None

    try:
        sIpRaspberry = configControladora.get('LEDS REMOT','raspberry.ip')
        iPort = configControladora.get('LEDS REMOT','raspberry.port')
    except NoOptionError:
        sIpRaspberry = "192.168.1.144"
        iPort = 10000    
    
    
    print('Inicialitzem el client socket TCP/IP:')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sIpRaspberry, int(iPort))
    print ( 'connecting to %s port %s ...' % server_address)
    sock.connect(server_address)
    
    
    print('inicialitzem el client ssh contra la IP ' +sIpRaspberry)
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(sIpRaspberry, username='pi', password='raspberry')

            
            
            
if __name__ == '__main__':

    InicialitzarConnexions()
    InicialitzarUSB()
    
    
    
    try:
        while True:
            if connexioSerialUSB.inWaiting():

                #transformem el botó apretat a una comanda
                try:
                    comanda = configBotonera.get('BotoneraUSB','boto.'+comanda)
                except NoOptionError:
                    comanda="@Comanda desconeguda" 
                print("-"+comanda+"-")
                    
                
                # mirem si és un comentari o cadena buida
                if comanda[0:1] != "@" and comanda != "":
                    if comanda[0:4] == "gpio": 
                        stdin, stdout, stderr = client.exec_command(comanda)
                    else:
                        sock.sendall(bytearray(comanda.strip(), 'utf-8'))



    finally:
        connexioSerialUSB.close()   
        sock.close()