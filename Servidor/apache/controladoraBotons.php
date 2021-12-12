
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

	.grid-layout{
		display: grid;
		grid-template-columns: auto auto auto auto auto;
		background: ForestGreen;
		padding:20px;
		margin:20px;
		margin-top:40px;		 

		 //box-shadow: 2px 2px 2px 1px rgba(0, 0, 0, 0.2);
		 
		 //box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
		 border: 1px solid black;
		box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
		 
		 max-width: 800px;
		 text-align: left;
		 margin: 0px auto;
		 margin-bottom: 20px;
		 
	}
 
    .circle {
      width: 80;
      height: 80px;
	  border: 1px solid black;
      -webkit-border-radius: 40px;
      -moz-border-radius: 40px;
      border-radius: 40px;
	  margin:20px;
	  align-self: center;
	  justify-self: center;
	  
      background: red;

    }



</style>
  <meta charset="utf-8">
  
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
  
boto1="|activarCanalI2C 15"
boto1D="|desactivarCanalI2C 15"
boto2="|GPIO_ON 21"
boto2D="|GPIO_OFF 21"
boto3="|color A |intensitat 255|omplir"
boto3D=""


		TotParat=0;
		function PararhoTot(){
			TotParat=1;
			setTimeout(function(){ TotParat=0; }, 3000);
		}
		
		function FerAccio(boto){
			console.log(boto + " Apretat");
			if (TotParat==1) {console.log("Estem parats encara !!");return;}
			
			PararhoTot();
			console.log(eval("boto"+boto));
			setTimeout(function(){ FerAccioStop(boto) }, 6000);
			document.getElementById("quadre").src="controladoraBotonsFerAccio.php?accio="+encodeURI(eval("boto"+boto));
		}
		
		function FerAccioStop(boto){
			
			if (eval("boto"+boto+"D") != ""){
				console.log(boto + " DesApretat: " + eval("boto"+boto+"D"));
				document.getElementById("quadre").src="controladoraBotonsFerAccio.php?mostrar=N&accio="+encodeURI(eval("boto"+boto+"D"));
			} else {
				console.log("no hi ha acció de desapretar per el boto " + boto );
			}

		}

		
		function PintarBotons(){
			//taula de colors
			//https://www.w3schools.com/tags/ref_colornames.asp
			const arrayColor = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite"/*,"ForestGreen"*/,"Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed ","Indigo  ","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"];


			var els = document.getElementsByClassName("circle");
			[].forEach.call(els, function (el,index) { el.setAttribute("NBoto", index);el.style.background=arrayColor[Math.floor(Math.random() * arrayColor.length)]; /* console.log(el,index)*/} );
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
		
		
  </script>
  
 
</head>

<body onload="Javascript:init()">

<img src="https://esplaiespurnes.files.wordpress.com/2014/12/3-reis.jpg?w=1600&h=598&crop=1" width="100%">
<div class="grid-layout">

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

  <iframe id='quadre' onload="" frameBorder="0" width="100%"  height="500px"></iframe>


  <?php
if (false){
	$addressMusica="192.168.1.189";
	$port="20000";
	$sockMusica=socket_create(AF_INET,SOCK_STREAM,0);
	$tenimMusica = false;
	if (socket_connect($sockMusica,$addressMusica,$port)){
		$tenimMusica = true;
		socket_write($sockMusica,"musica orient");
		sleep(1);
		socket_close($sockMusica);
	}
		echo $tenimMusica;
}	
?>




</body>
</html>