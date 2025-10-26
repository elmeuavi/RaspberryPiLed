
#Programa per llegir un boto que es transforma amb una comanda de la pantalla led amb el fitxer de propietats 
#i enviar-li la comanda a la pantalla.




# python.exe -m pip install --upgrade pip
import serial     #pip install pyserial
import configparser
from configparser import NoOptionError, NoSectionError
import os # buscar el directori actual per trobar el fitxer de configuarció de propietats
from paramiko import SSHClient, AutoAddPolicy       #pip install paramiko
import subprocess
import time

import serial.tools.list_ports  

            
connexioSerialBotonera = None
connexioSerialPantalla = None

client = None

configBotonera = configparser.RawConfigParser()
configBotonera.read(               os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controladoraBotonsPantalla.properties')              )


            
def InicialitzarUSB():

    global connexioSerialBotonera
    global connexioSerialPantalla
    
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



    
    
    
    wVelocitat = int(configBotonera.get('PantallaUSB','pantalla.velocitat'))
    wPort = configBotonera.get('PantallaUSB','pantalla.port')
        
    
    try:
        print('BOTONERA: provem connexió al port '+wPort + ' amb velocitat ' + str(wVelocitat))
        connexioSerialPantalla = serial.Serial(wPort,wVelocitat) # ,timeout = None
        print('Connexió USB amb la pantalla realitzada correctament al port '+wPort)
    except:
        print('ERROR: no tenim port USB on trobar la pantalla')
        exit(0)

    #la primera comanda la despreciem perquè pot arribar mitja comanda
    comanda= connexioSerialPantalla.readline().decode("utf-8") .rstrip("\r\n")
    print (comanda)




def LlistarUSB():

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
        print("Vendedor ID VID:", port.vid)
        print("Product ID:", port.pid)
        print("HWID:", port.hwid)
        print("Ubicació:", port.location)
        print("Interfície:", port.interface)
        print("-" * 40)

    #Segona forma de mirar els elements connectats via USB
    #os.system(" powershell \"Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } \"")


    
    #comanda="powershell \"$valor = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } | Select  -ExpandProperty FriendlyName; $valor2=$valor -match '(COM\\d*)' ; Write-Host $matches.0 \""
    #print (comanda)
    #port = subprocess.check_output(comanda, shell=True).rstrip()
    #print ("Ens connectarem al port -" + str(port.decode("utf-8")) +"-")
    #print (port)
    
    #return str(port.decode("utf-8"))
            
            
            
            
            
if __name__ == '__main__':

    LlistarUSB()
    InicialitzarUSB()

    
    print("Configuració incial finalitzada")

    
    try:
        while True:
            if connexioSerialBotonera.inWaiting():
                comanda= connexioSerialBotonera.readline().decode("utf-8") .rstrip("\r\n")
                print("-"+comanda+"-")

                #transformem el botó apretat a una comanda
                try:
                    comanda = configBotonera.get('BotoneraUSB','boto.'+comanda)
                    
                except NoOptionError:
                    comanda="@Comanda desconeguda" 
                print("-"+comanda+"-")
                
                if ( comanda == "ts:" ):
                    comanda = "ts: "
                
                if (not "@Comanda desconeguda" == comanda ) :
                    connexioSerialPantalla.write( (comanda + "\n").encode("utf-8"))    

                    
            if (connexioSerialPantalla.inWaiting()):
                time.sleep(0.1)
                comanda= connexioSerialPantalla.read(connexioSerialPantalla.in_waiting).decode("utf-8") .rstrip("\r\n")
                print("La pantalla ens diu: "+comanda )
                
                
                #connexioSerialPantalla.writelines(comanda.encode("utf-8"))
                #comanda= connexioSerialPantalla.read().decode("utf-8") .rstrip("\r\n")
                #print (comanda)


                # mirem si és un comentari o cadena buida
                #if comanda[0:1] != "@" and comanda != "":
                    #if comanda[0:4] == "gpio": 
                    #    stdin, stdout, stderr = client.exec_command(comanda)
                    #else:
                    #    sock.sendall(bytearray(comanda.strip(), 'utf-8'))



    finally:
        connexioSerialBotonera.close()   
        connexioSerialPantalla.close()