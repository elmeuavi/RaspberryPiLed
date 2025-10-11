
#Programa per llegir un boto i fer aleatoriament si mostrar uns reles o altres en funció de si ha encertat




# python.exe -m pip install --upgrade pip
import serial     #pip install pyserial
import configparser
from configparser import NoOptionError, NoSectionError
import os # buscar el directori actual per trobar el fitxer de configuarció de propietats
from paramiko import SSHClient, AutoAddPolicy       #pip install paramiko
import subprocess
import time
#import webbrowser
import subprocess

import serial.tools.list_ports  

            
connexioSerialBotonera = None
connexioSerialReles = None

client = None

configBotonera = configparser.RawConfigParser()
configBotonera.read(               os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controladoraBotonsReles.properties')              )

url1 = "file:///C:/Users/Xevi/Documents/RaspberryPiLed/Remot/20251011%20Botons%20i%20reles%20nom%C3%A9s/BotonsCelPanic.html"
url2 = "file:///C:/Users/Xevi/Documents/RaspberryPiLed/Remot/20251011%20Botons%20i%20reles%20nom%C3%A9s/BotonsCelPanic.html?data=1s2s5s7s9&premut=2"


            
def InicialitzarUSB():

    global connexioSerialBotonera
    global connexioSerialReles
    
    wVelocitat = int(configBotonera.get('BotoneraUSB','botonera.velocitat'))
    wPort = configBotonera.get('BotoneraUSB','botonera.port')
        
    try:
        print('BOTONERA: provem connexió al port '+wPort + ' amb velocitat ' + str(wVelocitat))
        connexioSerialBotonera = serial.Serial(wPort,wVelocitat) # ,timeout = None
        print('Connexió USB amb la caixa botonera realitzada correctament al port '+wPort)
    except:
        print('ERROR: no tenim port USB on trobar la botonera')
        exit(0)

    #la primera comanda la despreciem perquè pot arribar mitja comanda
    comanda= connexioSerialBotonera.readline().decode("utf-8") .rstrip("\r\n")
    print (comanda)



    
    
    
    wVelocitat = int(configBotonera.get('RelesUSB','reles.velocitat'))
    wPort = configBotonera.get('RelesUSB','reles.port')
        
    
    try:
        print('BOTONERA: provem connexió al port '+wPort + ' amb velocitat ' + str(wVelocitat))
        connexioSerialReles = serial.Serial(wPort,wVelocitat) # ,timeout = None
        print('Connexió USB amb la reles realitzada correctament al port '+wPort)
    except:
        print('ERROR: no tenim port USB on trobar la reles')
        exit(0)

    #la primera comanda la despreciem perquè pot arribar mitja comanda
    comanda= connexioSerialReles.readline().decode("utf-8") .rstrip("\r\n")
    print (comanda)




def LlistarUSB():

    #Primera forma de mirar els elements connectats via USB
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print( myports)

    #Segona forma de mirar els elements connectats via USB
    os.system(" powershell \"Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } \"")


    
    #comanda="powershell \"$valor = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } | Select  -ExpandProperty FriendlyName; $valor2=$valor -match '(COM\\d*)' ; Write-Host $matches.0 \""
    #print (comanda)
    #port = subprocess.check_output(comanda, shell=True).rstrip()
    #print ("Ens connectarem al port -" + str(port.decode("utf-8")) +"-")
    #print (port)
    
    #return str(port.decode("utf-8"))
            
            
def InicialitzarBrowser():            


    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
#
#    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
#    webbrowser.get('chrome').open(url1)
#    time.sleep(10)
#    webbrowser.get('chrome').open(url2)    

    profile_dir = r"C:\temp\chrome_temp_profile"
    
    # Obre la primera URL en mode pantalla completa
    p = subprocess.Popen([
        chrome_path,
        f"--user-data-dir={profile_dir}",
        "--kiosk",
        "--new-window",
        url1
    ])



def CanviarBrowser():      
    
    # Canvia la URL a la mateixa finestra mitjançant la nova URL
    # Amb Chrome no pots “reutilitzar pestanya” fàcilment, però pots obrir la nova URL a la mateixa finestra amb:
    subprocess.Popen([
        chrome_path,
        f"--user-data-dir={profile_dir}",
        "--kiosk",
        url2
    ])

  
            
if __name__ == '__main__':


    LlistarUSB()
    InicialitzarUSB()
    InicialitzarBrowser()
    
    print("Configuració incial finalitzada")

    
    try:
        while True:
            if connexioSerialBotonera.inWaiting():
                comanda= connexioSerialBotonera.readline().decode("utf-8") .rstrip("\r\n")
                print("-"+comanda+"-")

                #transformem el botó apretat a una comanda
                try:
                    comanda = "on:" + configBotonera.get('BotoneraUSB','boto.'+comanda)
                    
                except NoOptionError:
                    comanda="@Comanda desconeguda" 
                print("-"+comanda+"-")
                
                
                if (not "@Comanda desconeguda" == comanda ) :
                    connexioSerialReles.write( (comanda + "\n").encode("utf-8"))    

                    
            if (connexioSerialReles.inWaiting()):
                time.sleep(0.1)
                comanda= connexioSerialReles.read(connexioSerialReles.in_waiting).decode("utf-8") .rstrip("\r\n")
                print("La reles ens diu: "+comanda )
                




    finally:
        connexioSerialBotonera.close()   
        connexioSerialReles.close()