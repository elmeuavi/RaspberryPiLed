#!/bin/sh


# start C:\Users\xbrunet\Videos\PIMPIMPAMlent.mp3 && sleep 0 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "sh /home/pi/rpi-ws281x-python/xevi/PimPimPam.sh"


# start C:\Users\xbrunet\Videos\PIMPIMPAM.asx && sleep 0 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "sh /home/pi/rpi-ws281x-python/xevi/PimPimPam.sh"

# echo ^<Asx Version = "3.0"^> ^<Entry^> ^<StartTime value = "00:00:00.000" /^>     ^<Duration value = "00:05:00.000" /^> ^<Ref href = "C:\Users\xbrunet\Videos\PIMPIMPAMlent.mp3" /^>  ^</Entry^>  ^</Asx^> >> C:\Users\xbrunet\Videos\musica.asx && start C:\Users\xbrunet\Videos\musica.asx && sleep 0 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "sh /home/pi/rpi-ws281x-python/xevi/PimPimPam.sh"

# echo ^<Asx Version = "3.0"^> ^<Entry^> ^<Ref href = "C:\Users\xbrunet\Videos\PIMPIMPAMlent.mp3" /^>  ^</Entry^>  ^</Asx^> >> C:\Users\xbrunet\Videos\musica.asx && start C:\Users\xbrunet\Videos\musica.asx && sleep 0 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "sh /home/pi/rpi-ws281x-python/xevi/PimPimPam.sh"

gpio -g mode 10 out
cd /home/pi/rpi-ws281x-python/xevi


xeviEncenLedGPIO="sh ./lib/xeviEncenLedGPIO.sh"
xeviAnimacioLed="sudo python3 ./lib/xeviAnimacioLed.py"
xeviTiraRGB="sudo python3 ./lib/xeviTiraRGB.py"

intensitat=50



hora_inicial=$(($(date +%s%N)/1000000))



PimPimPam()
{

	if [ $1 -gt 8 ]; then    color=R
	else 					 color=B
	fi
	
	#sh ./lib/xeviEncenLedGPIO.sh 10 0.05 &
	#sudo python3 xeviPintar.py --long 50 --intensitat 50 --color $color --esborrar 
	$xeviAnimacioLed --animacio pintar --long 55 --intensitat $intensitat --color $color --esborrar 
	
	sleep 0.1
	
	#sh ./lib/xeviEncenLedGPIO.sh 10 0.05 &
	#sudo python3 xeviPintar.py --long 50 --intensitat 50 --color $color  --esborrar 
	$xeviAnimacioLed --animacio pintar --long 55 --intensitat $intensitat --color $color --esborrar 
	
	
	#gpio write 23 0
	$xeviTiraRGB --color W --long 100  --animacio pintar --intensitat 255 --esborrar &
	sleep 0.1 
	$xeviEncenLedGPIO 10 0.1 &
	#sudo python3 xeviPintar.py --long 100 --color W --esborrar --intensitat 20
	$xeviAnimacioLed --animacio pintar --long 100 --color W --esborrar --intensitat $intensitat
}

WeWillWeWill()
{

	color=G
	
	for i in 1 2
	do	
		$xeviTiraRGB --color $color --long 1400  --animacio creixer --intensitat 255 --esborrar &
		#sh ./lib/xeviEncenLedGPIO.sh 10 0.05 &
		#sudo python3 xeviPintar.py --long 600 --intensitat 10 --color $color 
		#sudo python3 xeviPintar.py --long 600 --intensitat 40 --color $color  --esborrar
		$xeviAnimacioLed --animacio pintar --long 1100 --intensitat $(expr $intensitat '/' 2) --color $color 
		$xeviAnimacioLed --animacio pintar --long 1100 --intensitat $intensitat --color $color  --esborrar
		
		if [ "$i" -eq "1" ]; then sleep 0.4; fi
		
	done	
	#	#sh ./lib/xeviEncenLedGPIO.sh 10 0.05 &
	#	sudo python3 xeviPintar.py --long 600 --intensitat 10 --color $color 
	#	sudo python3 xeviPintar.py --long 600 --intensitat 40 --color $color  --esborrar
	
	#gpio write 23 0
	
	
	
	sleep 0.1
	
	
	$xeviEncenLedGPIO 10 0.7 &
	$xeviAnimacioLed --animacio pintar --long 350 --color W --intensitat $(expr $intensitat '/' 3)
	$xeviAnimacioLed --animacio pintar --long 350 --color W --intensitat $intensitat --esborrar 

}



PimPimPamIntermig()
{
	#sudo python3 xeviPintar.py --long 100 --intensitat 30 --color R --esborrar 
	$xeviAnimacioLed --animacio pintar --long 100 --intensitat $intensitat --color R --esborrar 
	sleep 0.2
	#sudo python3 xeviPintar.py --long 100 --intensitat 30 --color R  --esborrar 
	$xeviAnimacioLed --animacio pintar --long 100 --intensitat $intensitat --color R  --esborrar 
	sleep 0.3 
	$xeviEncenLedGPIO 10 0.1 &
	#sudo python3 xeviPintar.py --long 100 --color W --esborrar --intensitat 30
	$xeviAnimacioLed --animacio pintar --long 150 --color W --esborrar --intensitat $intensitat
	sleep 0.6

}


for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16  
do
	if [ $i -eq 9 ]; then
		echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "Comença a xerrar"
	fi
	PimPimPam $i
	
	
	if [ $i -eq 12 ]; then
		sleep 0.50
#	elif [ $i -eq 16 ]; then
#		sleep 0.3
	else 
		sleep 0.70
	fi
	
done

#sleep 0.4

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "WeWillWeWill"

WeWillWeWill

sleep 0.15

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "PimPimPamIntermig"
PimPimPamIntermig

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "WeWillWeWill"

WeWillWeWill

sleep 0.5

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "WeWillWeWill"
PimPimPam

sleep 0.4

for i in 9 10 11 12 13 14 15 16  
do
	if [ $i -eq 9 ]; then
		echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "Comença a xerrar"
	fi
	PimPimPam $i
	
	
	if [ $i -eq 12 ]; then
		sleep 0.50
	elif [ $i -eq 16 ]; then
		sleep 0.3
	else 
		sleep 0.70
	fi
	
done

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "WeWillWeWill"

WeWillWeWill

sleep 0.15

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "PimPimPamIntermig"
PimPimPamIntermig

echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "WeWillWeWill"

WeWillWeWill

