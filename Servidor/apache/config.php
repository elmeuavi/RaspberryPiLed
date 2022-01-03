<?php

//Fitxer de log de errors a     tail -f /var/log/apache2/error.log
//Fitxer de configuració a /etc/php/7.4/apache2/php.ini

    // Typical configuration file
	$config['musica']['ip']         	= '192.168.1.189';
	$config['musica']['port']         	= 20000;
	$config['musica']['actiu']          	= 0;
	
	$config['apache']['tempsEntrePeticions']  = 2;
	$config['apache']['tempsDuradaEvent']  	  = 6; 
	$config['apache']['maxCaractersText']  	  = 40; 
	$config['apache']['EnviamentActiu']  	  = 1; 
	



	#Executar la següent comanda a la rasberryPI
	#ssh -R 80:localhost:10000 localhost.run

	$config['TunnelSSH']['actiu']        	= 0;
	$config['TunnelSSH']['ip']        	= 'https://cc4cf23627ad2d.localhost.run/';
	

	$config['leds']['port']         	= 10000;
	
	//$config['leds']['ip']         	= '127.0.0.1';
	//$config['leds']['ip']                 = '10.8.0.10';
	$config['leds']['ip']         		= '192.168.1.144';
?>    
