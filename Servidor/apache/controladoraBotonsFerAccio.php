
<html >
<head>

<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />

<style>

#comentari{
	font-size:30px
}

</style>
  <meta charset="utf-8">
  
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
	setTimeout(function(){ document.getElementById("comentari").style.display="none"; }, 3000);
  </script>
  
 
</head>

<body >
<div id="comentari">

	<?php


include 'config.php';

if ($config['apache']['EnviamentActiu'] == 0 ){
	echo "<div style='color: red'>Temporalment no disponible per manteniment o per acte reial</div><br>";
}else {

	if ($config['leds']['TunnelSSH'] ){
		#Executar la següent comanda a la rasberryPI
		#ssh -R 80:localhost:10000 localhost.run
		
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $config['TunnelSSH']['ip'] . urlencode($_GET["accio"]));
		curl_setopt($ch, CURLOPT_HEADER, false);

		curl_exec($ch);
		curl_close($ch);
		
	}else {	

		#$address="192.168.1.144";
		#$address="127.0.0.1";
		#$port="10000";
		
		//ini_set("default_socket_timeout", 10); 
		
		$sock=socket_create(AF_INET,SOCK_STREAM,0); # or die("Cannot create a socket");
		#socket_connect($sock,$address,$port);# ; or die("Could not connect to the socket");
		if (socket_connect($sock,$config['leds']['ip'],$config['leds']['port'])){
			socket_write($sock,$_GET["accio"]);
			socket_close($sock);
		}
	}
}



if (array_key_exists("comentari", $_GET)){
	   echo $_GET["comentari"];
}else  echo str_replace("|","<BR>",htmlspecialchars(substr($_GET["accio"],1)));

if (!array_key_exists("mostrar", $_GET) || $_GET["mostrar"] != 'N'){
	echo '<br>Espera ' . $config['apache']['tempsEntrePeticions'] . ' segons per obrir un altre botó';
}
		
	?>
	
</div>
</body>
</html>
