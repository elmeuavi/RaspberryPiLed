start  %userprofile%\AppData\Roaming\AccessPaquets\plink.exe  -t -pw raspberry -ssh pi@192.168.1.144 "sudo python3 /home/pi/RaspberryPiLed/Servidor/Leds/SERVIDOR.py" 
sleep 1
if exist %userprofile%\Documents\RaspberryPiLed\Remot\ControladoraLedTCPIP.py (
	python %userprofile%\Documents\RaspberryPiLed\Remot\ControladoraLedTCPIP.py
)
if exist Y:\Remot\ControladoraLedTCPIP.py (
	python  Y:\Remot\ControladoraLedTCPIP.py
)