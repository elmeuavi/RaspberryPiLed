

# sh xeviAleatoriLedDireccionable.sh


velocitat=`shuf -i 1-5 -n 1`
echo velocitat $velocitat 

sudo python3 ./lib/xeviAnimacioLed.py --long $( expr "$velocitat" '*' 3000 ) --color A --esborrar --subconjunt `shuf -i 1-2 -n 1`

#sudo python3 xeviAnimacioLed.py --animacio theaterChaseIteracions --wait_ms 200 --long 10 --subconjunt 3 --color A --esborrar 
sudo python3 ./lib/xeviAnimacioLed.py --animacio theaterChaseTempsTotal --wait_ms 400 --long $( expr "$velocitat" '*' 5000 ) --subconjunt 3 --color A --esborrar 
#sudo python3 xeviAnimacioLed.py --animacio rainbowIteracions --wait_ms 20 --long 5 --esborrar 
sudo python3 ./lib/xeviAnimacioLed.py --animacio rainbowTempsTotal --wait_ms 20 --long $( expr "$velocitat" '*' 5000 ) --esborrar 
#sudo python3 xeviAnimacioLed.py --animacio rainbowCycleIteracions --wait_ms 20 --long 5 --esborrar 
sudo python3 ./lib/xeviAnimacioLed.py --animacio rainbowCycleTempsTotal --wait_ms 20 --long $( expr "$velocitat" '*' 5000 ) --esborrar 
sudo python3 ./lib/xeviAnimacioLed.py --animacio theaterChaseRainbow --wait_ms 100  --long $( expr "$velocitat" '*' 5000 ) --esborrar 
sudo python3 ./lib/xeviAnimacioLed.py --animacio pintar --color A --long $( expr "$velocitat" '*' 3000 ) --intensitat 100 --esborrar


	aleatori=`shuf -i 0-255 -n 1`
	vermell=`sh ./lib/generarColor.sh $aleatori | awk 'NR==1'`
	verd=`sh ./lib/generarColor.sh $aleatori | awk 'NR==2'`
	blau=`sh ./lib/generarColor.sh $aleatori | awk 'NR==3'`
	vermell=$( expr "$vermell" '+' 1 )
	verd=$( expr "$verd" '+' 1 )
	blau=$( expr "$blau" '+' 1 )

sudo python3 ./lib/xeviAnimacioLed.py --animacio creixer --colorR $vermell --colorG $verd --colorB $blau --long $( expr "$velocitat" '*' 3000 ) 
sudo python3 ./lib/xeviAnimacioLed.py --animacio creixer --colorR $vermell --colorG $verd --colorB $blau --invers --long $( expr "$velocitat" '*' 3000 ) --esborrar



sudo python3 ./lib/xeviAnimacioLed.py --animacio incrementalParts --wait_ms $( expr "$velocitat" '*' 80 ) --color A --long `shuf -i 1-4 -n 1` --esborrar 

