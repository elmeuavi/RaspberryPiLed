#!/bin/sh


# start C:\Users\xbrunet\Videos\DimoniEscuatLentl.mp3 && sleep 1 && C:\Users\xbrunet\AppData\Roaming\AccessPaquets\plink.exe 192.168.1.144 -l pi -pw raspberry "sh /home/pi/rpi-ws281x-python/xevi/DimoniEscuat.sh"


#https://www.youtube.com/watch?v=c98rN8n2PK8

gpio -g mode 10 out
cd /home/pi/rpi-ws281x-python/xevi

intensitat=10

sudo python3 ./lib/xeviAnimacioLed.py --animacio creixer --color A  --long 1800 --intensitat $intensitat
#--esborrar


for i in 1 2 3 
do

	sleep 0.2
	#sudo python3 ./lib/xeviAnimacioLed.py --animacio pintar --long 80 --color W --intensitat 20 --esborrar 
	sudo python3 ./lib/xeviAnimacioLed.py --animacio rainbowTempsTotal --wait_ms 20 --long 3600 --esborrar --intensitat $intensitat

	sleep 0.2
	sudo python3 ./lib/xeviAnimacioLed.py --animacio pintar --color A --long 400 --esborrar --intensitat $intensitat

	sleep 0.1
		aleatori=`shuf -i 0-255 -n 1`
		vermell=`sh ./lib/generarColor.sh $aleatori | awk 'NR==1'`
		verd=`sh ./lib/generarColor.sh $aleatori | awk 'NR==2'`
		blau=`sh ./lib/generarColor.sh $aleatori | awk 'NR==3'`
		vermell=$( expr "$vermell" '+' 1 )
		verd=$( expr "$verd" '+' 1 )
		blau=$( expr "$blau" '+' 1 )
	sudo python3 ./lib/xeviAnimacioLed.py --animacio creixer --colorR $vermell --colorG $verd --colorB $blau  --long 600 --invers --intensitat $intensitat


done

sleep 0.1

sudo python3 ./lib/xeviAnimacioLed.py --animacio creixer --color A  --long 2000 --invers --intensitat $intensitat