#include <stdlib.h>


//https://github.com/adafruit/Adafruit_NeoMatrix
// Only use this functions or Serial will not work:
//https://github.com/adafruit/Adafruit_NeoMatrix/blob/master/Adafruit_NeoMatrix.h
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>



//#include "smileytongue24.h"

//generated by the other program. You cal also use main Adafruit letters (less dificult)
#include "fontProgmem.h"

#define PIN 10
#define MATRIU_WIDTH 29
#define MATRIU_HEIGHT 10

//ALERT: DEFAULT VALUE IS 9600
//#define SERIAL_BAUD 115200
#define SERIAL_BAUD 1000000








//screenOffset must be ONE less than the bigest width letter
#define screenOffset 12
byte posScreen = 0;
int screen[MATRIU_WIDTH + screenOffset];


//Cadena de caracters rebuda per el USB
char inputString[255] = "";


//String inputString = "";         // a String to hold incoming data
bool stringComplete = false;     // whether the string is complete

//When i found a char to write, i will store there
int  fontAEscriure[13];
byte ampladaFontAEscriure;


#define LED_BLACK    0

#define LED_RED_VERYLOW   (3 <<  11)
#define LED_RED_LOW     (7 <<  11)
#define LED_RED_MEDIUM    (15 << 11)
#define LED_RED_HIGH    (31 << 11)

#define LED_GREEN_VERYLOW (1 <<  5)
#define LED_GREEN_LOW     (15 << 5)
#define LED_GREEN_MEDIUM  (31 << 5)
#define LED_GREEN_HIGH    (63 << 5)

#define LED_BLUE_VERYLOW  3
#define LED_BLUE_LOW    7
#define LED_BLUE_MEDIUM   15
#define LED_BLUE_HIGH     31

#define LED_ORANGE_VERYLOW  (LED_RED_VERYLOW + LED_GREEN_VERYLOW)
#define LED_ORANGE_LOW    (LED_RED_LOW     + LED_GREEN_LOW)
#define LED_ORANGE_MEDIUM (LED_RED_MEDIUM  + LED_GREEN_MEDIUM)
#define LED_ORANGE_HIGH   (LED_RED_HIGH    + LED_GREEN_HIGH)

#define LED_PURPLE_VERYLOW  (LED_RED_VERYLOW + LED_BLUE_VERYLOW)
#define LED_PURPLE_LOW    (LED_RED_LOW     + LED_BLUE_LOW)
#define LED_PURPLE_MEDIUM (LED_RED_MEDIUM  + LED_BLUE_MEDIUM)
#define LED_PURPLE_HIGH   (LED_RED_HIGH    + LED_BLUE_HIGH)

#define LED_CYAN_VERYLOW  (LED_GREEN_VERYLOW + LED_BLUE_VERYLOW)
#define LED_CYAN_LOW    (LED_GREEN_LOW     + LED_BLUE_LOW)
#define LED_CYAN_MEDIUM   (LED_GREEN_MEDIUM  + LED_BLUE_MEDIUM)
#define LED_CYAN_HIGH   (LED_GREEN_HIGH    + LED_BLUE_HIGH)

#define LED_WHITE_VERYLOW (LED_RED_VERYLOW + LED_GREEN_VERYLOW + LED_BLUE_VERYLOW)
#define LED_WHITE_LOW   (LED_RED_LOW     + LED_GREEN_LOW     + LED_BLUE_LOW)
#define LED_WHITE_MEDIUM  (LED_RED_MEDIUM  + LED_GREEN_MEDIUM  + LED_BLUE_MEDIUM)
#define LED_WHITE_HIGH    (LED_RED_HIGH    + LED_GREEN_HIGH    + LED_BLUE_HIGH)




Adafruit_NeoMatrix *matrix = new Adafruit_NeoMatrix(MATRIU_WIDTH, MATRIU_HEIGHT, PIN,
    //NEO_MATRIX_BOTTOM     + NEO_MATRIX_RIGHT +
    NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
    NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
    NEO_GRB            + NEO_KHZ800);


//Foreground, background, aux1, aux2
uint16_t colors[3] = {LED_WHITE_HIGH, LED_BLACK, LED_GREEN_HIGH};




/*

*/
void init_neomatrix() {

  matrix->begin();
  //matrix->setFont(&TomThumb);
  //matrix->setTextWrap(false);
  matrix->setBrightness(10);
  //Show withe screen for 3 secons to ensure all is ok at init
  matrix->fillScreen(LED_WHITE_HIGH);
  matrix->show();
  delay(2000);
  matrix->clear();
  matrix->show();


}

/*
  #include <Fonts/TomThumb.h>
  int x = MATRIU_WIDTH;
  int pass = 0;
  //
  // Example of how to write using  nomatrix font
  //
  void iteracio_neomatrix(String pText, uint16_t llargada) {

  matrix->fillScreen(0);
  matrix->setCursor(x, 1);
  //matrix->setTextSize(1);
  //matrix->print(F("P E R E     M I Q U E L"));
  matrix->print(pText);
  //if (--x < int(sizeof("P E R E     M I Q U E L"))*int(-5)) {
  //if (--x < int(sizeof(pText)*int(-5))) {
  if (--x < -int(llargada)) {
    x = matrix->width();
    if (++pass >= 3) pass = 0;
    matrix->setTextColor(colors[pass]);
  }
  matrix->show();
  delay(100);

  }
*/





/*

*/
void setup() {

  Serial.begin(SERIAL_BAUD);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  init_neomatrix();

  Serial.println("Inicialització realitzada");

}



/*
  int iteracio = 0;
  String cadenes[] = {"ct:", ":gy", "t:PERE", "t:MIQUEL", "sm:", "cb:255,0,0","fl:"};
*/
/*-------------------------------------------------------------
                 MAIN FUNCTION
  -------------------------------------------------------------
*/
void loop() {



  if (not stringComplete) {
    //Mirem si ha arribat alguna comanada per USB a executar
    EventUSB();


  } else {
    stringComplete = false;
    
    Serial.println(inputString);
    
    if (inputString[2] == ':') {
      
      
      if (inputString[0] == 'c' ){
      
              
        //COUNT DOWN
        /*} else */if ( inputString[1] == 'd' ) {
          CompteEnrere();
          
        //CATALONIA FLAG
        } else if (inputString[1] == 't' ) {
          Catalunya();

        //COLORS SELECT
        } /*else if(inputString[1] == 's' ) {
              llegirColor();
        }*/
/*
      

      //Emplena la pantalla amb el color de fondo
      }else if (inputString[0] == 'f' && inputString[1] == 'l' ) {
            Serial.println("Rebut omplir");
            matrix->fillScreen(colors[1]);
            matrix->show();
/*        
      //pixel a pixel
      } else if (inputString[0] == 'f' && inputString[1] == 'c' ) {
        PixelAPixel();*/


      //WRITE A TEXT
    }else if (inputString[0] == 't' && inputString[1] == 'x') {
        if (inputString[2] != '\0') {
          Serial.println("Rebut text");
          writeText();

          //If don't have a new instruction that cuts this one
          if (!stringComplete) {
            //ask for more text
            Serial.println("+");
          }
        }


      //SMILE
      } else if (inputString[0] == 's' && inputString[1] == 'm' ) {
        Somriu();


      //GAY FLAG
      } else if (inputString[0] == 'g' && inputString[1] == 'y' ) {
        Gay();




      } else {
        Serial.println("Rebut desconegut");
      }
    }else {
        Serial.println("No es instruccio");
    }
  }


}



//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------


void llegirColor() {
  int quin = 0;
  int valorR = 0;
  int valorG = 0;
  int valorB = 0;

  int n = sscanf(&inputString[3], "%d,%d,%d,%d", &quin, &valorR, &valorG, &valorB);
  /*Serial.println(valorR);
  Serial.println(valorG);
  Serial.println(valorB);*/
  colors[quin] = matrix->Color(valorR, valorG, valorB);
}

//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
/*
void PixelAPixel() {
  Serial.println("Rebut fc");
  matrix->fillScreen(colors[1]);
  for (uint8_t i = 0; i < MATRIU_HEIGHT ; i++) {
    for (uint8_t j = 0; j < MATRIU_WIDTH ; j++) {
      matrix->drawPixel(j, i, colors[0]);
      matrix->show();
      delay(10);
    }
  }
}*/
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
void Catalunya() {

  Serial.println("Rebut Catalunya");

  matrix->fillScreen(0);
  for (byte i = 0; i < 7; i = i + 2) {
    matrix->drawFastHLine(0, i, MATRIU_WIDTH, matrix->Color(255, 255, 0));
    matrix->drawFastHLine(0, i + 1, MATRIU_WIDTH, matrix->Color(255, 0, 0));
  }
  matrix->drawFastHLine(0, 8, MATRIU_WIDTH, matrix->Color(255, 255, 0));

  matrix->drawFastVLine(0, 0, 9, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(1, 0, 9, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(2, 1, 7, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(3, 1, 7, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(4, 2, 5, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(5, 2, 5, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(6, 3, 3, matrix->Color(0, 0, 255));
  matrix->drawFastVLine(7, 3, 3, matrix->Color(0, 0, 255));

  matrix->drawPixel(8, 4, matrix->Color(0, 0, 255));
  matrix->drawPixel(9, 4, matrix->Color(0, 0, 255));


  matrix->drawPixel(2, 4, matrix->Color(255, 255, 255));
  matrix->drawLine(3, 3, 3, 5, matrix->Color(255, 255, 255));
  matrix->drawLine(4, 3, 4, 5, matrix->Color(255, 255, 255));
  matrix->drawPixel(5, 4, matrix->Color(255, 255, 255));

  matrix->show();
}



//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------

const  uint8_t  rellotge[] PROGMEM = {
  0, 0, 0, 1, 1, 1, 0, 0, 0,
  0, 0, 1, 0, 0, 0, 1, 0, 0,
  0, 1, 0, 0, 1, 0, 0, 1, 0,
  1, 0, 0, 0, 1, 0, 0, 0, 1,
  1, 0, 0, 0, 1, 0, 0, 0, 1,
  1, 0, 0, 0, 1, 1, 1, 0, 1,
  1, 0, 0, 0, 0, 0, 0, 0, 1,
  0, 1, 0, 0, 0, 0, 0, 1, 0,
  0, 0, 1, 0, 0, 0, 1, 0, 0,
  0, 0, 0, 1, 1, 1, 0, 0, 0,
};


void CompteEnrere() {

  uint8_t pixel[1];

  for (int numero = 9 ; numero > 0; numero --) {
    if (cercarFont(48 + numero)) { //hem convertit a char

      //Esborrar buffer screen
      for (byte i = 0; i < MATRIU_WIDTH + screenOffset ; i++) {
        screen[i] = 0;
      }

      //Encuar font i centrar font ampladaFontAEscriure
      for (byte i = 0; i < ampladaFontAEscriure; i++) {
        screen[((MATRIU_WIDTH - ampladaFontAEscriure) / 2) + 1 + i] = fontAEscriure[i];
      }

      escriureScreenLedStrip();
    }
    matrix->show();
    delay(600);

    //Dibuixem un rellotge durant 0.2 segons. La última iteració no ho fem. Utilitzem el color auxiliar
    if (numero > 1) {
      matrix->fillScreen(colors[1]);
      for (uint8_t i = 0; i < 10; i++) {
        for (uint8_t j = 0; j < 9; j++) {
          memcpy_P (pixel, rellotge + (i * 9) + j,  sizeof pixel);
          if ( pixel[0])     matrix->drawPixel(        ((MATRIU_WIDTH - 10) / 2) + 1 + j,           i,             colors[2]  );
        }
      }
      matrix->show();
    }
    delay(300);

    matrix->fillScreen(colors[1]);
    matrix->show();
    delay(100);


    if (EventUSB()) {
      for (byte i = 0; i < MATRIU_WIDTH + screenOffset ; i++) {
        screen[i] = 0;
      }
      break;
    }

  }
  for (byte i = 0; i < MATRIU_WIDTH + screenOffset ; i++) {
    screen[i] = 0;
  }
}


//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------



const  uint8_t  smile[] PROGMEM = {
  0,  0,  0,  1,  1,  1,  0,  0,  0,
  0,  0,  1,  0,  0,  0,  1,  0,  0,
  0,  1,  0,  0,  0,  0,  0,  1,  0,
  1,  0,  0,  1,  0,  1,  0,  0,  1,
  1,  0,  0,  0,  0,  0,  0,  0,  1,
  1,  0,  1,  0,  0,  0,  1,  0,  1,
  1,  0,  0,  1,  1,  1,  0,  0,  1,
  0,  1,  0,  0,  0,  0,  0,  1,  0,
  0,  0,  1,  0,  0,  0,  1,  0,  0,
  0,  0,  0,  1,  1,  1,  0,  0,  0,
};

void Somriu() {

  Serial.println("Rebut smile");

  int8_t pos = 0;
  uint8_t pixel[1];
  boolean dDreta = true;


  while (not EventUSB()) {

    matrix->fillScreen(colors[1]);

    for (uint8_t i = 0; i < 10; i++) {
      for (uint8_t j = 0; j < 9; j++) {
        memcpy_P (pixel, smile + (i * 9) + j,  sizeof pixel);
        if (pixel[0] == 1 )     matrix->drawPixel(        j + pos,           i,             colors[0]  );
      }
    }
    matrix->show();
    delay(100);

    if (dDreta) pos++;
    else pos --;

    if (pos > MATRIU_WIDTH - 9) {
      pos = pos - 2;
      dDreta = false;
    } else  if (pos < 0) {
      pos = 1;
      dDreta = true;
    }
  }
}

//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------


void Gay() {
  Serial.println("Rebut Gay");

  matrix->fillScreen(colors[1]);
  matrix->drawFastHLine(0, 2, MATRIU_WIDTH, matrix->Color(255, 0, 0));
  matrix->drawFastHLine(0, 3, MATRIU_WIDTH, matrix->Color(255, 128, 0));
  matrix->drawFastHLine(0, 4, MATRIU_WIDTH, matrix->Color(255, 255, 0));
  matrix->drawFastHLine(0, 5, MATRIU_WIDTH, matrix->Color(0, 255, 0));
  matrix->drawFastHLine(0, 6, MATRIU_WIDTH, matrix->Color(0, 0, 255));
  matrix->drawFastHLine(0, 7, MATRIU_WIDTH, matrix->Color(255, 0, 255));
  matrix->show();
}


/*-------------------------------------------------------------*/
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------



void writeText() {

  uint8_t i = 3;
  while (inputString[i] != '\0') {
    if (cercarFont(inputString[i])) {
      encuarFontScreen();
      while (posScreen > 0) {
        //Only for debug
        //escriureScreenUSB();
        escriureScreenLedStrip();
        ferCorrerScreen();
        delay(50);
      }

      if (EventUSB()) break;
    }
    i++;
  }

  //move last caracter until the end, althought another instruction arribes
  for (int i = 0; i < MATRIU_WIDTH; i++) {
    escriureScreenLedStrip();
    ferCorrerScreen();
    delay(50);
  }
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
  matrix->fillScreen(colors[1]);

  for (int colunes = 0; colunes < MATRIU_WIDTH; colunes++) {
    for (int files = 0; files < MATRIU_HEIGHT  ; files++) {
      // Compare bits 7-0 in byte
      if (screen[colunes] & (1 << files)) {
        matrix->drawPixel(colunes, MATRIU_HEIGHT - files - 1, colors[0]);
      }
    }
  }

  matrix->show();

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



//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------


//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------
//-------------------------------------------------------------

/*

*/
boolean EventUSB() {


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
