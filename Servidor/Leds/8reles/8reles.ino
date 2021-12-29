/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/

#define PrimerPin 2
#define MAXPINS 8;

#define SERIAL_BAUD 1000000

//Cadena de caracters rebuda per el USB
char inputString[255] = "";

//String inputString = "";         // a String to hold incoming data
bool stringComplete = false;     // whether the string is complete


uint8_t NUMEROPINS =8;

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(SERIAL_BAUD);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }



  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  for (uint8_t i=0;  i < NUMEROPINS ; i++){
      pinMode(PrimerPin+i, OUTPUT);
  }

  Serial.println("Inicialització realitzada");
}



// the loop function runs over and over again forever
void loop() {


  if (not stringComplete) {
      //Mirem si ha arribat alguna comanada per USB a executar
      EventUSB();
  
  
  } else {
      stringComplete = false;
  
      Serial.println(inputString);
  
      if (inputString[2] == ':') {
  
        if (not CallFuncions(inputString[0], inputString[1])) {
          //  Serial.println("Rebut desconegut");
          ;
        }
  
      } else {
        Serial.println("No es instruccio");
      }
  }

  /*
  digitalWrite(PrimerPin, HIGH);
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(PrimerPin, LOW);
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second

*/
  
}

//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------

bool CallFuncions(char c1, char c2) {
 
  if (c1 == 'i' && c2 == 't' ) {
    Iterar();
  }

  //Canviar el nombre de reles
  else if (c1 == 'n' && c2 == 'r' ) {
    sscanf(&inputString[3], "%ul",  &NUMEROPINS);
    Serial.println(String("Canviat a ") + NUMEROPINS);
  }

  //on:x
  else if (c1 == 'o' && c2 == 'n' ) {
    uint8_t pinTractar;
    sscanf(&inputString[3], "%ul",  &pinTractar);
    digitalWrite(PrimerPin+pinTractar, HIGH);
  }

  //off:x
  else if (c1 == 'o' && c2 == 'f' ) {
    uint8_t pinTractar;
    sscanf(&inputString[3], "%ul",  &pinTractar);
    digitalWrite(PrimerPin+pinTractar, LOW);
  }

   //pb:   panic black
  else if (c1 == 'p' && c2 == 'b' ) {
      for (uint8_t i=0;i<NUMEROPINS;i++){
        digitalWrite(PrimerPin+i, LOW);
      }
  }


   //pw:   panic white
  else if (c1 == 'p' && c2 == 'w' ) {
      for (uint8_t i=0;i<NUMEROPINS;i++){
        digitalWrite(PrimerPin+i, HIGH);
      }
  }


}



void Iterar(){

  for (uint8_t i=0;i<NUMEROPINS;i++){
    int pinAnt = (i ==0) ? PrimerPin+NUMEROPINS-1 : PrimerPin+i-1;
    digitalWrite(pinAnt, LOW);
    digitalWrite(PrimerPin+i, HIGH);
    delay(1000);                       // wait for a second
  }

   digitalWrite(PrimerPin+NUMEROPINS-1, LOW);
}




/*

*/
boolean EventUSB() {

  if (stringComplete) return true;

  if (Serial.available()) {
    //Reinicialitzem del que haguem pogut llegir l'anterior vegada
    //inputString = "";
    uint8_t xInputString = 0;

    char inChar = (char)Serial.read();
    while (inChar != '\n') {
      // get the new byte:
      // add it to the inputString:
      //inputString += inChar;
      inputString[xInputString] = inChar;
      xInputString++;
      while (not Serial.available()) {
        ;
      }
      inChar = (char)Serial.read();
    }
    inputString[xInputString] = '\0';
    stringComplete = true;
    return true;
  }

  return false;
}
