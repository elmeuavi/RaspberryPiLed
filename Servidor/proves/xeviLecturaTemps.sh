#!/bin/bash

#
# Executar comandes segons una línia de temps
#
# Execucio: bash xeviLecturaTemps.sh prova.time
# Exemple de fitxer "prova.time"
#   6.786 # |PanicBlanc
#   6.805 # gpio -g write 10 1
#   9.194 # |PanicBlack
#   9.278 # gpio -g write 10 0
#   11.945 # |color A |seleccionarTiraRGB 0,1,2,3,4,5 |intensitat 255|pintarTiraRGB
#   14.945 # |color A |intensitat 255|omplir
#   17.849 # |color A |intensitat 255|vano 5000 3
#   22.657 # |color A |intensitat 255|incremental 50 3
#   28.538 # |intensitat 255|theaterChaseRainbow 50 5000
#   33.961 # |PanicBlack
#   34.054 # gpio -g write 10 0



#EXEMPLE GRABACIÓ MUSICA des del windows (generar fitxer prova.time per reexecutar amb la comanda de sobre)
#     start 20201231ControladoraLedTCPIP.py && sleep 4 && start C:\Users\xbrunet\Videos\FUMFUMFUM.mp3

#EXEMPRE REPRODUIR
#     start cmd /C C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "bash /home/pi/rpi-ws281x-python/xevi/xeviLecturaTemps.sh /home/pi/rpi-ws281x-python/xevi/prova.time2" && sleep 4.8 && start C:\Users\xbrunet\Videos\PIMPIMPAMlent.mp3
#Alternatiu reproduir primer la música abans que els efectes
#     start C:\Users\xbrunet\Videos\FUMFUMFUM.mp3 && sleep 0 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "bash /home/pi/rpi-ws281x-python/xevi/xeviLecturaTemps.sh /home/pi/rpi-ws281x-python/xevi/prova.time"



exec 3<>/dev/tcp/localhost/10000


{  # això ès un TRY

	hora_inicial=$(($(date +%s%N)/1000000))
	
	inputFile=$1
	while IFS= read -r line
	do

	   line=$(echo "$line" | sed -e 's/#[ ]*/#/g' )
	   temps_transcorregut=$(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial )
	   tempsLlegit=$(echo ${line/./} | awk '{print $1}')
	   
	   if [ "x$(echo "$tempsLlegit" | sed -e 's/^[ ]*//g'  )" != "x" ]; then
		   while [ $temps_transcorregut -lt $tempsLlegit ] 
		   do
				sleep 0.01
				temps_transcorregut=$(expr  $(($(date +%s%N)/1000000)) '-' $hora_inicial )
		   done
		   
		   #echo $tempsLlegit  "is temps actual" 
		   
		   comanda=$(echo "$line" | awk -F "#" '{print $2;}' )
		   
		   primerCaracter=$(echo $comanda | cut -c 1-1 )
		   
		   if [ "$primerCaracter"  = "|" ]; then
			   echo $tempsLlegit "enviar a servidor $comanda "
			   echo "$comanda" 1>&3
		   elif [ "$primerCaracter"  = "@" ]; then
				# comentari
				echo $(echo ${line/./} | awk -F "@" '{print $2}')
		   else
			   echo $tempsLlegit "executar $comanda "
			   $comanda
		   fi
		else 
			# cadena buida de comanda
			echo -e "\n"  
		fi
	done < "$inputFile"

}  ||    { # your 'catch' block
    echo "hem capturat una interrupció del programa!! "
}  # això ès un final de un TRY/catch
 



#TANCAR LA CONNEXIO socket al servidor de LEDS localhost:10000 ...com si fos un finally. Ha d'estar després del final del TRY
exec 3<&-




#import pygame  # Load the popular external library
#pygame.init()
#pygame.mixer.init()
#pygame.mixer.music.load('C:\\Users\\xbrunet\\Videos\\FUMFUMFUM.mp3')
#pygame.mixer.music.rewind()
#pygame.mixer.music.play()
#
#while pygame.mixer.music.get_busy(): 
#    pygame.time.Clock().tick(10)
#    print(pygame.mixer.music.get_pos()+100)
