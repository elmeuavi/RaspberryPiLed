#proces=`ps -efa | grep xevi | grep -e "rpi" -e "lib/" | awk '{print $2}' `
#echo $proces
#if [ -z $proces ]; then echo no trobem el proces; else sudo kill  -9 $proces ; fi


if [ ! -z "$1" ]; then 

	for PIDvalor in `ps -efa | grep  $1 | grep -v 'killxevi.sh' | awk '{print $2}' ` 
	do 
	   ps -efa | grep $PIDvalor | grep -v "grep $PIDvalor"
	   sudo kill -9 $PIDvalor 
	done 
	
else 
	for PIDvalor in `ps -efa | grep xevi | grep -v 'killxevi.sh' | grep -e "rpi" -e "lib/" | awk '{print $2}' `
	do
	   ps -efa | grep $PIDvalor | grep -v "grep $PIDvalor"
	   sudo kill -9 $PIDvalor
	done
	
fi


if [ -z $PIDvalor ]; then echo no trobem el proces; fi
