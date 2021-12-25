@echo off

rem set RASPBERRY=192.168.1.144
rem set RASPBERRY=192.168.43.240


FOR /f "tokens=* USEBACKQ" %%G IN (`powershell.exe "(ConvertFrom-StringData(Get-Content '.\configuracio.properties' -raw)).'raspberry.ip'"`) DO (
 set RASPBERRY=%%G
 goto CONTINUAR
)
:CONTINUAR



echo Incialitzem servidor de la raspberry %RASPBERRY%
start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@%RASPBERRY% "sudo python3 /home/pi/RaspberryPiLed/Servidor/Leds/SERVIDOR.py" 
rem start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@%RASPBERRY% "sh /home/pi/RaspberryPiLed/Servidor/Leds/setupTunel.bat" 

if exist %userprofile%\Documents\RaspberryPiLed\Remot\ControladoraLedTCPIP.py (
	cd %userprofile%\Documents\RaspberryPiLed\Remot\
	
	echo incialitzem servidor de Musica per Halloween
	start python MusicaPCLocal.py
	
	echo incialitzem controladora
	python ControladoraLedTCPIP.py
)

