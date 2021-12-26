@echo off

rem set RASPBERRY=192.168.1.144
rem set RASPBERRY=192.168.43.240



call:LlegirPropietat raspberry.ip RASPBERRY 
call:LlegirPropietat musica.actiu MUSICA
call:LlegirPropietat tunnelSSH.actiu TUNELSSH

echo RASPBERRY %RASPBERRY%
echo MUSICA %MUSICA%


echo Incialitzem servidor de la raspberry %RASPBERRY%
start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@%RASPBERRY% "sudo python3 /home/pi/RaspberryPiLed/Servidor/Leds/SERVIDOR.py" 


if TUNELSSH EQU 1 (
	echo Inicialitzem el tunnel SSH
	start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@%RASPBERRY% "sh /home/pi/RaspberryPiLed/Servidor/Leds/setupTunel.bat" 
)else (
	echo NO inicialitzarem el tunnel SSH
)


if exist %userprofile%\Documents\RaspberryPiLed\Remot\ControladoraLedTCPIP.py (
	cd %userprofile%\Documents\RaspberryPiLed\Remot\

	if %MUSICA% EQU 1 (
		echo incialitzem servidor de Musica per Halloween
		start python MusicaPCLocal.py
	)else (
		echo NO inicialitzem la música
	)
	
	echo incialitzem controladora
	python ControladoraLedTCPIP.py
)

goto:eof




:LlegirPropietat

FOR /f "tokens=* USEBACKQ" %%G IN (`powershell.exe "(ConvertFrom-StringData(Get-Content '.\configuracio.properties' -raw)).'%~1'"`) DO (
 set %~2=%%G
 goto CONTINUAR
)
:CONTINUAR
goto:eof