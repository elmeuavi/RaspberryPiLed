
<html >
<head>

<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />

<style>


</style>
  <meta charset="utf-8">
  
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  
  
 
</head>

<body>

  
  
  <?php

$addressMusica="192.168.1.189";
$port="20000";
$sockMusica=socket_create(AF_INET,SOCK_STREAM,0);
$tenimMusica = false;
if (socket_connect($sockMusica,$addressMusica,$port)){
    $tenimMusica = true;
     socket_write($sockMusica,"musica");
}


sleep(5);


#$address="192.168.1.144";
$address="127.0.0.1";
$port="10000";

$sock=socket_create(AF_INET,SOCK_STREAM,0); # or die("Cannot create a socket");
#socket_connect($sock,$address,$port);# ; or die("Could not connect to the socket");
if (!socket_connect($sock,$address,$port)){
    sleep(10);
}else {
   sleep(5); 
    socket_write($sock,"|PANTALLA in:90");
    socket_write($sock,"|PANTALLA cs:0,255,100,0");
    socket_write($sock,"|PanicBlack");
    sleep(1);
    socket_write($sock,"|PANTALLA cd:");
    sleep(2);
                socket_write($sock,"|colorRGB 255 0 0");
                socket_write($sock,"|seleccionarTiraRGB 1,2,3,4,5,6");
                socket_write($sock,"|intensitat 255");
                socket_write($sock,"|creixerTiraRGB 5000");
    socket_write($sock,"|colorRGB 255 0 0");
    socket_write($sock,"|creixer 8000");
    sleep(3);
    sleep(6);
    socket_write($sock,"|activarCanalI2C 13");
    socket_write($sock,"|PANTALLA tx:Wellcome to Halloween Home");
    sleep(1);
    socket_write($sock,"|activarCanalI2C 12");
    sleep(13);
    socket_write($sock,"|intensitat 255|rainbowTempsTotal 5 5000");
    
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|PANTALLA cs:0,0,255,100");
    socket_write($sock,"|PANTALLA tx:... pero la Castanyera mola mes !");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|intensitat 255|theaterChaseRainbow 50 15000");
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|PANTALLA gy:");
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|color A");
    socket_write($sock,"|pintarTiraRGB");
    sleep(1);
    socket_write($sock,"|PanicBlanc");
    sleep(2);
    socket_write($sock,"|desactivarCanalI2C 12");
    sleep(8);
    socket_write($sock,"|PanicBlack");
    socket_write($sock,"|colorRGB 0 0 255 |intensitat 255|omplir");
    socket_write($sock,"|colorRGB 0 0 0 |intensitat 255|vano 8000 2");
    sleep(1);
    socket_write($sock,"|PANTALLA cs:0,0,0,255");
    socket_write($sock,"|PANTALLA tx:Celra 2021");
    sleep(1);
    socket_write($sock,"|colorRGB 0 0 255|seleccionarTiraRGB 1,2,3,4,5,6");
    sleep(1);    
    socket_write($sock,"|intensitat 255|decreixerTiraRGB 4000");
    
    socket_close($sock);
    sleep(5);
}


if ($tenimMusica){
    socket_write($sockMusica,"stop");
    socket_close($sockMusica);
}
    
?>

<br><br>
<center><h1 style="font-size:80px">Feliç castanyada !!</h1>

<img src='https://agora.xtec.cat/escolariudor/wp-content/uploads/usu545/2020/10/48c115f91a1c7a0323b09220ada57d86.jpg'>
  </center>
</body>
</html>
