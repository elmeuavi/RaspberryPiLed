
#Programa per llegir un boto i fer aleatoriament si mostrar uns reles o altres en funció de si ha encertat



#pip install websocket-client
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
import traceback
 
#import webbrowser
import subprocess
import winreg
import json
import urllib.request



import serial.tools.list_ports  

            
myports = None
connexioSerialBotonera = None
connexioSerialReles = None

client = None

configBotonera = configparser.RawConfigParser()
configBotonera.read(               os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controladoraBotonsReles.properties')              )

url1 = "file:///"+os.getcwd()+"/BotonsCelPanic.html"
url2 = "file:///"+os.getcwd()+"/BotonsCelPanic.html?data=1s2s5s7s9&premut=2"

def InicialitzarUSB():
    InicialitzarUSBReles()
    InicialitzarUSBBotons()

            
def InicialitzarUSBBotons():

    global connexioSerialBotonera
    
    wVelocitat = int(configBotonera.get('BotoneraUSB','botonera.velocitat'))
    #wPort = configBotonera.get('BotoneraUSB','botonera.port')

    ch340_ports = [port for port in myports if 'CH340' in port.description]
    wPort = ch340_ports[0].device

        
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



    
    
def InicialitzarUSBReles():

    global connexioSerialReles
    
    wVelocitat = int(configBotonera.get('RelesUSB','reles.velocitat'))
    #wPort = configBotonera.get('RelesUSB','reles.port')

    ch340_ports = [port for port in myports if 'Arduino Uno' in port.description]
    wPort = ch340_ports[0].device
        
    
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

    global myports

    #Primera forma de mirar els elements connectats via USB
    myports =  list(serial.tools.list_ports.comports())
    print( myports)

    print("-" * 40)
    for port in myports:
        print("Port:", port.device)
        print("Descripció:", port.description)
        print("Fabricant:", port.manufacturer)
        print("Producte:", port.product)
        print("Número de sèrie:", port.serial_number)
        print("VID:", port.vid)
        print("PID:", port.pid)
        print("HWID:", port.hwid)
        print("Ubicació:", port.location)
        print("Interfície:", port.interface)
        print("-" * 40)


    

#    # Filtrar els ports que tenen 'CH340' a la descripció
#    ch340_ports = [port.device for port in myports if 'CH340' in port.description]
#
#    # Mostrar els ports trobats
#    print("Ports CH340 trobats:", ch340_ports)
#
#    # Si només vols el primer port trobat:
#    if ch340_ports:
#        primer_port = ch340_ports[0]
#        print("Primer port CH340:", primer_port)
#    else:
#        print("No s'ha trobat cap dispositiu CH340.")





    #Segona forma de mirar els elements connectats via USB
    #os.system(" powershell \"Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } \"")


    
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
        f"--autoplay-policy=no-user-gesture-required",    # IMPORTANT per poder reproduir so només obrir una web !!
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
    
    
    try:
        while True:
            try:
                #time.sleep(0.2)
                if connexioSerialBotonera.inWaiting():
                    botoPremut=None
                    idBotonera= connexioSerialBotonera.readline().decode("utf-8") .rstrip("\r\n")
                    print("-"+idBotonera+"-")
                    try:
                        botoPremut = configBotonera.get('BotoneraUSB','boto.'+idBotonera)
                    except NoOptionError: #(option, section):
                        print("no hem trobat ")
                    if botoPremut:
                        numeros = sorted(random.sample(range(30), 10))
                        print(numeros)
                        novaUrl = url1 + "?data="+'s'.join(str(n) for n in numeros)+"&premut="+botoPremut
                        print(novaUrl)
                        CanviarBrowser(novaUrl)
                        connexioSerialBotonera.reset_input_buffer() 

                        time.sleep(6)
                        connexioSerialBotonera.reset_input_buffer() 
                        if int(botoPremut) in numeros:
                            #encenc els reles del 4 al 7
                            print(f"El número {botoPremut} està dins la llista.")
                            connexioSerialReles.write( ("up:" + "\n").encode("utf-8"))        
                        else:
                            #encenc els reles del 0 al 3
                            print(f"El número {botoPremut} no està dins la llista.")
                            connexioSerialReles.write( ("dw:" + "\n").encode("utf-8"))   


                            
                        time.sleep(12.5)
                        connexioSerialReles.reset_input_buffer() 
                        #while connexioSerialReles.is_open and connexioSerialReles.inWaiting():  
                        #       comanda= connexioSerialReles.read(connexioSerialReles.in_waiting).decode("utf-8") .rstrip("\r\n")
                        #       print("Els reles ens diu: "+comanda )
                        connexioSerialReles.write( ("pb:" + "\n").encode("utf-8"))    
                        CanviarBrowser(url1)
                        time.sleep(0.5)
                        connexioSerialBotonera.reset_input_buffer() 
                        connexioSerialReles.reset_input_buffer() 



                        
                if (connexioSerialReles.inWaiting()):
                    time.sleep(0.1)
                    comanda= connexioSerialReles.read(connexioSerialReles.in_waiting).decode("utf-8") .rstrip("\r\n")
                    print("La reles ens diu: "+comanda )
                    

            except serial.SerialException:
                print("Error del serial");
                traceback.print_exc()
                connexioSerialBotonera.close()
                if not connexioSerialBotonera.is_open :
                    print("Botonera")
                    time.sleep(2)
                    #LlistarUSB()
                    InicialitzarUSBBotons()


    finally:
        connexioSerialBotonera.close()   
        connexioSerialReles.close()
        websocketBrowser.close()