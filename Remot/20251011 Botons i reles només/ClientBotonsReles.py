
#Programa per llegir un boto i fer aleatoriament si mostrar uns reles o altres en funció de si ha encertat




# python.exe -m pip install --upgrade pip
import serial     #pip install pyserial
import configparser
from configparser import NoOptionError, NoSectionError
import os # buscar el directori actual per trobar el fitxer de configuarció de propietats
from paramiko import SSHClient, AutoAddPolicy       #pip install paramiko
import subprocess
import time
import os
import random

#import webbrowser
import subprocess
import winreg
import json
import urllib.request



import serial.tools.list_ports  

            
connexioSerialBotonera = None
connexioSerialReles = None

client = None

configBotonera = configparser.RawConfigParser()
configBotonera.read(               os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controladoraBotonsReles.properties')              )

url1 = "file:///"+os.getcwd()+"/BotonsCelPanic.html"
url2 = "file:///"+os.getcwd()+"/BotonsCelPanic.html?data=1s2s5s7s9&premut=2"


            
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
            




websocketBrowser = None

            
def InicialitzarBrowser():      
    
    global websocketBrowser

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
        chrome_path, _ = winreg.QueryValueEx(key, "")

    except FileNotFoundError:
        return None

    if chrome_path:
        print(f"Chrome trobat al registre: {chrome_path}")
    else:
        print("Chrome no trobat al registre.")


    user_data_dir = r"C:\temp\chrome-profile"
    port = "9222"

    subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        f"--remote-allow-origins=*",
        url1
        #,"--start-fullscreen"
    ])


    # Connecta't a l'API local de Chrome
    data = urllib.request.urlopen("http://localhost:9222/json").read()
    tabs = json.loads(data)

    # Agafem la primera pestanya oberta
    tab = tabs[0]
    websocket_url = tab["webSocketDebuggerUrl"]

    # Connectem-hi per dir-li que canviï de pàgina
    from websocket import create_connection

    websocketBrowser = create_connection(websocket_url)






def CanviarBrowser(pUrl):      
    
    command = json.dumps({
        "id": 1,
        "method": "Page.navigate",
        "params": {"url": pUrl}
    })
    websocketBrowser.send(command)
    


  
            
if __name__ == '__main__':


    LlistarUSB()
    InicialitzarUSB()
    InicialitzarBrowser()
    
    print("Configuració incial finalitzada")
    
    
    

    
    exit()

    
    try:
        while True:
            if connexioSerialBotonera.inWaiting():
                idBotonera= connexioSerialBotonera.readline().decode("utf-8") .rstrip("\r\n")
                print("-"+idBotonera+"-")

                botoPremut = configBotonera.get('BotoneraUSB','boto.'+idBotonera)

                numeros = sorted(random.sample(range(30), 10))
                print(numeros)
                CanviarBrowser(url1 + "?data="+'s'.join(str(n) for n in numeros)+"&premut="+botoPremut)


                if valor in numeros:
                    print(f"El número {valor} està dins la llista.")
                    connexioSerialReles.write( ("on:0" + "\n").encode("utf-8"))    
                else:
                    print(f"El número {valor} no està dins la llista.")
                    connexioSerialReles.write( ("on:5" + "\n").encode("utf-8"))    
                
                time.sleep(5)
                connexioSerialReles.write( ("pb:" + "\n").encode("utf-8"))    
                connexioSerialBotonera.reset_input_buffer()   #ignorem altres botons que hagi premut l'usuari




                    
            if (connexioSerialReles.inWaiting()):
                time.sleep(0.1)
                comanda= connexioSerialReles.read(connexioSerialReles.in_waiting).decode("utf-8") .rstrip("\r\n")
                print("La reles ens diu: "+comanda )
                




    finally:
        connexioSerialBotonera.close()   
        connexioSerialReles.close()
        websocketBrowser.close()