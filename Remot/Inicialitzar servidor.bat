@echo off

rem set RASPBERRY=192.168.1.144
rem set RASPBERRY=192.168.43.240



call:LlegirPropietat raspberry.ip RASPBERRY 
call:LlegirPropietat musica.actiu MUSICA
call:LlegirPropietat tunnelSSH.actiu TUNELSSH
call:LlegirPropietat tunnelSSH.actiu TUNELSSH
call:LlegirPropietat botonera.mode BOTONERA
echo RASPBERRY %RASPBERRY%
echo MUSICA %MUSICA%
echo BOTONERA '%BOTONERA%'


echo Incialitzem servidor de la raspberry %RASPBERRY%
start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@%RASPBERRY% "sudo python3 /home/pi/RaspberryPiLed/Servidor/Leds/SERVIDOR.py; read -p 'Press any key to resume ...'"   
timeout 5

if %TUNELSSH% EQU 1 (
	echo Inicialitzem el tunnel SSH
	start plink.exe  -t -pw raspberry  -no-antispoof -ssh pi@%RASPBERRY% "sh /home/pi/RaspberryPiLed/Servidor/Leds/setupTunel.bat; read -p 'Press any key to resume ...'"  
)else (
	echo NO inicialitzarem el tunnel SSH
)


if %BOTONERA% EQU 2 (
	echo Inicialitzem la botonera
	start cmd /c "python ClientPulsadorsRetroUSB.py & pause"
	timeout 5
)else (
	echo NO inicialitzarem la botonera
)


if exist %userprofile%\Documents\RaspberryPiLed\Remot\ControladoraLedTCPIP.py (
	cd %userprofile%\Documents\RaspberryPiLed\Remot\

	if %MUSICA% EQU 1 (
		echo incialitzem servidor de Musica
		start cmd /c "python MusicaPCLocal.py & pause"
	)else (
		echo NO inicialitzem la música
	)
	
	echo incialitzem controladora
	python ControladoraLedTCPIP.py 
)

goto:eof




:LlegirPropietat

FOR /f "tokens=* USEBACKQ" %%G IN (`powershell.exe "(Get-Content '.\configuracio.properties'  | Select-String -pattern @('^#', '^\[') -notMatch | ConvertFrom-StringData ).'%~1'"`) DO (
 set %~2=%%G
 goto CONTINUAR
)
:CONTINUAR
goto:eof