
int PINS_UTILITZATS[]={3,4,5,6};
int ESTAT_ANTERIOR[4][4]={{HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH},
                          {HIGH,HIGH,HIGH,HIGH}};

String NOM_BOTONS[4][4]={{"-","GROC","VERMELL","BUIT"},
                          {"NEGRE","-","BLAU",""},
                          {"VERD","","-",""},
                          {"","","","-"}};

String ACCIO_APRETAR1[4][4]={{"-",
                          "|color A |intensitat 255|vano 5000 3",     //GROC
                          "gpio -g write 10 1\n|PanicBlanc",  //VERMELL
                          "BUIT"},   
                          {"|color A |intensitat 255|theaterChaseTempsTotal 50 50000 3",   //NEGRE
                          "-",
                          "|color A |seleccionarTiraRGB 0,1,2,3,4,5 |intensitat 255|pintarTiraRGB",     //BLAU
                          ""},
                          {"|intensitat 255|rainbowTempsTotal 50 50000",    //VERD
                          "",
                          "-",
                          ""},
                          {"",
                          "",
                          "",
                          "-"}};

String ACCIO_ALLIBERAR[4][4]={{"-",
                          "",     //GROC
                          "gpio -g write 10 0\n|PanicBlack",  //VERMELL
                          "BUIT"},   
                          {"",   //NEGRE
                          "-",
                          "",    //BLAU
                          //"|seleccionarTiraRGB 0,1,2,3,4,5|netejarTiraRGB",     //BLAU
                          ""},
                          {"",    //VERD
                          //{"|netejar",    //VERD
                          "",
                          "-",
                          ""},
                          {"",
                          "",
                          "",
                          "-"}};



String ACCIO_APRETAR[4][4]={{"-",
                          "//21",     //GROC
                          "//31",  //VERMELL
                          "//41"},   
                          {"//12",   //NEGRE
                          "-",
                          "//32",     //BLAU
                          "//24"},
                          {"//13",    //VERD
                          "//23",
                          "-",
                          "//34"},
                          {"//14",
                          "//42",
                          "//43",
                          "-"}};

void setup() {
  //start serial connection
  Serial.begin(9600);
  //configure pin 2 as an input and enable the internal pull-up resistor

  for (int i=0;i<4;i++){
    pinMode(PINS_UTILITZATS[i], INPUT_PULLUP);
  }

  Serial.println("Inicialització realitzada");
}

void loop() {
String cadena="";
//pinMode(PINS_UTILITZATS[0], OUTPUT);
//digitalWrite(PINS_UTILITZATS[0], LOW);
//Serial.println(cadena +PINS_UTILITZATS[0] + " " + PINS_UTILITZATS[1] + " " +  digitalRead(PINS_UTILITZATS[1]));
  
 //  //read the pushbutton value into a variable
//  String cadena = "";
//  
  for (int i=0;i<4;i++){
     for (int j=0;j<4;j++){
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
                  Serial.println(ACCIO_ALLIBERAR[i][j]);
                }else {
                  //Serial.println(cadena +"Boto "+ (i+1) + " "+ (j+1)+ " APRETAT " + NOM_BOTONS[i][j]);
                  Serial.println(ACCIO_APRETAR[i][j]);
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
