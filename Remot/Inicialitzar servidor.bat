start  %userprofile%\AppData\Roaming\AccessPaquets\plink.exe  -t -pw raspberry -ssh pi@192.168.1.144 "sudo python3 /home/pi/RaspberryPiLed/Servidor/Leds/SERVIDOR.py" 
sleep 1
start %userprofile%\Documents\202101-python\GITRaspberryPiLed\Remot\ControladoraLedTCPIP.py