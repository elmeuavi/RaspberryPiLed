
int PINS_UTILITZATS[]={2,3,4,5,6,7};
int ESTAT_ANTERIOR[][6]={{HIGH,HIGH,HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH}};

/*String NOM_BOTONS[4][4]={{"-","GROC","VERMELL","BUIT"},
                          {"NEGRE","-","BLAU",""},
                          {"VERD","","-",""},
                          {"","","","-"}};*/
/*String ACCIO_ALLIBERAR[4][4]={{"-","21","31","41","51","61"},                          
                              {"12","-","32","42","52","62"},
                              {"3","3","-","3","3","3"},
                              {"4","4","4","-","4","4",},
                              {"5","5","5","5","-","5",},
                              {"6","6","6","6","6","-",}};
/*String ACCIO_ALLIBERAR[4][4]={{"-",
                          "@21a",     //GROC
                          "@31a",  //VERMELL
                          "@41a"},   
                          
                          {"@12a",   //NEGRE
                          "-",
                          "@32a",    //BLAU
                          "@24a"},
                          
                          {"@13a\r\n|desactivarCanalI2C 15",    //VERD
                          "@23a",
                          "-",
                          "@34a"},
                          
                          {"@14a\r\ngpio -g write 10 0\n|PanicBlack",
                          "@42a",
                          "@43a",
                          "-"}};*/


/*
String ACCIO_APRETAR[4][4] ={{"-",
                          "@21\r\n|color A |intensitat 255|vano 5000 3",     
                          "@31\r\n|color A |seleccionarTiraRGB 0,1,2,3,4,5 |intensitat 255|pintarTiraRGB",  
                          "@41\r\n|color A |intensitat 255|theaterChaseTempsTotal 50 50000 3"},   
                          
                          {"@12\r\n|intensitat 255|rainbowTempsTotal 50 50000",   
                          "-",
                          "@32\r\n|color A |intensitat 255|omplir",     
                          "@24\r\n|color A |creixer 5000"},
                          
                          {"@13\r\n|activarCanalI2C 15",    
                          "@23\r\n|color A |decreixer 5000",
                          "-",
                          "@34\r\n|color A |intensitat 255|incremental 50 3"},
                          
                          {"@14\r\ngpio -g write 10 1\n|PanicBlanc",
                          "@42\r\n|intensitat 255|theaterChaseRainbow 50 10000",
                          "@43\r\n|color A |seleccionarTiraRGB 0,1,2,3,4,5 |intensitat 255|creixerTiraRGB 5000",
                          "-"}};
*/                          

void setup() {
  //start serial connection
  Serial.begin(9600);
  //configure pin 2 as an input and enable the internal pull-up resistor

  for (int i=0;i<6;i++){
    pinMode(PINS_UTILITZATS[i], INPUT_PULLUP);
  }

  Serial.println("@Inicialització realitzada");
}

void loop() {
String cadena="";
//pinMode(PINS_UTILITZATS[0], OUTPUT);
//digitalWrite(PINS_UTILITZATS[0], LOW);
//Serial.println(cadena +PINS_UTILITZATS[0] + " " + PINS_UTILITZATS[1] + " " +  digitalRead(PINS_UTILITZATS[1]));
  
 //  //read the pushbutton value into a variable
//  String cadena = "";
//  
  for (int i=0;i<6;i++){
     for (int j=0;j<6;j++){
        if (i != j){
//            //Serial.println(i);
//            //Serial.println(HIGH);
            pinMode(PINS_UTILITZATS[i], OUTPUT);
            digitalWrite(PINS_UTILITZATS[i], LOW);
            int sensorVal = digitalRead(PINS_UTILITZATS[j]);
            delay (10);
            //Serial.println(cadena +"Boto "+ PINS_UTILITZATS[i] + " "+ PINS_UTILITZATS[j]+ " " + sensorVal);
            if (ESTAT_ANTERIOR[i][j] != sensorVal){
                if (sensorVal == HIGH) {
                  //Serial.println(cadena +"Boto "+ PINS_UTILITZATS[i] + " "+ PINS_UTILITZATS[j]+ " " + sensorVal);
                  //Serial.println(ACCIO_ALLIBERAR[i][j]);
                  Serial.println(cadena+(i+1)+(j+1)+"a");
                }else {
                  //Serial.println(cadena +"Boto "+ (i+1) + " "+ (j+1)+ " APRETAT " + NOM_BOTONS[i][j]);
                  //Serial.println(ACCIO_APRETAR[i][j]);
                  Serial.println(cadena+(i+1)+(j+1));
                }
//
                ESTAT_ANTERIOR[i][j] = sensorVal;
            }
//            //if (sensorVal == HIGH) {
//               
//            //} else {
//            //   digitalWrite(13, HIGH);
//            //   Serial.println(cadena +"Boto "+ (i+1) + " "+ (j+1)+ " apretat");
//            //}
            pinMode(PINS_UTILITZATS[i], INPUT_PULLUP);
      }
     }
//    
//  
  }

}

//digitalWrite(13, LOW); led indicador de la placa
