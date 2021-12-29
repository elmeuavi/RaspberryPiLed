<?php

//Fitxer de log de errors a     tail -f /var/log/apache2/error.log

    // Typical configuration file
	$config['musica']['ip']         	= '192.168.1.189';
	$config['musica']['port']         	= 20000;
	$config['musica']['actiu']          	= 0;

	//$config['leds']['ip']         	= '127.0.0.1';
	//$config['leds']['ip']                 = '10.8.0.10';
	$config['leds']['ip']         		= '192.168.1.144';
	$config['leds']['port']         	= 10000;

	$config['leds']['TunnelSSH']        	= 0;
?>    
