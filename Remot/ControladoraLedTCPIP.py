# coding: latin-1
#python.exe -m pip install --upgrade pip
#python -m pip install paramiko

from paramiko import SSHClient, AutoAddPolicy
import time
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk

import socket
from tkinter import filedialog

#pip install pyserial
import serial  # per la comunicació amb el USB per a la botonera
import serial.tools.list_ports  
import subprocess

from multiprocessing  import Queue 
#from xeviClientBotonsUSB import *

#python -m pip install pygame
import pygame # per la musica

from multiprocessing import Process, Event  # procés en background per la reproducció dels clips generats
import signal #per a capturar el final del procés en background

from os.path import expanduser # per a obtenir el directori de l'usuari expanduser("~")

from pathlib import Path # per obtenir el teu directori arrel de windows


import sys  # mirar el detall de la excepcio

import configparser
from configparser import NoOptionError, NoSectionError
import os # buscar el directori actual per trobar el fitxer de configuarció de propietats


#from machine import Timer
#import turtle


xeviEncenLedGPIO = "~/rpi-ws281x-python/xevi/lib/xeviEncenLedGPIO.sh"
xeviAnimacioLed = "~/rpi-ws281x-python/xevi/lib/xeviAnimacioLed.py"
xeviTiraRGB = "~/rpi-ws281x-python/xevi/lib/xeviTiraRGB.py"
killxevi = "~/rpi-ws281x-python/xevi/killxevi.sh "
servidorTCPIP = "~/rpi-ws281x-python/xevi/lib/servidor.py "

#"192.168.1.144"
sIpRaspberry = None
#10000
iPort = None



start_time = time.time()
client = None
sock = None
connexioSerialUSB = None
configControladora = configparser.RawConfigParser()
configBotonera = configparser.RawConfigParser()




def INICIALITZACONNEXIONS():
    global client
    global sock
    global connexioSerialUSB
    global configBotonera
    global sIpRaspberry
    global iPort
    
    debug=False
    MirarBotonera=False
    BotoneraVelocitat=500000
    
    
    
    configControladora.read(       os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuracio.properties')             )
    
    try:
        sIpRaspberry = configControladora.get('LEDS REMOT','raspberry.ip')
        iPort = configControladora.get('LEDS REMOT','raspberry.port')
        MirarBotonera = configControladora.get('LEDS REMOT','botonera.mode') == '1' #0-desactivada 1-integradaRemota 2-independentRemota 3-IntegradaServidor
        BotoneraVelocitat = int(configControladora.get('LEDS REMOT','botonera.velocitat'))
    except NoOptionError:
        sIpRaspberry = "192.168.1.144"
        iPort = 10000
    

    # IMPORTANT haver engegat el servidor de la tira LED adressable en remot
    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' servidor.py')
    #client.exec_command('sudo nohup python3 ' + servidorTCPIP + ' &')

    if not is_socket_opened(sock):
        print('inicialitzem el client socket TCP/IP contra la IP ' +sIpRaspberry+':'+iPort)
        # Create a TCP/IP socket per al led adresable
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port on the server given by the caller
        server_address = (sIpRaspberry, int(iPort))
        sock.connect(server_address)


    #Crear una sessió SSH contra la raspberry per a la resta d'elements
    if client is None or  client.get_transport() is None:
        print('inicialitzem el client ssh contra la IP ' +sIpRaspberry+':'+iPort)
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(sIpRaspberry, username='pi', password='raspberry')


    #Inicialitzar el PIN 10 de la raspberry en moda de sortida
    stdin, stdout, stderr = client.exec_command('gpio -g mode 10 out')





    if not MirarBotonera:
        print('NO configurarem la botonera de forma integrada')
    else:

        configBotonera.read(               os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controladora.properties')              )
            
        PORTBOTONERA=LlistarUSB()
        
        try:
            print('provem connexió al port '+PORTBOTONERA + ' amb velocitat ' + str(BotoneraVelocitat))
            connexioSerialUSB = serial.Serial(PORTBOTONERA,BotoneraVelocitat) # ,timeout = None
            print('Connexió USB amb la caixa botonera realitzada correctament al port '+PORTBOTONERA)
        except:
            print('no tenim port USB on trobar la botonera')
            None
        


def LlistarUSB():

    #Primera forma de mirar els elements connectats via USB
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print( myports)

    #Segona forma de mirar els elements connectats via USB
    os.system(" powershell \"Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } \"")


    #una altre manera de fer-ho
    #port = os.popen(" powershell \"$valor = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } | Select  -ExpandProperty FriendlyName; $valor2=$valor -match '(COM\\d*)' ; Write-Host $Matches.0 \"").read().rstrip()
    #print ("Ens connectarem al port -" + port + "-")
    
    port = subprocess.check_output("powershell \"$valor = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Where-Object { $_.FriendlyName -match 'CH340' } | Select  -ExpandProperty FriendlyName; $valor2=$valor -match '(COM\\d*)' ; Write-Host $Matches.0 \"", shell=True).rstrip()
    #print ("Ens connectarem al port -" + str(port.decode("utf-8")) +"-")
    
    return str(port.decode("utf-8"))
            
            

def TANCARCONNEXIONS():
    client.close()
    sock.close()
    try:
        if connexioSerialUSB is not None:
            connexioSerialUSB.close()
    except serial.serialutil.SerialException:
        None


def RegistrarComanda(pComanda):
    global procesSimular
    if  (pygame.mixer.get_init() and pygame.mixer.music.get_busy()) or (procesSimular and procesSimular.is_alive()):
        temps = str(tempsReproduccioAcomulat + (time.time() - horaIniciReproducio ))
        temps = temps[0:temps.index('.')+4]
        #lbOrdres.insert ( tk.END,temps + '#' + pComanda)
        
        posicio=0
        for i, listbox_entry in enumerate(lbOrdres.get(0, tk.END)):
            comanda = listbox_entry.split()
            if len(comanda)> 0 and float(comanda[0]) < float(temps):   posicio=i 
        
        #lbOrdres.select_clear(0, "end")                            
        lbOrdres.insert ( posicio+1,temps + ' # ' + pComanda)
        lbOrdres.selection_set(posicio+1)
        lbOrdres.see(posicio+1) 

                    
    else:
        temps = str(time.time() - start_time)
        temps = temps[0:temps.index('.')+4]
        #només es mostrarà a la consola la instrucció
        #print("nomes a consola:")
    
    print(temps,' # ', pComanda)


def EnviarComandaAServidor(pComanda):

    RegistrarComanda( pComanda)
    
    #si estem simulant no podem enviar des d'aquí
    if not procesSimular or not procesSimular.is_alive():
        sock.sendall(bytearray(pComanda, 'utf-8'))
    else:
        #Estem executant el procés de reproducció del mp3 i no tenim accés al socket.. ho posem a la Queue cap al procés pq sigui ell qui ho envii
        cuaOrdresUSB.put(pComanda)
        


    
def is_socket_opened(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        #print("unexpected exception when checking if a socket is closed")
        return False
    return False
    
    
    

def PanicCelestialOn(event):
    #stdin, stdout, stderr = client.exec_command('sudo python3 ' + xeviTiraRGB + ' --color W  --animacio pintar --intensitat 255 &')
    #EnviarComandaAServidor('|intensitat 255|seleccionarTiraRGB 0,1,2,3,4,5|color W|pintarTiraRGB')
    
    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed &&  sudo python3 ' + xeviAnimacioLed + ' --animacio pintar --color W  ')
    #EnviarComandaAServidor('|intensitat 255|color W|omplir')
    
    EnviarComandaAServidor('|PanicBlanc')
    
    
#    stdin, stdout, stderr = client.exec_command('gpio -g write 10 1')
#    global activatGPIO10
#    activatGPIO10=True
#    btn_textEncendreGPIO10.set("Apagar leds GPIO-10")    
#    RegistrarComanda( "gpio -g write 10 1") 


    #EnviarComandaAServidor('|activarCanalI2C 15' )
    global activat220vI2C15
    activat220vI2C15=True
    btn_textEncendreI2C15.set("Apagar 220v I2C (canal 15)")

    #EnviarComandaAServidor('|activarCanalI2C 14' )
    global activat220vI2C14
    activat220vI2C14=True
    btn_textEncendreI2C14.set("Apagar 220v I2C (canal 14)")

    #EnviarComandaAServidor('|activarCanalI2C 13' )
    global activat220vI2C13
    activat220vI2C13=True
    btn_textEncendreI2C13.set("Apagar 220v I2C (canal 13)")

    #EnviarComandaAServidor('|activarCanalI2C 12' )
    global activat220vI2C12
    activat220vI2C12=True
    btn_textEncendreI2C12.set("Apagar 220v I2C (canal 12)")


    #stdin, stdout, stderr = client.exec_command('gpio -g write 13 1')
    #RegistrarComanda( "gpio -g write 13 1") 
    

    
    
def PanicCelestialOff(event):

    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio pintar --color W --esborrar')
    #netejarLedAdressable()

    #stdin, stdout, stderr = client.exec_command('sudo python3 ' + xeviTiraRGB + ' --color W  --animacio pintar --esborrar &')
    #sock.sendall(bytearray('|seleccionarTiraRGB 0,1,2,3,4,5|netejarTiraRGB', 'utf-8'))
    #ApagarRGB()

    EnviarComandaAServidor('|PanicBlack' )
    
    
    #ApagarGPIO()    
    
#    stdin, stdout, stderr = client.exec_command('gpio -g write 10 0')
#    global activatGPIO10
#    activatGPIO10=False
#    btn_textEncendreGPIO10.set("Encendre leds GPIO-10")
#    RegistrarComanda( "gpio -g write 10 0")
    
    #stdin, stdout, stderr = client.exec_command('gpio -g write 13 0')
    #RegistrarComanda( "gpio -g write 13 0 ")
    
    #EnviarComandaAServidor('|desactivarCanalI2C 15' )
    global activat220vI2C15
    activat220vI2C15=False
    btn_textEncendreI2C15.set("Encendre 220v I2C (canal 15)")
    
    #EnviarComandaAServidor('|desactivarCanalI2C 14' )
    global activat220vI2C14
    activat220vI2C14=False
    btn_textEncendreI2C14.set("Encendre 220v I2C (canal 14)")
    
    #EnviarComandaAServidor('|desactivarCanalI2C 13' )
    global activat220vI2C1
    activat220vI2C13=False
    btn_textEncendreI2C13.set("Encendre 220v I2C (canal 13)")
    
    #EnviarComandaAServidor('|desactivarCanalI2C 12' )
    global activat220vI2C12
    activat220vI2C12=False
    btn_textEncendreI2C12.set("Encendre 220v I2C (canal 12)")
    

    
    
#def ApagarGPIO(event=None):
#    EnviarComandaAServidor('|desactivarCanalI2C 15' )
#    global activat220vI2C15
#    activat220vI2C15=False
#    btn_textEncendreI2C15.set("Encendre 220v I2C (canal 15)")
#    
#    stdin, stdout, stderr = client.exec_command('gpio -g write 10 0')
#    global activatGPIO10
#    activatGPIO10=False
#    btn_textEncendreGPIO10.set("Encendre leds GPIO-10")
#    RegistrarComanda( "gpio -g write 10 0")
#    
#    #stdin, stdout, stderr = client.exec_command('gpio -g write 13 0')
#    #RegistrarComanda( "gpio -g write 13 0 ")
    





#def GPIO10On(event):
#    stdin, stdout, stderr = client.exec_command('sleep 0.2 && gpio -g write 10 1')
#
#def GPIO10Off(event):
#    stdin, stdout, stderr = client.exec_command('sleep 0.2 && gpio -g write 10 0')

activatGPIO10=False
def EncendreGPIO10(event=None):
    global activatGPIO10
    if activatGPIO10:  
        stdin, stdout, stderr = client.exec_command('gpio -g write 10 0')
        activatGPIO10=False
        btn_textEncendreGPIO10.set("Encendre leds GPIO-10")
        RegistrarComanda( "gpio -g write 10 0")
    else:                     
        stdin, stdout, stderr = client.exec_command('gpio -g write 10 1')
        activatGPIO10=True
        btn_textEncendreGPIO10.set("Apagar leds GPIO-10")  
        RegistrarComanda( "gpio -g write 10 1")        
    
    #stdin, stdout, stderr = client.exec_command('sh ' + xeviEncenLedGPIO + ' 10 ' + str(float(txtTempsTotal.get())/1000.0) + ' &')
    
    
    
    
activat220vI2C15=False
def Encendre220vI2C15(event=None):
    global activat220vI2C15
    if activat220vI2C15:  
        EnviarComandaAServidor('|desactivarCanalI2C 15' )
        activat220vI2C15=False
        btn_textEncendreI2C15.set("Encendre 220v I2C (canal 15)")
    else:                     
        EnviarComandaAServidor('|activarCanalI2C 15' )
        activat220vI2C15=True
        btn_textEncendreI2C15.set("Apagar 220v I2C (canal 15)")
        
activat220vI2C14=False
def Encendre220vI2C14(event=None):
    global activat220vI2C14
    if activat220vI2C14:  
        EnviarComandaAServidor('|desactivarCanalI2C 14' )
        activat220vI2C14=False
        btn_textEncendreI2C14.set("Encendre 220v I2C (canal 14)")
    else:                     
        EnviarComandaAServidor('|activarCanalI2C 14' )
        activat220vI2C14=True
        btn_textEncendreI2C14.set("Apagar 220v I2C (canal 14)")


activat220vI2C13=False
def Encendre220vI2C13(event=None):
    global activat220vI2C13
    if activat220vI2C13:  
        EnviarComandaAServidor('|desactivarCanalI2C 13' )
        activat220vI2C13=False
        btn_textEncendreI2C13.set("Encendre 220v I2C (canal 13)")
    else:                     
        EnviarComandaAServidor('|activarCanalI2C 13' )
        activat220vI2C13=True
        btn_textEncendreI2C13.set("Apagar 220v I2C (canal 13)")
        
activat220vI2C12=False
def Encendre220vI2C12(event=None):
    global activat220vI2C12
    if activat220vI2C12:  
        EnviarComandaAServidor('|desactivarCanalI2C 12' )
        activat220vI2C12=False
        btn_textEncendreI2C12.set("Encendre 220v I2C (canal 12)")
    else:                     
        EnviarComandaAServidor('|activarCanalI2C 12' )
        activat220vI2C12=True
        btn_textEncendreI2C12.set("Apagar 220v I2C (canal 12)")



#def RGBCanal1On(event):
#    #if chk_color_aleatori.get():
#        stdin, stdout, stderr = client.exec_command('sudo python3 ' + xeviTiraRGB + ' --color A  --animacio pintar --intensitat 255 &')
#    #else:
#    #    stdin, stdout, stderr = client.exec_command('sudo python3 ' + xeviTiraRGB + ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + '  --animacio pintar --intensitat 255 &')
#    
#def RGBCanal1Off(event):
#    stdin, stdout, stderr = client.exec_command('sudo python3 ' + xeviTiraRGB + ' --colorR 1 --colorG 1 --colorB 1  --animacio pintar --intensitat 1 &')

    
sTotesTires = '0,1'
sTiresCanal1 = '0'
sTiresCanal2 = '1'
    
def ApagarRGB(event=None):
    EnviarComandaAServidor('|seleccionarTiraRGB '+sTotesTires+'|netejarTiraRGB')
    
    
def EncendreRGB(event=None):
    #if chk_color_aleatori.get():
    #    stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --color A  --animacio pintar --intensitat ' + str(int(txtIntensitat.get())+1) + ' --long ' + txtTempsTotal.get() + ' --esborrar --tira ' + sCanal.get() + ' &')
    #else:
    #    stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + '  --animacio pintar --intensitat ' + str(int(txtIntensitat.get())+1) + ' --long ' + txtTempsTotal.get() + ' --tira ' + sCanal.get() + ' --esborrar &')
    comanda=""
    if chk_color_aleatori.get():
        comanda+='|color A '
    else:
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()
        
    if sCanal.get() == 'T' : comanda+='|seleccionarTiraRGB '+sTotesTires+' '
    elif sCanal.get() == '1' : comanda+='|seleccionarTiraRGB '+sTiresCanal1+' '
    elif sCanal.get() == '2' : comanda+='|seleccionarTiraRGB '+sTiresCanal2+' '
    
    comanda+='|intensitat ' + txtIntensitat.get() + '|pintarTiraRGB ' #+ txtTempsTotal.get()
    EnviarComandaAServidor(comanda)
    

def CreixerRGB(event=None):
    #if chk_color_aleatori.get():
    #    stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --color A  --animacio creixer  --long ' + txtTempsTotal.get() + ' --tira ' + sCanal.get() + ' --esborrar &')
    #else:
    #    stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + '  --animacio creixer  --long ' + txtTempsTotal.get() + ' --tira ' + sCanal.get() + ' --esborrar &')
    #print('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --color A  --animacio creixer  --long ' + txtTempsTotal.get() + ' --tira ' + sCanal.get() + ' --esborrar &')
    comanda=""
    if chk_color_aleatori.get():
        comanda+='|color A '
    else:
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()
        
    if sCanal.get() == 'T' : comanda+='|seleccionarTiraRGB '+sTotesTires+' '
    elif sCanal.get() == '1' : comanda+='|seleccionarTiraRGB '+sTiresCanal1+' '
    elif sCanal.get() == '2' : comanda+='|seleccionarTiraRGB '+sTiresCanal2+' '
    comanda+='|intensitat ' + txtIntensitat.get() + '|creixerTiraRGB ' + txtTempsTotal.get() 
    EnviarComandaAServidor(comanda)
    
    
def DecreixerRGB(event=None):
    #if chk_color_aleatori.get():
    #    stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --color A  --animacio decreixer  --long ' + txtTempsTotal.get() + ' --tira ' + sCanal.get() + ' --esborrar &')
    #else:
    #    stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviTiraRGB && sudo python3 ' + xeviTiraRGB + ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + '  --animacio decreixer  --long ' + txtTempsTotal.get() + ' --tira ' + sCanal.get() + ' --esborrar &')
    comanda=""
    if chk_color_aleatori.get():
        comanda+='|color A '
    else:
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()
        
    if sCanal.get() == 'T' : comanda+='|seleccionarTiraRGB '+sTotesTires+' '
    elif sCanal.get() == '1' : comanda+='|seleccionarTiraRGB '+sTiresCanal1+' '
    elif sCanal.get() == '2' : comanda+='|seleccionarTiraRGB '+sTiresCanal2+' '
    comanda+='|intensitat ' + txtIntensitat.get() + '|decreixerTiraRGB ' + txtTempsTotal.get() 
    EnviarComandaAServidor(comanda)


    
    
    
    

def rainbowTempsTotal(event=None):
    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio rainbowTempsTotal --wait_ms ' + txtTempsIteracio.get() + ' --long ' + txtTempsTotal.get() + '  --intensitat  ' + str(int(txtIntensitat.get())+1) + ' --esborrar ')
    comanda='|intensitat ' + txtIntensitat.get() + '|rainbowTempsTotal ' + txtTempsIteracio.get() + ' ' + txtTempsTotal.get() 
    EnviarComandaAServidor(comanda)
    
def rainbowCycleTempsTotal(event=None):
    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio rainbowCycleTempsTotal --wait_ms ' + txtTempsIteracio.get() + ' --long ' + txtTempsTotal.get() + '  --intensitat  ' + str(int(txtIntensitat.get())+1) + ' --esborrar')
    comanda='|intensitat ' + txtIntensitat.get() + '|rainbowCycleTempsTotal ' + txtTempsIteracio.get() + ' ' + txtTempsTotal.get() 
    EnviarComandaAServidor(comanda)

def theaterChaseTempsTotal(event=None):
    comanda=''
    if chk_color_aleatori.get():
        #color_seleccionat = ' --color A '
        comanda+='|color A '
    else:
        #color_seleccionat = ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + ' '
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()

    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio theaterChaseTempsTotal --wait_ms ' + txtTempsIteracio.get() + ' --long ' + txtTempsTotal.get() + '  --intensitat  ' + str(int(txtIntensitat.get())+1) + ' --esborrar --subconjunt ' + txtSubconjunt.get() + ' ' + color_seleccionat)
    comanda+='|intensitat ' + txtIntensitat.get() + '|theaterChaseTempsTotal ' + txtTempsIteracio.get() + ' ' + txtTempsTotal.get() +' ' + txtSubconjunt.get()
    EnviarComandaAServidor(comanda)
    
    
def theaterChaseRainbow(event=None):
    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio theaterChaseRainbow --wait_ms ' + txtTempsIteracio.get() + ' --long ' + txtTempsTotal.get() + '  --intensitat  ' + str(int(txtIntensitat.get())+1) + ' --esborrar')
    comanda='|intensitat ' + txtIntensitat.get() + '|theaterChaseRainbow ' + txtTempsIteracio.get() + ' ' + txtTempsTotal.get() 
    EnviarComandaAServidor(comanda)



    
    
def netejarLedAdressable(event=None):
    EnviarComandaAServidor('|netejar ')
    
    
def omplirLedAdressable(event=None):
    comanda=''
    if chk_color_aleatori.get():
        comanda+='|color A '
    else:
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()
    comanda+='|intensitat ' + txtIntensitat.get() + '|omplir'
    EnviarComandaAServidor(comanda)
    
    
    
    
def creixerLedAdressable(event=None):
    comanda=''
    if chk_color_aleatori.get():
        #color_seleccionat = ' --color A '
        comanda+='|color A '
    else:
        #color_seleccionat = ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + ' '
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()

    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio creixer --long ' + txtTempsTotal.get() + ' --esborrar ' + color_seleccionat)
    comanda+='|creixer ' + txtTempsTotal.get()  
    EnviarComandaAServidor(comanda)

def decreixerLedAdressable(event=None):
    comanda=''
    if chk_color_aleatori.get():
        #color_seleccionat = ' --color A '
        comanda+='|color A '
    else:
        #color_seleccionat = ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + ' '
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()

    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio creixer --invers --long ' + txtTempsTotal.get() + ' --esborrar ' + color_seleccionat)
    comanda+='|decreixer ' + txtTempsTotal.get()  
    EnviarComandaAServidor(comanda)
   
def wipeLedAdressable(event=None):
    comanda=''
    if chk_color_aleatori.get():
        #color_seleccionat = ' --color A '
        comanda+='|color A '
    else:
        #color_seleccionat = ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + ' '
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()

    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio vano --subconjunt ' + txtSubconjunt.get() + ' --long ' + txtTempsTotal.get() + ' --esborrar ' + color_seleccionat)
    #print('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio vano --subconjunt ' + txtSubconjunt.get() + ' --long ' + txtTempsTotal.get() + ' --esborrar ' + color_seleccionat)
    comanda+='|intensitat ' + txtIntensitat.get() + '|vano ' + txtTempsTotal.get() + ' ' + txtSubconjunt.get() 
    EnviarComandaAServidor(comanda)
   
def incremental(event=None):
    comanda=''
    if chk_color_aleatori.get():
        #color_seleccionat = ' --color A '
        comanda+='|color A '
    else:
        #color_seleccionat = ' --colorR ' + str(int(txtR.get())+1) + ' --colorG ' + str(int(txtG.get())+1) + ' --colorB ' + str(int(txtB.get())+1) + ' '
        comanda+='|colorRGB ' + txtR.get() + ' ' + txtG.get() + ' ' + txtB.get()

    #stdin, stdout, stderr = client.exec_command('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio incrementalParts --subconjunt ' + txtSubconjunt.get() + ' --wait_ms ' + txtTempsIteracio.get() + ' --esborrar ' + color_seleccionat)
    #print('sh ' + killxevi +  ' xeviAnimacioLed && sudo python3 ' + xeviAnimacioLed + ' --animacio incrementalParts --subconjunt ' + txtSubconjunt.get() + ' --wait_ms ' + txtTempsIteracio.get() + ' --esborrar ' + color_seleccionat)
    comanda+='|intensitat ' + txtIntensitat.get() + '|incremental ' + txtTempsIteracio.get() + ' ' + txtSubconjunt.get() 
    EnviarComandaAServidor(comanda)
    
    
    
    
    
def chekAleatoriChange():    
    if chk_color_aleatori.get():
        txtR['fg']="grey"
        txtG['fg']="grey"
        txtB['fg']="grey"
        lblR['fg']="grey"
        lblG['fg']="grey"
        lblB['fg']="grey"
    else: 
        txtR['fg']="black"
        txtG['fg']="black"
        txtB['fg']="black"
        lblR['fg']="black"
        lblG['fg']="black"
        lblB['fg']="black"


def componentHex(valor):
    retorn = str(hex(int(valor)))[2:4]
    #print(valor, retorn, hex(int(valor)), hex (65))
    if len(retorn) == 1:
        return "0"+retorn
    else:
        return retorn

        
def ColorPredefinitChange(even):
    #print (choiceVar.get())
    #print(choices.where(choiceVar.get()))
    chk_color_aleatori.set(False)
    chekAleatoriChange()
    for index, item in enumerate(choices):
        if item == choiceVar.get():
            #print (item, index)
            #print (valorsRGB[index][0], valorsRGB[index][1],valorsRGB[index][2])
            txtR.delete(0, 'end')
            txtG.delete(0, 'end')
            txtB.delete(0, 'end')
            
            txtR.insert(tk.END,valorsRGB[index][0])
            txtG.insert(tk.END, valorsRGB[index][1])
            txtB.insert(tk.END, valorsRGB[index][2])
            
    button_mostrar_color.configure(bg = "#"  +  componentHex (txtR.get())  +   componentHex (txtG.get())   +   componentHex (txtB.get()) )
    #print()

    

def EnviarTextPantalla(even=None):    
    EnviarComandaAServidor('|PANTALLA cs:0,'+txtR.get()+','+txtG.get()+','+txtB.get())
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA tx:'+txtPantalla.get())

def EnviarTextComanda(even=None):    
    EnviarComandaAServidor(txtComanda.get())
    
def EnviarBanderaCat(even=None):        
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA ct:')
def EnviarBanderaGay(even=None):        
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA gy:')
def EnviarSmile(even=None):        
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA sm:9500')
def EnviarCountdown(even=None):        
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA cd:')
def EnviarRosa(even=None):      
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA rs:')
def EnviarAutomatic(even=None):      
    EnviarComandaAServidor('|PANTALLA in:'+txtIntensitat.get())
    EnviarComandaAServidor('|PANTALLA au:')
  


    
#FITXER_MP3=str(Path.home())+'.\\data\\FUMFUMFUM.mp3'
FITXER_MP3='.\\data\\FUMFUMFUM.mp3'
#FITXER_INSTRUCCIONS=str(Path.home())+'\\Downloads\\prova.time.xev'
FITXER_INSTRUCCIONS='.\\data\\FUMFUMFUM.time'
def menuObrirMp3():
    global FITXER_MP3
    FITXER_MP3 = filedialog.askopenfilename(initialdir = expanduser("~"),title = "Select MP3 file:",filetypes = (("mp3 files","*.mp3"),))
    #if not pygame.mixer.get_init():
    #    #pygame.mixer.pre_init(115000, -16, 2, 2048)
    #    pygame.mixer.init()
    
    pygame.mixer.music.load(FITXER_MP3)
    pygame.mixer.music.set_volume(0.3)

    #print (FITXER_MP3)
    
def menuObrirInstruccions():    
    global FITXER_INSTRUCCIONS
    FITXER_INSTRUCCIONS = filedialog.askopenfilename(initialdir = expanduser("~"),title = "Selecciona un fitxer amb instruccions:",filetypes = (("xev files","*.xev"),))
    
    file1 = open(FITXER_INSTRUCCIONS, 'r') 
    Lines = file1.readlines() 
    
    lbOrdres.delete(0,lbOrdres.size())
    for line in Lines: 
        lbOrdres.insert(tk.END,line )
    file1.close() 



def menuGuardarInstruccions():    
    global FITXER_INSTRUCCIONS
    #initialdir = expanduser("~")
    FITXER_INSTRUCCIONS = filedialog.asksaveasfilename(initialdir = FITXER_INSTRUCCIONS,title = "Indica el nom del fitxer amb instruccions a guardar:",filetypes = (("xev files","*.xev"),))
    print(FITXER_INSTRUCCIONS)

    
    file1 = open(FITXER_INSTRUCCIONS, 'w') 
    #for i, listbox_entry in enumerate(lbOrdres.get(0, tk.END)):
    for listbox_entry in lbOrdres.get(0, tk.END):
        file1.writelines(listbox_entry)
    file1.close() 


    

cuaOrdresUSB=Queue()
def procesSimularExecucio(pFitxerInstruccions, pFitxerMp3,tempsReproduccioAcomulat,eventInici,cuaOrdresUSB):

    global client
    global sock
    
    print(pFitxerInstruccions, pFitxerMp3,tempsReproduccioAcomulat)
    file1 = open(pFitxerInstruccions, 'r') 
    Lines = file1.readlines() 
    file1.close()
    
    INICIALITZACONNEXIONS()
    buscantInici=True
    
    #pygame.init()
    #pygame.mixer.pre_init(115000, -16, 2, 2048)
    pygame.mixer.init(frequency=48000)
    pygame.mixer.music.load(pFitxerMp3)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(start=tempsReproduccioAcomulat)  # start=POSICIO_MP3/1000
    eventInici.set()
    start_time = time.time()-tempsReproduccioAcomulat
    
    try:
        for lina in Lines:
            talls = lina.split()
            if len (talls)>1:
                temps = float(talls[0])

                #Esperem a poder executar la seguent comanda i de mentres revisem els botons USB 
                while  time.time() - start_time < temps:
                    buscantInici=False
                    time.sleep(0.05)
                    
                    if not cuaOrdresUSB.empty():
                        print("HEM REBUT UNA ORDRE PER USB !! ")
                        sock.sendall(bytearray(cuaOrdresUSB.get(), 'utf-8'))
                    
                                

                #És hora de executar una de les comandes predefinides
                if not buscantInici:
                    print(lina)
                    comanda = lina.split('#')[1]

                    if '|' in comanda:
                        sock.sendall(bytearray(comanda.strip(), 'utf-8'))
                    elif '@' in comanda:
                        print('És un comentari')
                    else:
                        stdin, stdout, stderr = client.exec_command(comanda)
    finally:
        #print("FINAL POSICIO PROCES: ",pygame.mixer.music.get_pos())
        client.close()
        sock.close()



def  MATAR_PROCES_SEGON_PLA():
    global procesSimular
    global client
    global sock
    global horaIniciReproducio
    
    
    #matem el possible procés que estigui simulant les instruccions actuals
    if procesSimular and procesSimular.is_alive():   
            #print("Hem matat el procés de simulació de segon pla")
            procesSimular.terminate();
            #print("Ens hem quedat a la marca de temps: ",time.time() - horaIniciReproducio )




            
UltimaOrdreExecutada=0
UltimaOrdreSeleccionada=-1
def seguirExecucioOrdres():
    global UltimaOrdreExecutada
    global horaIniciReproducio
    global tempsReproduccioAcomulat
    global UltimaOrdreSeleccionada
    
    # si estem executant el play faig el seguiment
    if horaIniciReproducio > 0:
        tempsSeguiment = tempsReproduccioAcomulat + time.time() - horaIniciReproducio
        posicio=0
        for i, listbox_entry in enumerate(lbOrdres.get(UltimaOrdreExecutada, tk.END)):
            comanda = listbox_entry.split()
            if len(comanda)> 5:
                if float(comanda[0]) < tempsSeguiment:
                    posicio=i
                else: 
                    #print(float(comanda[0]) , tempsSeguiment)
                    break
                
        UltimaOrdreExecutada = UltimaOrdreExecutada + posicio
        if UltimaOrdreExecutada > 0:
            if UltimaOrdreSeleccionada >= 0: lbOrdres.select_clear(UltimaOrdreSeleccionada)
            lbOrdres.selection_set(UltimaOrdreExecutada) 
            lbOrdres.see(UltimaOrdreExecutada+10) 
            UltimaOrdreSeleccionada = UltimaOrdreExecutada


        #actualitzem el comptador de temps actual
        txtTempsRepro.delete(0,tk.END)
        txtTempsRepro.insert(tk.END ,str(tempsSeguiment)[:str(tempsSeguiment ).find('.')+4])
        
        
        #crida recursiva cada 1 segon
        root.after(250, seguirExecucioOrdres)

    #reinicialitzem    
    else: UltimaOrdreSeleccionada=-1
        


def lbOrdresEsborrarFila(event):
    lbOrdres.delete(lbOrdres.curselection())

def lbSeleccionarTemps(event):
    if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
        print(lbOrdres.curselection())
        #agafem l'ultim element seleccionat, pot no ser el que ha seleccionat el usuari
        text = lbOrdres.get(lbOrdres.curselection()[-1]).split()
        if len(text) > 1:
            txtTempsRepro.delete(0,tk.END)
            txtTempsRepro.insert(tk.END ,text[0][:str(tempsReproduccioAcomulat).find('.')+4])
            #txtTempsRepro.insert(tk.END ,text[0][:6])

    
    
    
    
PLAY_MP3='OFF'    
procesSimular=None
tempsReproduccioAcomulat=0.0
horaIniciReproducio=time.time()
def buttonPlayPausePress(event=None):
    
    global FITXER_MP3
    global PLAY_MP3
    global POSICIO_MP3
    global procesSimular
    global tempsReproduccioAcomulat
    global horaIniciReproducio
    global UltimaOrdreExecutada
    global cuaOrdresUSB

    MATAR_PROCES_SEGON_PLA()
    
    if PLAY_MP3=='ON':
        print("Pausa")
        #print("Iteracio:" ,time.time() - horaIniciReproducio ,pygame.mixer.music.get_pos() )
        if  pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            #pygame.mixer.music.pause()
            #if tempsReproduccioAcomulat>0.0: 
            #    tempsReproduccioAcomulat = tempsReproduccioAcomulat -1.8
            #    print("resto")
            #tempsReproduccioAcomulat += pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.stop()
            #print("calculat el temps per aqui")
        tempsReproduccioAcomulat += time.time() - horaIniciReproducio 
        
        
        PLAY_MP3='PAUSE'
        buttonPlay.config(text="4")
        
        horaIniciReproducio=0
        print("Ens hem quedat a la marca de temps: ",tempsReproduccioAcomulat)
        txtTempsRepro.delete(0,tk.END)
        txtTempsRepro.insert(tk.END ,str(tempsReproduccioAcomulat)[:str(tempsReproduccioAcomulat).find('.')+4])

        #Seleccionem l'últim element executat
        pos_selected=0
        for i, listbox_entry in enumerate(lbOrdres.get(0, tk.END)):
            comanda = listbox_entry.split()
            if len(comanda)> 5:
                if float(comanda[0]) < tempsReproduccioAcomulat:
                    pos_selected=i
                else: break
        if pos_selected > 0:
            #lbOrdres.select_clear(0, "end")
            lbOrdres.selection_set(pos_selected) 
            lbOrdres.see(pos_selected) 
        
        INICIALITZACONNEXIONS()
        
        
    else:
        print("plaY")

        #deseleccionem tots els elements de la llista
        lbOrdres.select_clear(0, "end") 
        
        if pygame.mixer.get_init() is None:
            #pygame.mixer.pre_init(115000, -16, 2, 2048)
            pygame.mixer.init(frequency=48000)
            pygame.mixer.music.load(FITXER_MP3)
        
        buttonPlay.config(text=";")
        PLAY_MP3='ON'
        tempsReproduccioAcomulat= float(txtTempsRepro.get())
        
        if checkSimular.get() == 1:
            #TANCARCONNEXIONS()   # ens caldrà tancar la connexió del socket i la del USB
            sock.close()
            
            eventInici = Event()
            procesSimular = Process(target=procesSimularExecucio, args=(FITXER_INSTRUCCIONS,FITXER_MP3,tempsReproduccioAcomulat,eventInici,cuaOrdresUSB))
            procesSimular.start()
            
            #esperem que comenci a reproduir la música
            eventInici.wait()
        else:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(start=tempsReproduccioAcomulat)  # start=POSICIO_MP3/1000

        horaIniciReproducio=time.time()
        
        #entegem un timer que vagi seleccionant els elements que es van executant de la llista
        UltimaOrdreExecutada=0
        root.after(1000, seguirExecucioOrdres)

        #esborrem l'últim temps executat del timing
        txtTempsRepro.delete(0,tk.END)
        txtTempsRepro.insert(tk.END ,"")

        
        

                        
                    
                    
                
    
    
def buttonBackPress():
    global tempsReproduccioAcomulat
    tempsReproduccioAcomulat-=5
    if tempsReproduccioAcomulat < 0: tempsReproduccioAcomulat=0
    
    #pygame.mixer.music.set_pos(tempsReproduccioAcomulat)
    
    txtTempsRepro.delete(0,tk.END)
    txtTempsRepro.insert(tk.END ,str(tempsReproduccioAcomulat)[:str(tempsReproduccioAcomulat).find('.')+4])
    #txtTempsRepro.insert(tk.END ,tempsReproduccioAcomulat)
       

def buttonAbansarPress():
    global tempsReproduccioAcomulat
    print("abasar")
    tempsReproduccioAcomulat+=5
    
    txtTempsRepro.delete(0,tk.END)
    txtTempsRepro.insert(tk.END ,str(tempsReproduccioAcomulat)[:str(tempsReproduccioAcomulat).find('.')+4])
    #txtTempsRepro.insert(tk.END ,tempsReproduccioAcomulat)
    
    


def buttonStopPress():
    print("Stop")
    global PLAY_MP3
    global tempsReproduccioAcomulat
    global horaIniciReproducio

    if pygame.mixer.get_init():
        pygame.mixer.music.stop() 
    
    MATAR_PROCES_SEGON_PLA()    
        
    if PLAY_MP3=='ON':
        tempsReproduccioAcomulat += time.time() - horaIniciReproducio
    #pygame.mixer.music.rewind()
    
    buttonPlay.config(text="4")
    
    print("Ens hem quedat a la marca de temps: ",tempsReproduccioAcomulat)
    txtTempsRepro.delete(0,tk.END)
    txtTempsRepro.insert(tk.END ,str(tempsReproduccioAcomulat)[:str(tempsReproduccioAcomulat).find('.')+4])
    #txtTempsRepro.insert(tk.END ,tempsReproduccioAcomulat)
    tempsReproduccioAcomulat=0
    horaIniciReproducio=0
    
    PLAY_MP3='OFF'    
    
    INICIALITZACONNEXIONS()

    

    

    

    
    
    
#eventGestonarUSBBotons=None
def procesLlegirBotoneraUSB():
    global sock
    global connexioSerialUSB
    global procesSimular
    global configBotonera
    
    #la primera comanda la despreciem perquè pot arribar mitja comanda
    #comanda= connexioSerialUSB.readline().decode("utf-8") .rstrip("\r\n")
    if connexioSerialUSB is not None:
        try:
        #    while True:
            if connexioSerialUSB.inWaiting():
                comanda= connexioSerialUSB.readline().decode("utf-8") .rstrip("\r\n")
                print("-"+comanda+"-")
                
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
                        EnviarComandaAServidor(comanda)


            root.after(100, procesLlegirBotoneraUSB)
        except:
            print(sys.exc_info())  #[0]
            print("no consultarem més el USB")
        #finally:
        #    connexioSerialUSB.close()    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
        
        
    INICIALITZACONNEXIONS()
    
    
    col = 0
    fila = 0




    #Pintem la finestra windows 
    root = tk.Tk()
    root.title("Controladora de LEDS")
    root.geometry('1200x800')

    #Configuració de les dreceres de teclat
    root.bind('<F1>',PanicCelestialOff)
    root.bind('<F2>',PanicCelestialOn)
    
    
#    root.bind('q',ApagarGPIO)
#    root.bind('w',EncendreGPIO10)
#    root.bind('e',Encendre220vI2C15)
#    
#    root.bind('a',ApagarRGB)
#    root.bind('s',EncendreRGB)
#    root.bind('d',CreixerRGB)
#    root.bind('f',DecreixerRGB)
#    
#    root.bind('z',netejarLedAdressable)
#    root.bind('x',omplirLedAdressable)
#    root.bind('c',creixerLedAdressable)
#    root.bind('v',decreixerLedAdressable)
#    root.bind('b',wipeLedAdressable)
#    root.bind('n',incremental)
#    root.bind('m',rainbowTempsTotal)
#    root.bind(',',rainbowCycleTempsTotal)
#    root.bind('.',theaterChaseTempsTotal)
#    root.bind('-',theaterChaseRainbow)
#    
#    
#    root.bind('p',buttonPlayPausePress)

    
    #<Tab>
    #<Caps_Lock>
    
    
    
    
    
    #espai a la esquerra perquè no quedi tot enganxat
    frame = tk.Frame(root)
    frame.pack(fill="x",side=tk.LEFT, padx="20")



    frameLed = tk.Frame(root)
    frameLed.pack(side='left')

    frameTotal = tk.Frame(frameLed)
    frameTotal.pack(side='top')

    frame1Led = tk.Frame(frameLed)
    frameCanal = tk.Frame(frameLed)
    frameLedAddr = tk.Frame(frameLed)
    frame1Led.pack(side='top')
    frameCanal.pack(side='top')
    frameLedAddr.pack(side='top')

    #frameLedAddr1 = tk.Frame(frameLedAddr)
    #frameLedAddr1.pack(side='left')
    #frameLedAddr2 = tk.Frame(frameLedAddr)
    #frameLedAddr2.pack(side='left')



    buttonPANIC_Celestial = tk.Button(frameTotal, bg="white",text="Pànic Blanc")
    buttonPANIC_Celestial.bind('<ButtonPress>',PanicCelestialOn)
    buttonPANIC_Celestial.bind('<ButtonRelease>',PanicCelestialOff)
    buttonPANIC_Celestial.grid(column=col, row=fila)
    buttonPANIC_Celestial['font'] = font.Font(size=20)
    
    

    buttonPANIC_Infern = tk.Button(frameTotal, bg="white",text="Pànic Negre")
    buttonPANIC_Infern.bind('<ButtonPress>',PanicCelestialOff)
    buttonPANIC_Infern.grid(column=col+1, row=fila, padx=(50,0))
    buttonPANIC_Infern['font'] = font.Font(size=20)





    


    #btn_textEncendreGPIO10 = tk.StringVar()
    #buttonEncendreGPIO10 = tk.Button(frame1Led, 
    #                   textvariable=btn_textEncendreGPIO10,
    #                   command=EncendreGPIO10,                   
    #                   fg="black")
    #btn_textEncendreGPIO10.set("Encendre leds GPIO-10")
    #buttonEncendreGPIO10.grid(column=col, row=fila, pady=(40, 10))
    #fila = fila + 1

    btn_textEncendreI2C15 = tk.StringVar()
    buttonEncendreI2C15 = tk.Button(frame1Led, 
                       textvariable=btn_textEncendreI2C15,
                       command=Encendre220vI2C15,                   
                       fg="black")
    btn_textEncendreI2C15.set("Encendre 220v I2C (canal 15)")
    buttonEncendreI2C15.grid(column=col, row=fila, pady=(40, 5))
    col = col + 1

    btn_textEncendreI2C14 = tk.StringVar()
    buttonEncendreI2C14 = tk.Button(frame1Led, 
                       textvariable=btn_textEncendreI2C14,
                       command=Encendre220vI2C14,                   
                       fg="black")
    btn_textEncendreI2C14.set("Encendre 220v I2C (canal 14)")
    buttonEncendreI2C14.grid(column=col, row=fila, pady=(40, 5),padx=(20, 10))
    col = 0 
    fila = fila + 1
    btn_textEncendreI2C12 = tk.StringVar()
    buttonEncendreI2C12 = tk.Button(frame1Led, 
                       textvariable=btn_textEncendreI2C12,
                       command=Encendre220vI2C12,                   
                       fg="black")
    btn_textEncendreI2C12.set("Encendre 220v I2C (canal 12)")
    buttonEncendreI2C12.grid(column=col, row=fila, pady=(10, 10))
    col = col + 1

    btn_textEncendreI2C13 = tk.StringVar()
    buttonEncendreI2C13 = tk.Button(frame1Led, 
                       textvariable=btn_textEncendreI2C13,
                       command=Encendre220vI2C13,                   
                       fg="black")
    btn_textEncendreI2C13.set("Encendre 220v I2C (canal 13)")
    buttonEncendreI2C13.grid(column=col, row=fila, pady=(10, 10),padx=(20, 10))
    col = 0 
    fila = fila + 1




    sCanal = tk.StringVar()
    R1 = tk.Radiobutton(frameCanal, text="Tots", variable=sCanal, value='T')
    R1.grid(column=0, row=0, pady=(10, 40))
    R2 = tk.Radiobutton(frameCanal, text="Canal 1", variable=sCanal, value='1')
    R2.grid(column=1, row=0, pady=(10, 40))
    R3 = tk.Radiobutton(frameCanal, text="Canal 2", variable=sCanal, value='2')
    R3.grid(column=2, row=0, pady=(10, 40))
    R1.select()




#    buttonPolsRGBCanal1 = tk.Button(frame1Led, 
#                       text="Pols RGB color Aleatori", 
#                       fg="black")
#    buttonPolsRGBCanal1.bind('<ButtonPress>',RGBCanal1On)
#    buttonPolsRGBCanal1.bind('<ButtonRelease>',RGBCanal1Off)
#    buttonPolsRGBCanal1.grid(column=col, row=fila, pady=(40, 10))
#    fila = fila + 1




    buttonApagarRGB = tk.Button(frame1Led, 
                       text="Netejar RGB", 
                       command=ApagarRGB,              
                       fg="black")
    buttonApagarRGB.grid(column=col, row=fila, pady=(30, 10))
    col = col + 1


    buttonEncendreRGB = tk.Button(frame1Led, 
                       text="Encendre RGB (C)", 
                       command=EncendreRGB,              
                       fg="black")
    buttonEncendreRGB.grid(column=col, row=fila, pady=(30, 10),padx=(20, 10))
    col = 0 
    fila = fila + 1

    buttonCreixerRGB = tk.Button(frame1Led, 
                       text="Creixer RGB (TT, C)", 
                       command=CreixerRGB,              
                       fg="black")
    buttonCreixerRGB.grid(column=col, row=fila, pady=(0, 10))
    col = col + 1



    buttonDecreixerRGB = tk.Button(frame1Led, 
                       text="Decreixer RGB (TT, C)", 
                       command=DecreixerRGB,              
                       fg="black")
    buttonDecreixerRGB.grid(column=col, row=fila, pady=(0, 10),padx=(20, 10))
    fila = fila + 1




    

    button_netejarLedAdresable = tk.Button(frameLedAddr, 
                       text="Netejar", 
                       fg="black",
                       command=netejarLedAdressable)
    button_netejarLedAdresable.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1
    
    button_omplirLedAdresable = tk.Button(frameLedAddr, 
                       text="Omplir (C)", 
                       fg="black",
                       command=omplirLedAdressable)
    button_omplirLedAdresable.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1


    button_creixerLedAdressable = tk.Button(frameLedAddr, 
                       text="Creixer (TT, C)", 
                       fg="black",
                       command=creixerLedAdressable)
    button_creixerLedAdressable.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1

    button_decreixerLedAdressable = tk.Button(frameLedAddr, 
                       text="Decreixer (TT, C)", 
                       fg="black",
                       command=decreixerLedAdressable)
    button_decreixerLedAdressable.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1


    button_WipeLedAdressable = tk.Button(frameLedAddr, 
                       text="Vano (TT, SUB, C)", 
                       fg="black",
                       command=wipeLedAdressable)
    button_WipeLedAdressable.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1

    button_incremental = tk.Button(frameLedAddr,    # o rellotge de sorra
                       text="Incremental (TI, SUB, C)", 
                       fg="black",
                       command=incremental)
    button_incremental.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1


    buttonrainbow = tk.Button(frameLedAddr, 
                       text="rainbowTempsTotal (TT, TI, I)", 
                       fg="black",
                       command=rainbowTempsTotal)
    buttonrainbow.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1



    button_rainbowCycleTempsTotal = tk.Button(frameLedAddr, 
                       text="rainbowCycleTempsTotal (TT, TI, I)", 
                       fg="black",
                       command=rainbowCycleTempsTotal)
    button_rainbowCycleTempsTotal.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1

    button_theaterChaseTempsTotal = tk.Button(frameLedAddr, 
                       text="theaterChaseTempsTotal (TT, TI, SUB, C, I)", 
                       fg="black",
                       command=theaterChaseTempsTotal)
    button_theaterChaseTempsTotal.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1

    button_theaterChaseRainbow = tk.Button(frameLedAddr, 
                       text="theaterChaseRainbow (TT, TI, I)", 
                       fg="black",
                       command=theaterChaseRainbow)
    button_theaterChaseRainbow.grid(column=col, row=fila, pady=(0, 10))
    fila = fila + 1









    frameConfig = tk.Frame(root)
    frameConfig.pack(side='left')


    frame0 = tk.Frame(frameConfig)
    frame0.pack( )

    frame1 = tk.Frame(frameConfig)
    frame1.pack( )

    frame2 = tk.Frame(frameConfig)
    frame2.pack()

    frame3 = tk.Frame(frameConfig)
    frame3.pack()
    
    
    framePantalla = tk.Frame(frameConfig)
    framePantalla.pack()


    fila = 0
    col = 0
    lbOm = tk.Label(frame0, text="Color predefinit:")
    lbOm.grid(column=col, row=fila, pady=(0, 5))
    col = col + 1

    choiceVar = tk.StringVar()
    choices = ( "blanc", "vermell", "taronja", "groc", "verd clar", "verd fosc", "verd-blau", "blau-cel", "blauEsmortait", "blau", "lila", "rosa",  "gris")
    valorsRGB=((255,255,255),(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,0),(0,255,128),(0,255,255),(0,128,255),(0,0,255),(127,0,255),(255,0,255),(128,128,128))


    choiceVar.set(choices[0])
    om = tk.OptionMenu(frame0, choiceVar, *choices, command=ColorPredefinitChange)
    om.grid(column=col, row=fila,padx=(5, 0),pady=(0, 10))

    col = col + 1
    button_mostrar_color = tk.Button(frame0, text="          ")
    button_mostrar_color.grid(column=col, row=fila, padx=(20, 0), pady=(0, 10))



    fila = 0
    col = 0
    lblR = tk.Label(frame1, text="Red:")
    lblR.grid(column=col, row=fila,padx=(50, 0),)
    col = col + 1
    txtR = tk.Entry(frame1,width=5, justify=tk.RIGHT)
    txtR.insert(tk.END ,"255")
    txtR.grid(column=col, row=fila, padx=(5, 10), pady=(0, 0))
    col = col + 1

    lblG = tk.Label(frame1, text="Green:")
    lblG.grid(column=col, row=fila)
    col = col + 1
    txtG = tk.Entry(frame1,width=5, justify=tk.RIGHT)
    txtG.insert(tk.END ,"255")
    txtG.grid(column=col, row=fila, padx=(5, 10), pady=(0, 0))
    col = col + 1

    lblB = tk.Label(frame1, text="Blue:")
    lblB.grid(column=col, row=fila)
    col = col + 1
    txtB = tk.Entry(frame1,width=5, justify=tk.RIGHT)
    txtB.insert(tk.END ,"255")
    txtB.grid(column=col, row=fila, padx=(5, 10), pady=(0, 0))
    col = 0
    fila = fila + 1


    chk_color_aleatori = tk.BooleanVar()
    chk_color_aleatori.set(True) #set check state
    chkAleatori = tk.Checkbutton(frame2, text='Color Aleatori', var=chk_color_aleatori, command=chekAleatoriChange)
    chkAleatori.grid(column=col, row=fila)
    fila = fila + 1
    chekAleatoriChange()




    fila =0
    lblIntensitat = tk.Label(frame3, text="Intensitat:")
    lblIntensitat.grid(column=col, row=fila, pady=(40, 0))
    col = col + 1
    txtIntensitat = tk.Entry(frame3,width=5, justify=tk.RIGHT)
    txtIntensitat.insert(tk.END ,"255")
    txtIntensitat.grid(column=col, row=fila, padx=(5, 10), pady=(40, 0))



    fila = fila + 1
    col =0
    lblTempsTotal = tk.Label(frame3, text="Temps Total:")
    lblTempsTotal.grid(column=col, row=fila, padx=(25, 10), pady=(40, 10))
    col = col + 1
    txtTempsTotal = tk.Entry(frame3,width=5, justify=tk.RIGHT)
    txtTempsTotal.insert(tk.END ,"5000")
    txtTempsTotal.grid(column=col, row=fila, padx=(5, 10), pady=(40, 10))


    fila = fila + 1
    col =0
    lblTempsIteracio = tk.Label(frame3, text="Temps Iteració:")
    lblTempsIteracio.grid(column=col, row=fila, padx=(25, 10), pady=(0, 10))
    col = col + 1
    txtTempsIteracio = tk.Entry(frame3,width=5, justify=tk.RIGHT)
    txtTempsIteracio.insert(tk.END ,"50")
    txtTempsIteracio.grid(column=col, row=fila, padx=(5, 10), pady=(0, 10))
    col = col + 1

    fila = fila + 1
    col =0
    lblSubconjunt = tk.Label(frame3, text="Subconjunt:")
    lblSubconjunt.grid(column=col, row=fila, padx=(25, 10), pady=(0, 30))
    col = col + 1
    txtSubconjunt = tk.Entry(frame3,width=5, justify=tk.RIGHT)
    txtSubconjunt.insert(tk.END ,"3")
    txtSubconjunt.grid(column=col, row=fila, padx=(5, 10), pady=(0, 30))
    col = col + 1

    
    
    
    #enviar text A PANTALLA
    col =0
    fila = 0
    lblTextPantalla = tk.Label(framePantalla, text="Text:")
    lblTextPantalla.grid(column=col, row=fila,padx=(50, 0),)
    col = col + 1
    txtPantalla = tk.Entry(framePantalla,width=30, justify=tk.LEFT)
    txtPantalla.insert(tk.END ,"Feli# Sant Jordi")
    txtPantalla.grid(column=col, row=fila, padx=(5, 10), pady=(0, 0))
    col = col + 1
    
    button_enviarPantalla = tk.Button(framePantalla, 
                       text="Send", 
                       fg="black",
                       command=EnviarTextPantalla)
    button_enviarPantalla.grid(column=col, row=fila, pady=(0, 0))

    #enviar comanda al servidor
    col =0
    fila = 1
    lblComanda = tk.Label(framePantalla, text="Comanda:")
    lblComanda.grid(column=col, row=fila,padx=(50, 0), pady=(10, 0),)
    col = col + 1
    txtComanda = tk.Entry(framePantalla,width=30, justify=tk.LEFT)
    txtComanda.insert(tk.END ,"|PANTALLA ")
    txtComanda.grid(column=col, row=fila, padx=(5, 10), pady=(10, 0))
    col = col + 1
    
    button_enviarComanda = tk.Button(framePantalla, 
                       text="Send", 
                       command=EnviarTextComanda).grid(column=col, row=fila, pady=(10, 0))
    
    
    framePantallaBotons = tk.Frame(frameConfig)
    framePantallaBotons.pack()

    tk.Button(framePantallaBotons,text="ct", command=EnviarBanderaCat).grid(column=0, row=0, padx=(5, 0), pady=(10,0))
    tk.Button(framePantallaBotons,text="gy", command=EnviarBanderaGay).grid(column=1, row=0, padx=(5, 0), pady=(10,0))
    tk.Button(framePantallaBotons,text="sm", command=EnviarSmile     ).grid(column=2, row=0, padx=(5, 0), pady=(10,0))
    tk.Button(framePantallaBotons,text="cd", command=EnviarCountdown ).grid(column=3, row=0, padx=(5, 0), pady=(10,0))
    tk.Button(framePantallaBotons,text="rs", command=EnviarRosa      ).grid(column=4, row=0, padx=(5, 0), pady=(10,0))
    tk.Button(framePantallaBotons,text="au", command=EnviarAutomatic ).grid(column=5, row=0, padx=(5, 0), pady=(10,0))

    
    
    
    

    frameSimulador = tk.Frame(root)
    frameSimulador.pack(side="left",padx=(25,0))
    

    
    checkSimular = tk.IntVar()
    checkButtonSimular = tk.Checkbutton(frameSimulador, text = "Simular reproducció", variable = checkSimular, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
    checkButtonSimular.pack()
    checkSimular.set(1)

    #buttonOrdenar = tk.Button(frameSimulador, text="Ordenar Instruccions", command=buttonOrdenarPress)
    #buttonOrdenar.pack(pady=(0, 10))

    
    frameOrdres = tk.Frame(frameSimulador)
    frameOrdres.pack()

    lbOrdres = tk.Listbox(frameOrdres, selectmode='multiple',width=50, height=30)
    lbOrdres.bind('<Delete>',lbOrdresEsborrarFila)
    lbOrdres.bind("<<ListboxSelect>>", lbSeleccionarTemps)
    lbOrdres.pack(side="left", fill="y")
    
    scrollbarYOrdres = tk.Scrollbar(frameOrdres, orient="vertical")
    scrollbarYOrdres.config(command=lbOrdres.yview)
    scrollbarYOrdres.pack(side="left",fill="y" ) 
    
    lbOrdres.config(yscrollcommand=scrollbarYOrdres.set)
    lbOrdres.activate(1)


    


    frameReproductor = tk.Frame(frameSimulador)
    frameReproductor.pack()
    
    
    fila=0
    buttonRetrocedir = tk.Button(frameReproductor, text="7", command=buttonBackPress)
    buttonRetrocedir['font'] = font.Font(family='Webdings', size=20)
    buttonRetrocedir.grid(column=0, row=fila,pady=(20, 20),padx=(10, 10))

    buttonPlay = tk.Button(frameReproductor, text="4", command=buttonPlayPausePress)
    buttonPlay['font'] = font.Font(family='Webdings', size=20,)
    buttonPlay.grid(column=1, row=fila,pady=(20, 20),padx=(10, 10))
    col = col + 1
    
    #buttonPause = tk.Button(frameReproductor, text=";", command=buttonPausePress)
    #buttonPause['font'] = font.Font(family='Webdings', size=20)
    #buttonPause.grid(column=2, row=fila,pady=(20, 20),padx=(10, 10))

    buttonAbansar = tk.Button(frameReproductor, text="8", command=buttonAbansarPress)
    buttonAbansar['font'] = font.Font(family='Webdings', size=20)
    buttonAbansar.grid(column=2, row=fila,pady=(20, 20),padx=(10, 10))

    buttonStop = tk.Button(frameReproductor, text="n", command=buttonStopPress)
    buttonStop['font'] = font.Font(family='Wingdings', size=20)
    buttonStop.grid(column=3, row=fila,pady=(20, 20),padx=(10, 10))

    
    frameTempsIniciRepro = tk.Frame(frameSimulador)
    frameTempsIniciRepro.pack()
    
    
    lblTempsRepro = tk.Label(frameTempsIniciRepro, text="Temps actual:")
    lblTempsRepro.grid(column=0, row=0)
    col = col + 1
    txtTempsRepro = tk.Entry(frameTempsIniciRepro,width=10, justify=tk.RIGHT)
    txtTempsRepro.insert(tk.END ,"0")
    txtTempsRepro.grid(column=1, row=0, padx=(5, 10), pady=(0, 10))

    
    
    
    
    
    
    
    
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="ObrirMp3",command=menuObrirMp3)
    filemenu.add_command(label="Obrir Instruccions",command=menuObrirInstruccions)
    filemenu.add_command(label="Guardar Instruccions",command=menuGuardarInstruccions)
    #filemenu.add_separator()

    menubar.add_cascade(label="Menú", menu=filemenu)
    
  
    
    
    
    # A ESBORRAR !!! 
    file1 = open(FITXER_INSTRUCCIONS, 'r') 
    Lines = file1.readlines() 
    
    lbOrdres.delete(0,lbOrdres.size())
    for line in Lines: 
        lbOrdres.insert(tk.END,line )
    file1.close() 
    #FINAL A ESBORRAR !!!
    
    
    
    #eventGestonarUSBBotons = Event()
    #procesSimular = Process(target=procesLlegirBotoneraUSB, args=(eventGestonarUSBBotons,))
    #procesSimular.start()

    root.after(10000, procesLlegirBotoneraUSB)
    
    
    try:
        root.mainloop()

    except:
        TANCARCONNEXIONS()

    #procesSimular.kill()
    TANCARCONNEXIONS()
