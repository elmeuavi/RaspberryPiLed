#!/bin/sh

#sudo pip3 install pyinstaller
#sudo pyinstaller xeviAnimacioLed.py --onefile

cd /home/pi/rpi-ws281x-python/xevi/lib/
sudo rm -R TMP_compilar

mkdir TMP_compilar
cp funcions.py ./TMP_compilar/
cp generarColor.sh ./TMP_compilar/
cp parametres.py ./TMP_compilar/
cp xeviAnimacioLed.py ./TMP_compilar/
cp xeviTiraRGB.py ./TMP_compilar/

cd ./TMP_compilar/
echo .
echo .
echo .
sudo pyinstaller xeviAnimacioLed.py --onefile
echo .
echo .
echo .
echo .
echo .
echo .

sudo pyinstaller xeviTiraRGB.py --onefile

cd ..
echo .
echo .
echo actualitzant xeviAnimacioLed
cp ./TMP_compilar/dist/xeviAnimacioLed ./

echo .
echo .
cp ./TMP_compilar/dist/xeviTiraRGB ./

