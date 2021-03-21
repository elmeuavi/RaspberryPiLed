#include <stdlib.h>


//https://github.com/adafruit/Adafruit_NeoMatrix
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include "fontProgmem.h"


#define PIN 12
#define MATRIU_WIDTH 15
#define MATRIU_HEIGHT 10




//screenOffset must be ONE less than the bigest letter width
const byte screenOffset = 12;
byte posScreen = 0;
int screen[MATRIU_WIDTH + screenOffset];


//Cadena de caracters rebuda per el USB
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

//When i found a char to write, i will store there
int  fontAEscriure[13];
byte ampladaFontAEscriure;



Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(MATRIU_WIDTH, MATRIU_HEIGHT, PIN,
                            NEO_MATRIX_BOTTOM     + NEO_MATRIX_RIGHT +
                            NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
                            NEO_GRB            + NEO_KHZ800);
const uint16_t colors[] = {  matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255) };


byte matrixOrdenadaX[] =   {9, 10, 29, 30, 49, 50, 69, 70, 89, 90, 109, 110, 129, 130, 149,
                            8, 11, 28, 31, 48, 51, 68, 71, 88, 91, 108, 111, 128, 131, 148,
                            7, 12, 27, 32, 47, 52, 67, 72, 87, 92, 107, 112, 127, 132, 147,
                            6, 13, 26, 33, 46, 53, 66, 73, 86, 93, 106, 113, 126, 133, 146,
                            5, 14, 25, 34, 45, 54, 65, 74, 85, 94, 105, 114, 125, 134, 145,
                            4, 15, 24, 35, 44, 55, 64, 75, 84, 95, 104, 115, 124, 135, 144,
                            3, 16, 23, 36, 43, 56, 63, 76, 83, 96, 103, 116, 123, 136, 143,
                            2, 17, 22, 37, 42, 57, 62, 77, 82, 97, 102, 117, 122, 137, 142,
                            1, 18, 21, 38, 41, 58, 61, 78, 81, 98, 101, 118, 121, 138, 141,
                            0, 19, 20, 39, 40, 59, 60, 79, 80, 99, 100, 119, 120, 139, 140
                           };


/*

*/
void init_neomatrix() {

  //#include <Fonts/TomThumb.h>
  // matrix.setFont(&TomThumb);

  matrix.begin();
  matrix.setTextWrap(false);
  matrix.setBrightness(10);
  matrix.fillScreen(0);
  matrix.setTextColor(colors[0]);
  matrix.show();
}


//int x = matrix.width();
int x = MATRIU_WIDTH;
int pass = 0;

/*
 *Example of how to write using  nomatrix font
 *
  void iteracio_neomatrix(){

  matrix.fillScreen(0);
  matrix.setCursor(x, 1);
  //matrix.setTextSize(1);
  matrix.print(F("P E R E     M I Q U E L"));
  if(--x < int(sizeof("P E R E     M I Q U E L"))*int(-5)) {
    x = matrix.width();
    if(++pass >= 3) pass = 0;
    matrix.setTextColor(colors[pass]);
  }
  matrix.show();
  delay(100);

  }
*/


/*
 * 
 */
void setup() {

  Serial.begin(9600);
  delay(2000);


  init_neomatrix();



}







/*-------------------------------------------------------------
 *               MAIN FUNCTION
 *-------------------------------------------------------------
 */
void loop() {


  matrix.fillScreen(0);

  byte quinPixel = 0;
  for (int colunes = 0; colunes < MATRIU_WIDTH; colunes++) {
    for (int files = 0; files < MATRIU_HEIGHT; files++) {
      // Compare bits 7-0 in byte
      matrix.setPixelColor(matrixOrdenadaX[quinPixel], 255, 255, 255);

      quinPixel++;
      matrix.show();
      delay(10);
    }
  }





  EventUSB();

  if (stringComplete) {
    Serial.println(inputString);

    //escribim la frase rebuda
    for (auto i : inputString)  {
      if (cercarFont((char)i)) {
        encuarFontScreen();
        while (posScreen > 0) {
          //escriureScreenUSB();
          escriureScreenLedStrip();
          ferCorrerScreen();
          delay(50);
        }
      }
    }
    //fem que es netegi la matriu
    for (int i = 0; i < MATRIU_WIDTH; i++) {
      escriureScreenLedStrip();
      ferCorrerScreen();
      delay(50);
    }


    // clear the string:
    inputString = "";
    stringComplete = false;


  }

  //iteracio_neomatrix();


}




/*
   Iterar a trabés de les taules de amplades de fonts per trobar la que busquem
*/
boolean cercarFont(char pCaracter) {
  int iCaracter = pCaracter;

  //reinicialitzem les variables de font trobada de la llista
  ampladaFontAEscriure = 0;
  for ( int i = 0; i < 13; i++) {
    fontAEscriure[i] = 0;
  }


  for (byte i = 0; i < QuantesTaulesFonts; i++) {
    cercarFontLletres(i, TotesLesFontsQuantes[i], TotesLesFontsAmplada[i], iCaracter);
    if (ampladaFontAEscriure != 0) break;
  }

  return ampladaFontAEscriure > 0;
}

/*
   Iterar sobre una taula d'una amplada concret de font
*/
void cercarFontLletres(int quinaArray, byte pQuantesLLetres, byte pMidaLletres, int pCaracter) {

  for (byte lletra = 0; lletra < pQuantesLLetres; lletra++) {

    int posIni = (2 /*bytes*/ * lletra * (pMidaLletres + 1)); //apuntem al codi de caràcter
    if (pCaracter ==  pgm_read_word(   TotesLesFonts[quinaArray] + posIni   )    ) {
      posIni = posIni + 2; //Apuntem a la lletra
      ampladaFontAEscriure = pMidaLletres;
      for ( int i = 0; i < ampladaFontAEscriure; i++) {
        fontAEscriure[i] = pgm_read_word(   TotesLesFonts[quinaArray] + posIni + (i * 2)  );
      }
      break;
    }

  }


}

/*

*/
void encuarFontScreen() {

  for (byte i = 0; i < ampladaFontAEscriure; i++) {
    screen[MATRIU_WIDTH + i - 1] = fontAEscriure[i];
  }
  posScreen = ampladaFontAEscriure;
}

/*

*/
void escriureScreenUSB() {
  for (int colunes = 0; colunes < MATRIU_WIDTH + screenOffset; colunes++) {
    for (int bits = 9; bits > -1; bits--) {
      // Compare bits 7-0 in byte
      if (screen[colunes] & (1 << bits)) {
        Serial.print("1");
      }
      else {
        Serial.print(" ");
      }
    }
    Serial.print("\n");
  }
}
/*

*/
void escriureScreenLedStrip() {

  byte matrixOrdenada[] =  {149 , 148 , 147 , 146 , 145 , 144 , 143 , 142 , 141 , 140 ,
                            130 , 131 , 132 , 133 , 134 , 135 , 136 , 137 , 138 , 139 ,
                            129 , 128 , 127 , 126 , 125 , 124 , 123 , 122 , 121 , 120 ,
                            110 , 111 , 112 , 113 , 114 , 115 , 116 , 117 , 118 , 119 ,
                            109 , 108 , 107 , 106 , 105 , 104 , 103 , 102 , 101 , 100 ,
                            90  , 91  , 92  , 93  , 94  , 95  , 96  , 97  , 98  , 99  ,
                            89  , 88  , 87  , 86  , 85  , 84  , 83  , 82  , 81  , 80  ,
                            70  , 71  , 72  , 73  , 74  , 75  , 76  , 77  , 78  , 79  ,
                            69  , 68  , 67  , 66  , 65  , 64  , 63  , 62  , 61  , 60  ,
                            50  , 51  , 52  , 53  , 54  , 55  , 56  , 57  , 58  , 59  ,
                            49  , 48  , 47  , 46  , 45  , 44  , 43  , 42  , 41  , 40  ,
                            30  , 31  , 32  , 33  , 34  , 35  , 36  , 37  , 38  , 39  ,
                            29  , 28  , 27  , 26  , 25  , 24  , 23  , 22  , 21  , 20  ,
                            10  , 11  , 12  , 13  , 14  , 15  , 16  , 17  , 18  , 19  ,
                            9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , 0 ,
                           };

  matrix.setCursor(x, 1);
  matrix.fillScreen(0);


  byte quinPixel = 0;
  for (int colunes = 0; colunes < MATRIU_WIDTH; colunes++) {
    for (int files = MATRIU_HEIGHT - 1; files >= 0 ; files--) {
      // Compare bits 7-0 in byte
      if (screen[colunes] & (1 << files)) {
        matrix.setPixelColor(matrixOrdenada[quinPixel], 255, 255, 255);
      }
      else {
        matrix.setPixelColor(matrixOrdenada[quinPixel], 0, 0, 0);
      }

      quinPixel++;
    }
  }

  matrix.show();

}

/*

*/
void ferCorrerScreen() {
  for (int columna = 0; columna < MATRIU_WIDTH + screenOffset - 1; columna++) {
    screen[columna] = screen[columna + 1];
  }
  screen[MATRIU_WIDTH + screenOffset - 1] = 0;
  posScreen = posScreen - 1;
}



/*
   ONLY FOR DEBUG. WE DON'T USE IT
*/
void escriureLletraSeleccionada() {
  for (int colunes = 0; colunes < ampladaFontAEscriure; colunes++) {
    //Serial.println(fontAEscriure[colunes]);
    for (int bits = 9; bits > -1; bits--) {
      // Compare bits 7-0 in byte
      if (fontAEscriure[colunes] & (1 << bits)) {
        Serial.print("1");
      }
      else {
        Serial.print(" ");
      }
    }
    Serial.print("\n");
  }
}



/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.

  NOTE: The serialEvent() feature is not available on the Leonardo, Micro, or
  other ATmega32U4 based boards.
*/

void EventUSB() {

  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    Serial.print("REBUT:" + inChar);
    if (inChar == '\n') {
      stringComplete = true;
 //     Serial.println("HEM LLEGIT UNA LINIA");
 //     Serial.println(inputString);
    }

  }

}
