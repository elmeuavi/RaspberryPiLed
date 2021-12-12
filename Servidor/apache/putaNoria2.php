
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



#$address="192.168.1.144";
$address="127.0.0.1";
$port="10000";

$sock=socket_create(AF_INET,SOCK_STREAM,0); # or die("Cannot create a socket");
#socket_connect($sock,$address,$port);# ; or die("Could not connect to the socket");
if (socket_connect($sock,$address,$port)){
    socket_write($sock,"|GPIO_ON 21");
    sleep(5);
    socket_write($sock,"|GPIO_OFF 21");
    
    socket_close($sock);
}

    
?>

<br><br>
<center><h1 style="font-size:80px">Gràcies per tocar la moral al papa !!</h1>

<div id="sfc1xtqxpxk9wfs6e2j9wkz5hkzstzm7unt"></div>
<script type="text/javascript" src="https://counter7.stat.ovh/private/counter.js?c=1xtqxpxk9wfs6e2j9wkz5hkzstzm7unt&down=async" async></script>



<img src='https://maestroferretero.es/storage/common/products/1000x1000/71685.jpg?v=1573825819'>
  </center>
</body>
</html>
