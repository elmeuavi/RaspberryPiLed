<?php 
//http://192.168.1.144/ReisMags/controladoraBotons.php

//Configurar a /etc/apache2/apache2.conf
//
//Alias /ReisMags /home/pi/RaspberryPiLed/Servidor/apache
//<Directory /home/pi/RaspberryPiLed/Servidor/apache>
//        AllowOverride None
//        Require all granted
//</Directory>




include 'config.php';

?>
<html >
<head>

<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />

<style>

	html {
		text-align: center;
		width: 100%; 
	}
	
	body{
		max-width: 800px;
		margin-left: auto;
		margin-right: auto;
	}
	img {mix-blend-mode: multiply;}
	.fosc{
		background-color:LightGray;
	}
	
	label, input{
		 font-size: 2em;
		 font-family: Arial, sans-serif
	}
	
	label img{
		vertical-align: middle
	}
	
	#EntradaText{
		margin-top: 60px;
	}
	input{
		margin-top: 20px;
		margin-bottom: 20px;
		font-size: 2em;
		font-family: Arial, sans-serif
	}

	.grid-layout{
		display: grid;
		grid-template-columns: auto auto auto auto auto;
		background: ForestGreen;
		padding:20px;
			 

		 //box-shadow: 2px 2px 2px 1px rgba(0, 0, 0, 0.2);
		 
		 //box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
		 border: 1px solid black;
		box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
		 
		 max-width: 800px;
		 text-align: left;
		 margin: 0px auto;
		 margin-bottom: 20px;
		 margin-top:20px;	
		 
	}
 
    .circle {
      width: 80;
      height: 80px;
	  //border: 1px solid black;
      -webkit-border-radius: 40px;
      -moz-border-radius: 40px;
      border-radius: 40px;
	  margin:20px;
	  align-self: center;
	  justify-self: center;
    }



	.Vermell	{ background: url("botons.png");  background-size: 393%;  	background-position:0% 0%	}
	.Verd		{ background: url("botons.png");  background-size: 393%;	background-position:50.5% 0%	}
	.BlauClar	{ background: url("botons.png");  background-size: 393%;	background-position:75% 0%	}
	.Groc		{ background: url("botons.png");  background-size: 393%;	background-position:0% 49.3%	}
	.Negre		{ background: url("botons.png");  background-size: 393%;	background-position:50.5% 49.3%	}
	.Blanc		{ background: url("botons.png");  background-size: 393%;	background-position:100% 49.3%	}
	.BlauFosc	{ background: url("botons.png");  background-size: 393%;	background-position:0% 100%	}
	.Taronja	{ background: url("botons.png");  background-size: 393%;	background-position:50.5% 100%	}
	.Rosa		{ background: url("botons.png");  background-size: 393%;	background-position:50.5% 0%	}
	

	.amagat   {display:none;visibility :hidden}
	.visible{}
	
	.error{ color: red ;font-size: 2em;}
	
	#resulatTextEntrat{margin-top:40px;	}



</style>
  <meta charset="utf-8">
  
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
  
boto0="|activarCanalI2C 12"
boto0D="|desactivarCanalI2C 12"
comentari0= "Encesa la llum de 12";
comentari0D="Apagada la llum de 12";

boto1="|activarCanalI2C 13"
boto1D="|desactivarCanalI2C 13"
comentari1= "Encesa la llum de 13";
comentari1D="Apagada la llum de 13";

boto2="|activarCanalI2C 14"
boto2D="|desactivarCanalI2C 14"
comentari2= "Encesa la llum de 14";
comentari2D="Apagada la llum de 14";

boto3="|activarCanalI2C 15"
boto3D="|desactivarCanalI2C 15"
comentari3= "Encesa la llum de 15";
comentari3D="Apagada la llum de 15";

boto4="|GPIO_ON 21"
boto4D="|GPIO_OFF 21"
comentari4= "Encesa la llum del pesebre";
comentari4D="Apagada la llum del pesebre";


boto5= "|color A |seleccionarTiraRGB 0 |intensitat 255|pintarTiraRGB"
boto5D="|seleccionarTiraRGB 0|netejarTiraRGB"
boto6= "|color A |seleccionarTiraRGB 1 |intensitat 255|pintarTiraRGB"
boto6D="|seleccionarTiraRGB 1|netejarTiraRGB"
boto7= "|color A |seleccionarTiraRGB 0,1 |intensitat 255|creixerTiraRGB 6000"
boto7D="|seleccionarTiraRGB 1|netejarTiraRGB"
boto8="|color A |seleccionarTiraRGB 0,1 |intensitat 255|decreixerTiraRGB 6000"
boto8D="|seleccionarTiraRGB 1|netejarTiraRGB"
boto9= "|color A |intensitat 255|omplir"
boto9D="|netejar"

boto10= "|color A |intensitat 255|vano 6000 3"
boto10D="|netejar"
boto11= "|color A |intensitat 255|incremental 5 2"
boto11D=""
boto12= "|intensitat 255|rainbowTempsTotal 10 10000"
boto12D=""
boto13= "|intensitat 255|rainbowCycleTempsTotal 10 10000"
boto13D=""
boto14= "|color A |intensitat 255|theaterChaseTempsTotal 80 6000 10"
boto14D="|netejar"


boto15= "|intensitat 255|theaterChaseRainbow 100 6000"
boto15D="|netejar"
boto16= "|PANTALLA in:150|PANTALLA ct:"
boto16D="|PANTALLA tx:"
boto17= "|PANTALLA in:150|PANTALLA gy:"
boto17D="|PANTALLA tx:"
boto18= "|PANTALLA in:150|PANTALLA sm:6000"
boto18D="|PANTALLA tx:"
boto19= "|PANTALLA in:150|PANTALLA cr:"
boto19D="|PANTALLA tx:"

boto20= "|RELES on: 0"
boto20D="|RELES of: 0"
boto21= "|RELES on: 1"
boto21D="|RELES of: 1"
boto22= "|RELES on: 2"
boto22D="|RELES of: 2"
boto23= "|RELES on: 3"
boto23D="|RELES of: 3"
boto24= "|RELES on: 4"
boto24D="|RELES of: 4"



boto25= "|PANTALLA cs:0,255,128,0|PANTALLA in:150|PANTALLA tx:En Fumera et veu quan fas malifetes"
boto25D=""
boto26= "|PANTALLA cs:0,0,255,255|PANTALLA in:150|PANTALLA tx:Cavalcada Reis CELRA 2022 "
boto26D=""
boto27= "|PANTALLA cs:0,0,255,128|PANTALLA in:150|PANTALLA tx:Portem molts regals per a tu"
boto27D=""
boto28= "|PANTALLA cs:0,0,255,0|PANTALLA in:150|PANTALLA tx:Aquest any t'has portat molt be"
boto28D=""
boto29= "|PANTALLA cs:0,255,255,255|PANTALLA in:150|PANTALLA tx:Visca els tres reis de l'orient!"
boto29D=""


		function EnviarTextPersonal(){
			document.getElementById("resulatTextEntrat").classList.add("visible");
			document.getElementById("EntradaText").classList.add("amagat");
				
			document.getElementById("resulatTextEntrat").classList.remove("amagat");
			document.getElementById("EntradaText").classList.remove("visible");
			
			document.getElementById("quadre").src="controladoraBotonsFerAccio.php?mostrar=N&accio="+encodeURI('|PANTALLA cs:0,255,255,255|PANTALLA in:150|PANTALLA tx:'+document.getElementById('TextEntrat').value.replace('|',''));
			
			setTimeout(function(){ 
				document.getElementById("resulatTextEntrat").classList.remove("visible");
				document.getElementById("EntradaText").classList.remove("amagat");
			
				document.getElementById("resulatTextEntrat").classList.add("amagat");
				document.getElementById("EntradaText").classList.add("visible");
				document.getElementById('TextEntrat').value = "";
			}, <?php echo((2  * $config['apache']['tempsDuradaEvent']) . '000'); ?>);
			
		}

		TotParat=0;
		function PararhoTot(){
			TotParat=1;
			
			document.getElementsByTagName("body")[0].classList.add("fosc");
			setTimeout(function(){ 
						TotParat=0; 
						document.getElementsByTagName("body")[0].classList.remove("fosc");
					}, <?php echo($config['apache']['tempsEntrePeticions'] . '000'); ?>);
		}
		
		function FerAccio(boto){
			
			console.log(boto + " Apretat");
			if (TotParat==1) {console.log("Estem parats encara !!");return;}

			
			PararhoTot();
			console.log(eval("boto"+boto));
			
			strComentari = "";
			if (eval("typeof  comentari"+boto +" !== 'undefined'") ){
				strComentari= "&comentari="+encodeURI(eval("comentari"+boto));
				console.log("COMENTARI "+boto+": " +eval("comentari"+boto));
			} else console.log("COMENTARI "+boto+": " + "ERROR NO HI HA COMENTARI");
			
			document.getElementById("quadre").src="controladoraBotonsFerAccio.php?accio="+encodeURI(eval("boto"+boto))+strComentari;
			setTimeout(function(){ FerAccioStop(boto) }, <?php echo($config['apache']['tempsDuradaEvent'] . '000'); ?>);

		}
		
		function FerAccioStop(boto){
			
			if (eval("boto"+boto+"D") != ""){
				console.log("DesApretat "+boto+": " + eval("boto"+boto+"D"));
				strComentari = "";
				if (eval("typeof  comentari"+boto +"D !== 'undefined'") ){
					strComentari= "&comentari="+encodeURI(eval("comentari"+boto+"D"));
					console.log("COMENTARI "+boto+"D: " + eval("comentari"+boto));
				} else console.log("COMENTARI "+boto+"D: " + "ERROR NO HI HA COMENTARI");
				document.getElementById("quadre").src="controladoraBotonsFerAccio.php?mostrar=N&accio="+encodeURI(eval("boto"+boto+"D"))+strComentari;
			} else {
				console.log("no hi ha acció de desapretar per el boto " + boto +"D");
			}

		}

		
		function PintarBotons(){
			//taula de colors
			//https://www.w3schools.com/tags/ref_colornames.asp
			//const arrayColor = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite"/*,"ForestGreen"*/,"Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed ","Indigo  ","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"];
			const arrayColor = ["Vermell","Negre","Verd","Groc","Vermell",
								"Taronja","Groc","Blanc","Taronja","BlauFosc",
								"BlauFosc","Vermell","BlauFosc","Groc","Verd",
								"Negre","Verd","Taronja","Negre","Blanc",
								"BlauFosc","Groc","Blanc","Vermell","Groc",
								"Taronja","Negre","Verd","BlauFosc","Blanc"]

			var els = document.getElementsByClassName("circle");
			//[].forEach.call(els, function (el,index) { el.setAttribute("NBoto", index);el.style.background=arrayColor[Math.floor(Math.random() * arrayColor.length)]; /* console.log(el,index)*/} );
			[].forEach.call(els, function (el,index) { 
										el.setAttribute("NBoto", index);
										el.setAttribute("role", "img text");
										el.classList.add(arrayColor[index]); /* console.log(el,index)*/
										el.setAttribute("title",eval("boto"+index));
			} );
		}		
		
		function init(){
			PintarBotons();

			//console.log(window.innerWidth);

			rect = document.getElementsByClassName("circle")[0].getBoundingClientRect();
			//console.log(rect.top, rect.right, rect.bottom, rect.left);
			rect1 = document.getElementsByClassName("circle")[1].getBoundingClientRect();
			//console.log(rect1.top, rect1.right, rect1.bottom, rect1.left);
			//console.log(rect1.left- rect.right );
			//rect2 = document.getElementsByClassName("circle")[5].getBoundingClientRect();
			//console.log(rect2.top, rect2.right, rect2.bottom, rect2.left);
			//console.log(rect2.top  - rect.bottom );

			document.getElementsByClassName("grid-layout")[0].style.gridRowGap  = rect1.left- rect.right -20 + "px";
			
			$(".circle").click(function(){FerAccio(this.getAttribute("NBoto"))});
		}
		

	const removeAccents = (str) => {
	  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
	} 
		
  </script>
  
 
</head>

<body onload="Javascript:init()" >

<img src="3-reis.jpg" width="100%" >

	<?php
if ($config['apache']['EnviamentActiu'] == 0 ){
	echo "<div class='error'>Temporalment no disponible per manteniment o per acte reial</div>";
}else {
	?>
	
	
<label for="botonera">Encen les llums per als Reis Mags: </label>
<div class="grid-layout" id="botonera">

<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>

</div>

<div id=EntradaText>
	<label for="TextEntrat">I també, diga'ns què vols que et portin els Reis: </label>
	<input type="text" name="TextEntrat" id="TextEntrat" maxlength="<?php echo($config['apache']['maxCaractersText']); ?>" size="<?php echo($config['apache']['maxCaractersText']); ?>" 
				onkeydown ="JavaScript:document.getElementById('quedenCaracters').innerHTML  = 'Queden ' + (document.getElementById('TextEntrat').getAttribute('maxlength') - document.getElementById('TextEntrat').value.length ) + ' caràcters màxim'"; document.getElementById('TextEntrat').innerHTML = document.getElementById('TextEntrat').value.substring(0,document.getElementById('TextEntrat').getAttribute('maxlength'));" 
				onfocusout="JavaScript:document.getElementById('quedenCaracters').innerHTML  = 'Queden ' + (document.getElementById('TextEntrat').getAttribute('maxlength') - document.getElementById('TextEntrat').value.length ) + ' caràcters màxim'";document.getElementById('TextEntrat').value = removeAccents(document.getElementById('TextEntrat').value)"></input><br>
	<div id="quedenCaracters">Queden <script>document.write(document.getElementById('TextEntrat').getAttribute("maxlength")); </script> caràcters màxim</div>
	<input type="button" value="Enviar" onclick="javascript:if (document.getElementById('TextEntrat').value.length > 0) EnviarTextPersonal()">
</div>
<div id="resulatTextEntrat" class="amagat"><label>Mira la pantalla&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Pixeles_de_telefono.jpg/220px-Pixeles_de_telefono.jpg"></label></div>

  <iframe id='quadre' onload="" frameBorder="0" width="100%"  height="300px"></iframe>
<?php
} //temporalment no disponible
?>

  <?php
	//ini_set("default_socket_timeout", 10); 
if ($config['musica']['actiu'] ){
	#$addressMusica="192.168.1.189";
	#$port="20000";
	$sockMusica=socket_create(AF_INET,SOCK_STREAM,0);
	$tenimMusica = false;
	if (socket_connect($sockMusica,$config['musica']['ip'],$config['musica']['port'])){
		$tenimMusica = true;
		socket_write($sockMusica,"musica orient");
		sleep(5);
		socket_close($sockMusica);
	}
	#echo $tenimMusica;
}	
?>





</body>
</html>