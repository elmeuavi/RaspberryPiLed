#!/bin/sh
#primer pametre es el numero del pin GPIO
#segon pametre esl temps en que el led esta ences

# la opcio -g es perque agafi la anotacio GPIO o altrament dit BCM i no pas la wPi

#gpio readall

sleep 0.15
gpio -g write $1 1
sleep $2
gpio -g write $1 0
