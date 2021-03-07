#!/bin/sh


# start C:\Users\xbrunet\Videos\FUMFUMFUM.mp3 && sleep 0 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "sh /home/pi/rpi-ws281x-python/xevi/FumFumFum.sh"

#sh /home/pi/rpi-ws281x-python/xevi/killxevi.sh

gpio -g mode 10 out
cd /home/pi/rpi-ws281x-python/xevi

xeviEncenLedGPIO="sh ./lib/xeviEncenLedGPIO.sh"
xeviAnimacioLed="sudo python3 ./lib/xeviAnimacioLed.py"
#xeviAnimacioLed="sudo ./lib/xeviAnimacioLed"


hora_inicial=$(($(date +%s%N)/1000000))



FumFumFum()
{
	
	for i in 1 2
	do	
		$xeviEncenLedGPIO 10 0.08 &
		#sudo python3 xeviPintar.py --long 80 --color W --intensitat 20 --esborrar 
		$xeviAnimacioLed --animacio pintar --long 80 --color W --intensitat 20 --esborrar 
		sleep 0.2 
	done
	#sh ./lib/xeviEncenLedGPIO.sh 10 0.08 &
	##gpio write 23 1 && sleep 50 && gpio write 23 0 & 
	#sudo python3 xeviPintar.py --long 80 --color W  --intensitat 20 --esborrar 
	##gpio write 23 0
	#sleep 0.2 

	#gpio write 23 1
	$xeviEncenLedGPIO 10 0.3 &
	#gpio write 23 1 && sleep 50 && gpio write 23 0 & 
	#sudo python3 xeviPintar.py --long 300 --color R --esborrar --intensitat 60
	$xeviAnimacioLed --animacio pintar --long 300 --color R --esborrar --intensitat 60
	#gpio write 23 0
}



FumFumFum3()
{
	for i in 1 2
	do
		$xeviEncenLedGPIO 10 0.4 &
		#sudo python3 xeviPintar.py --long 200 --color W --intensitat 20 --esborrar 
		$xeviAnimacioLed --animacio pintar --long 400 --color W --intensitat 20 --esborrar 
		if [ $i -eq 1 ]; then sleep 0.6;  fi 
	done
	
	#$xeviEncenLedGPIO 10 0.2 &
	#sudo python3 xeviPintar.py --long 200 --color W  --intensitat 20 --esborrar 
	sleep 0.2 

	$xeviEncenLedGPIO 10 1.7 &
	#sudo python3 xeviPintar.py --long 1000 --color R --intensitat 60
	$xeviAnimacioLed --animacio pintar --long 1200 --color R --intensitat 60
	
	#sudo python3 creixer.py --long 700 --color R --invers --esborrar
	$xeviAnimacioLed --animacio creixer --color R --invers --long 700 --esborrar
}






Vers(){

	modeDebug=0

	
	echo Iteració $1 
	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial )
	
	
	#generació de nombres aleatoris entre 1 i 256
	#vermell=`shuf -i 1-256 -n 1`
	#verd=`shuf -i 1-256 -n 1`
	#blau=`shuf -i 1-256 -n 1`
	aleatori=`shuf -i 0-255 -n 1`
	vermell=`sh ./lib/generarColor.sh $aleatori | awk 'NR==1'`
	verd=`sh ./lib/generarColor.sh $aleatori | awk 'NR==2'`
	blau=`sh ./lib/generarColor.sh $aleatori | awk 'NR==3'`
	vermell=$( expr "$vermell" '+' 1 )
	verd=$( expr "$verd" '+' 1 )
	blau=$( expr "$blau" '+' 1 )
	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) color aleatori
	intensitat=58
	
	#echo color aleatori generat $vermell $verd $blau
	
	if [ $1 -eq 1 ]; then		
		#sudo python3 creixer.py --long 1300 --color B  --invers --esborrar
		$xeviAnimacioLed --animacio creixer --color B  --long 1300 --esborrar  
	else						
		#sudo python3 creixer.py --long 1600 --color B  --invers --esborrar
		$xeviAnimacioLed --animacio creixer --color B --long 1600 --esborrar  
   	fi
	
	sleep 0.5
	FumFumFum

	sleep 0.7
	#sudo python3 creixer.py --long 600 --color B  
	$xeviAnimacioLed --animacio creixer --color B --long 600  
	#sudo python3 creixer.py --long 800 --color B  --invers --esborrar
	$xeviAnimacioLed --animacio creixer --color B --invers --long 800 --esborrar  
	sleep 0.5
	FumFumFum

	sleep 0.7

	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "posició vano"  
	
	if [ "$modeDebug" -eq "1" ]; then   echo $xeviAnimacioLed --long 3000 --intensitat $intensitat --colorR $vermell --colorG $verd --colorB $blau ; fi
	if [ "$modeDebug" -eq "1" ]; then   echo $xeviAnimacioLed --long 3000 --color B --intensitat $intensitat --esborrar --colorRini $vermell --colorGini $verd --colorBini $blau; fi
	$xeviAnimacioLed --long 1500 --intensitat $intensitat --colorR $vermell --colorG $verd --colorB $blau 
	$xeviAnimacioLed --long 1500 --color A --intensitat $intensitat --esborrar --colorRini $vermell --colorGini $verd --colorBini $blau 

	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "posició dormir" 
	sleep 1

	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "posició segon vano" 
	$xeviAnimacioLed --long 1500 --intensitat $intensitat --colorR $vermell --colorG $verd --colorB $blau 
	$xeviAnimacioLed --long 1500 --color A --intensitat $intensitat --esborrar --colorRini $vermell --colorGini $verd --colorBini $blau 
	
	
	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "tirem el fum fum fum" 
	sleep 0.5
	FumFumFum
	
	sleep 0.5

	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "després de fum fum fum" 

	if [ $1 -eq 3 ]; then    durada=1700
	else 					 durada=1500
	fi
	$xeviAnimacioLed --long $durada --color G --intensitat $intensitat
	$xeviAnimacioLed --long 1500 --color B --intensitat $intensitat --esborrar --colorInicial G

	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "abans de descansar" 
	sleep 1

	$xeviAnimacioLed --long 1400 --color G --intensitat $intensitat
	$xeviAnimacioLed --long 1400 --color B --intensitat $intensitat --esborrar --colorInicial G
	
	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "tirem el fum fum fum segon" 		
	
	if [ $1 -eq 3 ]; then	
		sleep 1.1
		FumFumFum3
	else
		sleep 0.5
		FumFumFum
	fi
	echo $(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial ) "acabem !!" 	
}	


#INICI PROGRAMA PRINCIPAL !!!

Vers 1
sleep 1
Vers 2
sleep 1
Vers 3

#FINAL PROGRAMA PRINCIPAL !!!



