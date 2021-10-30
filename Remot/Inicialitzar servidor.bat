@echo off

echo incialitzem servidor de la raspberry
start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@192.168.1.144 "sudo python3 /home/pi/RaspberryPiLed/Servidor/Leds/SERVIDOR.py" 

if exist %userprofile%\Documents\RaspberryPiLed\Remot\ControladoraLedTCPIP.py (
	cd %userprofile%\Documents\RaspberryPiLed\Remot\
	
	echo incialitzem servidor de Musica per Halloween
	start python MusicaPCLocal.py
	
	echo incialitzem controladora
	python ControladoraLedTCPIP.py
)
