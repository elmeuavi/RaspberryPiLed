#/home/pi/RaspberryPiLed/Servidor/Leds

ps -efa | grep ssh | grep "localhost.run" 
pidMatar=`ps -efa | grep ssh | grep "localhost.run" | awk '{print $2}'`
echo $pidMatar
kill $pidMatar
sleep 3
ssh -R 80:localhost:10000 localhost.run



