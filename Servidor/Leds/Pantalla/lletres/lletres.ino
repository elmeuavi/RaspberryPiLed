#include <stdlib.h>


//https://github.com/adafruit/Adafruit_NeoMatrix
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <Fonts/TomThumb.h>
#ifndef PSTR
 #define PSTR // Make Arduino Due happy
#endif

#define PIN 4
#define MATRIU_WIDTH 15
#define MATRIU_HEIGHT 10

#define FPSTR(pstr_pointer) (reinterpret_cast<const __FlashStringHelper *>(pstr_pointer))

//ASCII code / Column 1 / Column 2 / ...
const int ABECEDARI3[] PROGMEM  = {
  //'
  39, 0b0000000000, 0b1110000000, 0b1110000000,
  //|
  124, 0b0000000000, 0b1111111111, 0b0000000000
};
const int ABECEDARI4[] PROGMEM  = {
  //
  32, 0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000,
  //!
  33, 0b0000000000, 0b1111111011, 0b1111111011, 0b0000000000,
  //(
  40, 0b0011111000, 0b0111111110, 0b1100000011, 0b0000000000,
  //)
  41, 0b1100000011, 0b0111111110, 0b0001111000, 0b0000000000,
  //,
  44, 0b0000000000, 0b0000001101, 0b0000001110, 0b0000000000,
  //.
  46, 0b0000000000, 0b0000000011, 0b0000000011, 0b0000000000,
  //:
  58, 0b0000000000, 0b0001100011, 0b0001100011, 0b0000000000,
  //;
  59, 0b0000000000, 0b0110001101, 0b0110001110, 0b0000000000,
  //I
  73, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000000000,
  //[
  91, 0b1111111111, 0b1111111111, 0b1000000001, 0b0000000000,
  //]
  93, 0b1000000001, 0b1111111111, 0b1111111111, 0b0000000000,
  //`
  96, 0b1000000000, 0b1100000000, 0b0100000000, 0b0000000000,
  //i
  105, 0b0000000000, 0b1101111111, 0b1101111111, 0b0000000000,
  //j
  106, 0b1011111111, 0b1011111110, 0b0000000000, 0b0000000000,
  //l
  108, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000000000,
  //{
  123, 0b0111111110, 0b1111101111, 0b1000000001, 0b0000000000,
  //}
  125, 0b1000000001, 0b1111101111, 0b0111111110, 0b0000010000
};
const int ABECEDARI5[] PROGMEM = {
  //*
  42, 0b0101000000, 0b0101000000, 0b1110000000, 0b0101000000, 0b0101000000,
  //-
  45, 0b0000000000, 0b0000000100, 0b0000000100, 0b0000000100, 0b0000000000,
  ///
  47, 0b0000000011, 0b0000011100, 0b0011100000, 0b1100000000, 0b0000000000,
  //contra barra 
  92, 0b1100000000, 0b0011100000, 0b0000011100, 0b0000000011, 0b0000000000,
  //f
  102, 0b0001000000, 0b0111111111, 0b1111111111, 0b1001000000, 0b1000000000,
  //t
  116, 0b0001000000, 0b0011111110, 0b0111111111, 0b0001000001, 0b0000000000
};
const int ABECEDARI6[] PROGMEM = {
  //"
  34, 0b0000000000, 0b1110000000, 0b1110000000, 0b0000000000, 0b1110000000, 0b1110000000,
  //$
  36, 0b0011100100, 0b0100110010, 0b1111111111, 0b0100110010, 0b0010011100, 0b0000000000,
  //r
  114, 0b0000000000, 0b0001111111, 0b0001111111, 0b0001000000, 0b0001000000, 0b0000000000
};
const int ABECEDARI7[] PROGMEM = {
  //0
  48, 0b0111111110, 0b1111111111, 0b1000000001, 0b1000000001, 0b1111111111, 0b0111111110, 0b0000000000,
  //1
  49, 0b0000000000, 0b0011000000, 0b0110000000, 0b1111111111, 0b1111111111, 0b0000000000, 0b0000000000,
  //2
  50, 0b0100000011, 0b1100000111, 0b1000011101, 0b1000111001, 0b1111110001, 0b0111000001, 0b0000000000,
  //3
  51, 0b0100000010, 0b1100000011, 0b1000100001, 0b1000100001, 0b1111111111, 0b0111011110, 0b0000000000,
  //4
  52, 0b0000001100, 0b0000110100, 0b0011000100, 0b1111111111, 0b1111111111, 0b0000000100, 0b0000000000,
  //5
  53, 0b0011100010, 0b1111100011, 0b1101000001, 0b1001000001, 0b1001111111, 0b1000111110, 0b0000000000,
  //6
  54, 0b0011111110, 0b0111111111, 0b1000100001, 0b1000100001, 0b1100111111, 0b0100011110, 0b0000000000,
  //7
  55, 0b1000000000, 0b1000000111, 0b1000111111, 0b1011111000, 0b1111000000, 0b1100000000, 0b0000000000,
  //8
  56, 0b0111011110, 0b1111111111, 0b1000100001, 0b1000100001, 0b1111111111, 0b0111011110, 0b0000000000,
  //9
  57, 0b0111100010, 0b1111110011, 0b1000010001, 0b1000010001, 0b1111111110, 0b0111111100, 0b0000000000,
  //J
  74, 0b0000000110, 0b0000000111, 0b0000000001, 0b0000000001, 0b1111111111, 0b1111111110, 0b0000000000,
  //a
  97, 0b0000000000, 0b0000100110, 0b0001001111, 0b0001011001, 0b0001010001, 0b0001111111, 0b0000111111,
  //c
  99, 0b0000000000, 0b0000111110, 0b0001111111, 0b0001000001, 0b0001000001, 0b0001100011, 0b0000100010,
  //e
  101, 0b0000000000, 0b0000111110, 0b0001111111, 0b0001001001, 0b0001001001, 0b0001111011, 0b0000111010,
  //s
  115, 0b0000110010, 0b0001111011, 0b0001011001, 0b0001001101, 0b0001101111, 0b0000100110, 0b0000000000,
  //z
  122, 0b0000000000, 0b0001000011, 0b0001001111, 0b0001011101, 0b0001110001, 0b0001100001, 0b0000000000
};
const int ABECEDARI8[] PROGMEM = {
  //#
  35, 0b0001001111, 0b0001111000, 0b1111001000, 0b0001001111, 0b0001111000, 0b1111001000, 0b0000000000, 0b0000000000,
  //+
  43, 0b0000000000, 0b0000010000, 0b0000010000, 0b0001111100, 0b0001111100, 0b0000010000, 0b0000010000, 0b0000000000,
  //<
  60, 0b0000010000, 0b0000111000, 0b0000101000, 0b0001101100, 0b0001000100, 0b0011000110, 0b0000000000, 0b0000000000,
  //=
  61, 0b0000101000, 0b0000101000, 0b0000101000, 0b0000101000, 0b0000101000, 0b0000101000, 0b0000101000, 0b0000000000,
  //>
  62, 0b0000000000, 0b0011000110, 0b0001000100, 0b0001101100, 0b0000101000, 0b0000111000, 0b0000010000, 0b0000000000,
  //?
  63, 0b0100000000, 0b1100000000, 0b1000001011, 0b1000011011, 0b1000110000, 0b1111100000, 0b0111000000, 0b0000000000,
  //F
  70, 0b0000000000, 0b1111111111, 0b1111111111, 0b1000010000, 0b1000010000, 0b1000010000, 0b1000010000, 0b0000000000,
  //L
  76, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000000,
  //T
  84, 0b1000000000, 0b1000000000, 0b1000000000, 0b1111111111, 0b1111111111, 0b1000000000, 0b1000000000, 0b1000000000,
  //Z
  90, 0b1000000011, 0b1000000111, 0b1000011101, 0b1001111001, 0b1011100001, 0b1110000001, 0b1100000001, 0b0000000000,
  //^
  94, 0b0000010000, 0b0001110000, 0b0111000000, 0b0111000000, 0b0001110000, 0b0000010000, 0b0000000000, 0b0000000000,
  //b
  98, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000100010, 0b0001000001, 0b0001111111, 0b0000111110, 0b0000000000,
  //d
  100, 0b0000000000, 0b0000111110, 0b0001111111, 0b0001000001, 0b0000100010, 0b1111111111, 0b1111111111, 0b0000000000,
  //g
  103, 0b0000000000, 0b0111110010, 0b1111111001, 0b1000001001, 0b0100010001, 0b1111111111, 0b1111111110, 0b0000000000,
  //h
  104, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000100000, 0b0001000000, 0b0001111111, 0b0000111111, 0b0000000000,
  //k
  107, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000011000, 0b0000111110, 0b0001100111, 0b0001000001, 0b0000000000,
  //n
  110, 0b0000000000, 0b0001111111, 0b0001111111, 0b0000100000, 0b0001000000, 0b0001111111, 0b0000111111, 0b0000000000,
  //o
  111, 0b0000000000, 0b0000111110, 0b0001111111, 0b0001000001, 0b0001000001, 0b0001111111, 0b0000111110, 0b0000000000,
  //p
  112, 0b0000000000, 0b1111111111, 0b1111111111, 0b0100010000, 0b1000001000, 0b1111111000, 0b0111110000, 0b0000000000,
  //q
  113, 0b0000000000, 0b0111110000, 0b1111111000, 0b1000001000, 0b0100010000, 0b1111111111, 0b1111111111, 0b0000000000,
  //u
  117, 0b0000000000, 0b0001111110, 0b0001111111, 0b0000000001, 0b0000000001, 0b0001111111, 0b0001111111, 0b0000000000,
  //v
  118, 0b0001100000, 0b0001111100, 0b0000011111, 0b0000000011, 0b0000011111, 0b0001111100, 0b0001100000, 0b0000000000,
  //x
  120, 0b0000000000, 0b0001100011, 0b0001110111, 0b0000011100, 0b0000011100, 0b0001110111, 0b0001100011, 0b0000000000,
  //y
  121, 0b1100000001, 0b1111100001, 0b0011111111, 0b0000011111, 0b0011111100, 0b1111100000, 0b1100000000, 0b0000000000,
  //~
  126, 0b0000001000, 0b0000010000, 0b0000010000, 0b0000011000, 0b0000001000, 0b0000001000, 0b0000010000, 0b0000000000
};
const int ABECEDARI9[] PROGMEM = {
  //B
  66, 0b0000000000, 0b1111111111, 0b1111111111, 0b1000100001, 0b1000100001, 0b1000100001, 0b1111111111, 0b0111011110, 0b0000000000,
  //C
  67, 0b0000000000, 0b0011111100, 0b0111111110, 0b1100000011, 0b1000000001, 0b1000000001, 0b1000000001, 0b1100000011, 0b0100000010,
  //D
  68, 0b0000000000, 0b1111111111, 0b1111111111, 0b1000000001, 0b1000000001, 0b1100000011, 0b0111111110, 0b0011111100, 0b0000000000,
  //E
  69, 0b0000000000, 0b1111111111, 0b1111111111, 0b1000100001, 0b1000100001, 0b1000100001, 0b1000100001, 0b0000000000, 0b0000000000,
  //H
  72, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000100000, 0b0000100000, 0b0000100000, 0b1111111111, 0b1111111111, 0b0000000000,
  //N
  78, 0b0000000000, 0b1111111111, 0b1111111111, 0b0111000000, 0b0001110000, 0b0000011100, 0b1111111111, 0b1111111111, 0b0000000000,
  //P
  80, 0b0000000000, 0b1111111111, 0b1111111111, 0b1000010000, 0b1000010000, 0b1000010000, 0b1111110000, 0b0111100000, 0b0000000000,
  //Q
  81, 0b0001111000, 0b0011111100, 0b0110000110, 0b0100001010, 0b0110000110, 0b0011111110, 0b0001111001, 0b0000000000, 0b0000000000,
  //S
  83, 0b0000000000, 0b0111000010, 0b1111100011, 0b1001110001, 0b1000110001, 0b1000111001, 0b1100011111, 0b0100001110, 0b0000000000,
  //U
  85, 0b0000000000, 0b1111111110, 0b1111111111, 0b0000000001, 0b0000000001, 0b0000000001, 0b1111111111, 0b1111111110, 0b0000000000,
  //V
  86, 0b1100000000, 0b1111100000, 0b0011111100, 0b0000011111, 0b0000000011, 0b0000011111, 0b0011111100, 0b1111100000, 0b1100000000,
  //X
  88, 0b0000000000, 0b1100000011, 0b1110000111, 0b0011111100, 0b0001111000, 0b0011111100, 0b1110000111, 0b1100000011, 0b0000000000,
  //_
  95, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000001, 0b0000000000, 0b0000000000
};
const int ABECEDARI10[] PROGMEM = {
  //&
  38, 0b0000000000, 0b0000001110, 0b0110011111, 0b1111110001, 0b1001111001, 0b1111011111, 0b0111000110, 0b0000011111, 0b0000000001, 0b0000000000,
  //A
  65, 0b0000000011, 0b0000011111, 0b0011111100, 0b1111100100, 0b1100000100, 0b1111100100, 0b0011111100, 0b0000011111, 0b0000000011, 0b0000000000,
  //G
  71, 0b0000000000, 0b0011111100, 0b0111111110, 0b1100000011, 0b1000000001, 0b1000010001, 0b1000010001, 0b1100011111, 0b0100011110, 0b0000000000,
  //K
  75, 0b0000000000, 0b1111111111, 0b1111111111, 0b0000110000, 0b0011100000, 0b0111111100, 0b1100011111, 0b1000000011, 0b0000000000, 0b0000000000,
  //O
  79, 0b0000000000, 0b0011111100, 0b0111111110, 0b1100000011, 0b1000000001, 0b1000000001, 0b1100000011, 0b0111111110, 0b0011111100, 0b0000000000,
  //R
  82, 0b0000000000, 0b1111111111, 0b1111111111, 0b1000010000, 0b1000010000, 0b1000011000, 0b1111111110, 0b0111100111, 0b0000000001, 0b0000000000,
  //Y
  89, 0b1100000000, 0b1110000000, 0b0011100000, 0b0001111111, 0b0001111111, 0b0011100000, 0b1110000000, 0b1100000000, 0b0000000000, 0b0000000000
};
const int ABECEDARI11[] PROGMEM = {
  //@
  64, 0b0001111000, 0b0110000110, 0b0100111010, 0b1011000101, 0b1010000101, 0b1010001101, 0b1011111101, 0b1011000101, 0b0100001010, 0b0011110010, 0b0000000000,
  //M
  77, 0b0000000000, 0b1111111111, 0b1111111111, 0b1111100000, 0b0011111110, 0b0000000111, 0b0011111110, 0b1111100000, 0b1111111111, 0b1111111111, 0b0000000000,
  //W
  87, 0b1100000000, 0b1111111000, 0b0011111111, 0b0000000111, 0b0001111111, 0b1111111000, 0b0001111111, 0b0000000111, 0b0011111111, 0b1111111000, 0b1100000000,
  //w
  119, 0b0001100000, 0b0001111100, 0b0000011111, 0b0000000111, 0b0000111110, 0b0001110000, 0b0000111110, 0b0000000111, 0b0000011111, 0b0001111100, 0b0001100000
};
const int ABECEDARI12[] PROGMEM = {
  //%
  37, 0b0000000000, 0b1111100000, 0b1000100000, 0b1111100011, 0b0000011100, 0b0001100000, 0b1110011111, 0b0000010001, 0b0000011111, 0b0000000000, 0b0000000000, 0b0000000000,
  //m
  109, 0b0000000000, 0b0001111111, 0b0001111111, 0b0000100000, 0b0001000000, 0b0001111111, 0b0001111111, 0b0000100000, 0b0001000000, 0b0001111111, 0b0000111111, 0b0000000000
};
//Manualy, i reduced width of this letter
//int ABECEDARI13[] = {
  //W
  //87, 0b1100000000, 0b1111111000, 0b0011111111, 0b0000000111, 0b0001111111, 0b1111111000, 0b1110000000, 0b1111111000, 0b0001111111, 0b0000000111, 0b0011111111, 0b1111111000, 0b1100000000
//};


long TotesLesFonts[]  = {(int*)&ABECEDARI3,(int*)&ABECEDARI4,(int*)&ABECEDARI5,(int*)&ABECEDARI6,(int*)&ABECEDARI7,(int*)&ABECEDARI8,(int*)&ABECEDARI9,(int*)&ABECEDARI10,(int*)&ABECEDARI11,(int*)&ABECEDARI12}; //,(int*)&ABECEDARI13};
//long TotesLesFonts[10];
//const char* TotesLesFonts[]  = {ABECEDARI3,ABECEDARI4,ABECEDARI5,ABECEDARI6,ABECEDARI7,ABECEDARI8,ABECEDARI9,ABECEDARI10,ABECEDARI11,ABECEDARI12}; //,(int*)&ABECEDARI13};
//with of any type of font
unsigned int TotesLesFontsAmplada[] ={3,4,5,6,7,8,9,10,11,12};
/*int TotesLesFontsAmplada[] ={sizeof(ABECEDARI3[0]) / sizeof(ABECEDARI3[0][0])-1,     //3
                              sizeof(ABECEDARI4[0]) / sizeof(ABECEDARI4[0][0])-1,    //4
                              sizeof(ABECEDARI5[0]) / sizeof(ABECEDARI5[0][0])-1,    //5
                              sizeof(ABECEDARI6[0]) / sizeof(ABECEDARI6[0][0])-1,    //6
                              sizeof(ABECEDARI7[0]) / sizeof(ABECEDARI7[0][0])-1,    //7
                              sizeof(ABECEDARI8[0]) / sizeof(ABECEDARI8[0][0])-1,    //8
                              sizeof(ABECEDARI9[0]) / sizeof(ABECEDARI9[0][0])-1,    //9
                              sizeof(ABECEDARI10[0]) / sizeof(ABECEDARI10[0][0])-1,  //10
                              sizeof(ABECEDARI11[0]) / sizeof(ABECEDARI11[0][0])-1,  //11
                              sizeof(ABECEDARI12[0]) / sizeof(ABECEDARI12[0][0])-1};  //12
//                              sizeof(ABECEDARI13[0]) / sizeof(ABECEDARI13[0][0])-1}; //13*/
//How many fons we have of with3, with4, width5,..)

int TotesLesFontsQuantes[] ={sizeof(ABECEDARI3) / sizeof(ABECEDARI3[0]) /  (TotesLesFontsAmplada[0]+1),
                              sizeof(ABECEDARI4) / sizeof(ABECEDARI4[0])/  (TotesLesFontsAmplada[1]+1),
                              sizeof(ABECEDARI5) / sizeof(ABECEDARI5[0])/  (TotesLesFontsAmplada[2]+1),
                              sizeof(ABECEDARI6) / sizeof(ABECEDARI6[0])/  (TotesLesFontsAmplada[3]+1),
                              sizeof(ABECEDARI7) / sizeof(ABECEDARI7[0])/  (TotesLesFontsAmplada[4]+1),
                              sizeof(ABECEDARI8) / sizeof(ABECEDARI8[0])/  (TotesLesFontsAmplada[5]+1),
                              sizeof(ABECEDARI9) / sizeof(ABECEDARI9[0])/  (TotesLesFontsAmplada[6]+1),
                              sizeof(ABECEDARI10) / sizeof(ABECEDARI10[0])/  (TotesLesFontsAmplada[7]+1),
                              sizeof(ABECEDARI11) / sizeof(ABECEDARI11[0])/  (TotesLesFontsAmplada[8]+1),
                              sizeof(ABECEDARI12) / sizeof(ABECEDARI12[0])/  (TotesLesFontsAmplada[9]+1)};
//                              sizeof(ABECEDARI13) / sizeof(ABECEDARI13[0])};

byte QuantesTaulesFonts = sizeof(TotesLesFontsAmplada)/sizeof(TotesLesFontsAmplada[0]);


//When i found a char to write, i will store there
int  fontAEscriure[13];
byte ampladaFontAEscriure;

//30 primeres posicions son la pantalla real, les altres 11 son per offset
const byte screenWidth = 15;
//One less than the bigest letter width
const byte screenOffset = 11; 
byte posScreen = 0;
int screen[screenWidth+screenOffset];



Adafruit_NeoMatrix matrix= Adafruit_NeoMatrix(MATRIU_WIDTH, MATRIU_HEIGHT, PIN,
  NEO_MATRIX_BOTTOM     + NEO_MATRIX_RIGHT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);
const uint16_t colors[] = {  matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255) };



void init_neomatrix(){
 
 // matrix.setFont(&TomThumb);
  matrix.begin();  
  matrix.setTextWrap(false);
  matrix.setBrightness(10);


  matrix.setTextColor(colors[0]);
}


//int x = matrix.width();
int x = MATRIU_WIDTH;
int pass = 0;

/*
 * 
 */
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

/*
 * 
 */
void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  delay(3000);

  
Serial.println(" "); 
/*
  TotesLesFonts[0] = (long) pgm_get_far_address(ABECEDARI3);
  TotesLesFonts[1] = (long) pgm_get_far_address(ABECEDARI4);
  TotesLesFonts[2] = (long) pgm_get_far_address(ABECEDARI5);
  TotesLesFonts[3] = (long) pgm_get_far_address(ABECEDARI6);
  TotesLesFonts[4] = (long) pgm_get_far_address(ABECEDARI7);
  TotesLesFonts[5] = (long) pgm_get_far_address(ABECEDARI8);
  TotesLesFonts[6] = (long) pgm_get_far_address(ABECEDARI9);
  TotesLesFonts[7] = (long) pgm_get_far_address(ABECEDARI10);
  TotesLesFonts[8] = (long) pgm_get_far_address(ABECEDARI11);
  TotesLesFonts[9] = (long) pgm_get_far_address(ABECEDARI12);
*/

for (int i=0;i<10;i++){
    int readValue = pgm_read_word(TotesLesFonts[i]);
  Serial.print(" "); 
  Serial.print("pgm_read_word");
  Serial.print(readValue);
  Serial.println(" "); 
}

  
 init_neomatrix();

  
}






void loop() {
/*
  byte matrixOrdenada[] =   {9,10,29,30,49,50,69,70,89,90,109,110,129,130,149,
            8,11,28,31,48,51,68,71,88,91,108,111,128,131,148,
            7,12,27,32,47,52,67,72,87,92,107,112,127,132,147,
            6,13,26,33,46,53,66,73,86,93,106,113,126,133,146,
            5,14,25,34,45,54,65,74,85,94,105,114,125,134,145,
            4,15,24,35,44,55,64,75,84,95,104,115,124,135,144,
            3,16,23,36,43,56,63,76,83,96,103,116,123,136,143,
            2,17,22,37,42,57,62,77,82,97,102,117,122,137,142,
            1,18,21,38,41,58,61,78,81,98,101,118,121,138,141,
            0,19,20,39,40,59,60,79,80,99,100,119,120,139,140};
 delay(3000);
  byte quinPixel=0;
        for (int colunes = 0; colunes < MATRIU_WIDTH; colunes++) {
          for (int files = 0; files < MATRIU_HEIGHT; files++) {
            // Compare bits 7-0 in byte
            matrix.setPixelColor(matrixOrdenada[quinPixel], 255, 255, 255); 
          
          quinPixel++;
           matrix.show();
          Serial.print (quinPixel);
          Serial.print ("");
          Serial.println (matrixOrdenada[quinPixel]);
          delay(100);
          }
       }

 delay(10000);

*/
  
  
  //iteracio_neomatrix();


  for (int i =32; i<127;i++)
    if (cercarFont((char)i)){
/*      Serial.print(i);
      Serial.println((char)i);
      escriureLletraSeleccionada();
      //delay(100);
  */    
      encuarFontScreen();
      while (posScreen> 0){
        //  Serial.println("INICI PANTALLA");
          escriureScreenUSB();
          escriureScreenLedStrip();
          ferCorrerScreen();
        //  Serial.println("FINAL PANTALLA");
          delay(50);
      }
    
    } else {
      Serial.print("Font No trobada:");
      Serial.print(i);
      Serial.print(" ");
      Serial.println(char(i));
//      delay(1000);
    }
    

delay(2000);

}




/*
 * Iterar a trabés de les taules de amplades de fonts per trobar la que busquem
 */
boolean cercarFont(char pCaracter){
  int iCaracter = pCaracter;
  
/*  
   Serial.print("QuantesTaulesFonts");
  Serial.print(" "); 
   Serial.print(QuantesTaulesFonts);
   delay(1000);
  */
  //reinicialitzem les variables de font trobada de la llista
  ampladaFontAEscriure = 0;
  for( int i =0;i<13;i++) {fontAEscriure[i]=0;}


  for (byte i=0;i<QuantesTaulesFonts;i++){
    cercarFontLletres(i,TotesLesFontsQuantes[i],TotesLesFontsAmplada[i],iCaracter);
    if (ampladaFontAEscriure != 0) break;
  }
/*cercarFontLletres(ABECEDARI3,TotesLesFontsQuantes[0],TotesLesFontsAmplada[0],iCaracter);
  cercarFontLletres(ABECEDARI4,TotesLesFontsQuantes[1],TotesLesFontsAmplada[1],iCaracter);
  cercarFontLletres(ABECEDARI5,TotesLesFontsQuantes[2],TotesLesFontsAmplada[2],iCaracter);
  cercarFontLletres(ABECEDARI6,TotesLesFontsQuantes[3],TotesLesFontsAmplada[3],iCaracter);
  cercarFontLletres(ABECEDARI7,TotesLesFontsQuantes[4],TotesLesFontsAmplada[4],iCaracter);
  
  cercarFontLletres(ABECEDARI8,TotesLesFontsQuantes[5],TotesLesFontsAmplada[5],iCaracter);
  cercarFontLletres(ABECEDARI9,TotesLesFontsQuantes[6],TotesLesFontsAmplada[6],iCaracter);
  cercarFontLletres(ABECEDARI10,TotesLesFontsQuantes[7],TotesLesFontsAmplada[7],iCaracter);
  cercarFontLletres(ABECEDARI11,TotesLesFontsQuantes[8],TotesLesFontsAmplada[8],iCaracter);
  cercarFontLletres(ABECEDARI12,TotesLesFontsQuantes[9],TotesLesFontsAmplada[9],iCaracter);*/
  

  return ampladaFontAEscriure > 0;
}

/*
 * Iterar sobre una taula d'una amplada concret de font 
 */
void cercarFontLletres(int quinaArray, byte pQuantesLLetres, byte pMidaLletres, int pCaracter){
 int debug = 0;
if (debug == 1){
//if (pCaracter == 48){
     Serial.print("pQuantesLLetres");
  Serial.print(" "); 
   Serial.print(pQuantesLLetres);
  Serial.print(" "); 
     Serial.print("pMidaLletres");
  Serial.print(" "); 
   Serial.print(pMidaLletres);
  Serial.print(" "); 
     Serial.print("quinaArray");
  Serial.print(" "); 
   Serial.print(quinaArray);
/*  Serial.print(" "); 
  Serial.print("TotesLesFonts[quinaArray][0]");
  Serial.print(" "); 
  Serial.print(TotesLesFonts[quinaArray][0]);
  Serial.print(" "); 
  Serial.print("FPSTR(TotesLesFonts[quinaArray]).charAt(0)");
  Serial.print(" "); 
  Serial.print(FPSTR(TotesLesFonts[quinaArray]));
  Serial.print(" "); */
  /*
  int mida = pQuantesLLetres * (pMidaLletres+1) * 2 ;
  Serial.print("mida");
  Serial.print(" "); 
  Serial.print(mida);
  Serial.print(" "); 
  
  int  r[mida];
    memcpy_P((void*)&r, TotesLesFonts[quinaArray], sizeof(r)); 
    
  //Serial.print(FPSTR(TotesLesFonts[quinaArray])->charAt(0));
  //pstr_pointer xyz = FPSTR(TotesLesFonts[quinaArray]);
  Serial.print(r[0]); 
  //pgm_read_byte(xyz + i);

  int readValue;
  readValue = pgm_read_word(&TotesLesFonts[quinaArray][0]);
  Serial.print(" "); 
  Serial.print("pgm_read_word");
  Serial.print(readValue);
  Serial.print(" "); 

  readValue = pgm_read_word(&ABECEDARI8[0]);
  Serial.print(" "); 
  Serial.print("pgm_read_word");
  Serial.print(readValue);
  Serial.print(" "); 
*/
   
  /*Serial.print(" "); 
        Serial.print("pMidaLletres");
  Serial.print(" "); 
   Serial.print(pMidaLletres);
   Serial.print(" "); */
     Serial.print("pCaracter");
  Serial.print(" "); 
   Serial.print(char(pCaracter));/*
    Serial.print("       "); 
     Serial.print("sizeof(ABECEDARI4)"); 
      Serial.print(sizeof(ABECEDARI4)); 
  Serial.print(" "); 
           Serial.print("sizeof(ABECEDARI4[0])"); 
      Serial.print(sizeof(ABECEDARI4[0])); */
/*      Serial.print(" ");
      Serial.print("TotesLesFonts[quinaArray][0]"); 
      Serial.print(TotesLesFonts[quinaArray][0]); 
      Serial.print((char)TotesLesFonts[quinaArray][0]); 
      Serial.print(" ");
      Serial.print("TotesLesFonts[5][0]");
      Serial.print(TotesLesFonts[5][0]);

/*
            Serial.print("TotesLesFontsQuantes"); 
      Serial.println(TotesLesFontsQuantes); */


  Serial.println("");
   delay(100);
}
   
    for (byte lletra = 0; lletra < pQuantesLLetres; lletra++) {
        //if (pCaracter == 48){ //Serial.println(TotesLesFonts[quinaArray][lletra * (pMidaLletres+1)]);   
        //Serial.println(pgm_read_word(TotesLesFonts[quinaArray] +     (2 * lletra * (pMidaLletres+1))     ));   
        //                      }

        //if (pCaracter ==  TotesLesFonts[quinaArray][lletra * (pMidaLletres+1)]){
        int posIni = (2 /*bytes*/ * lletra * (pMidaLletres+1));  //apuntem al codi de caràcter
        if (pCaracter ==  pgm_read_word(   TotesLesFonts[quinaArray] + posIni   )    ){
          Serial.println("trobada!!!");
          posIni = posIni + 2; //Apuntem a la lletra
          ampladaFontAEscriure = pMidaLletres;
          //for( int i =0;i<ampladaFontAEscriure;i++) {fontAEscriure[i]=TotesLesFonts[quinaArray][posIni+i];}
          for( int i =0;i<ampladaFontAEscriure;i++) {fontAEscriure[i]=pgm_read_word(   TotesLesFonts[quinaArray] + posIni + (i*2)  );}
          break;
        }
        
    }
    

}

/*
 *
 */
void encuarFontScreen(){
 
  for (byte i =0;i<ampladaFontAEscriure;i++){
    screen[screenWidth+i-1] = fontAEscriure[i];
  }
  posScreen = ampladaFontAEscriure;
}

/*
 * 
 */
void escriureScreenUSB(){
        for (int colunes = 0; colunes < screenWidth+screenOffset; colunes++) {
          for (int bits = 9; bits > -1; bits--) {
            // Compare bits 7-0 in byte
            if (screen[colunes] & (1 << bits)) { Serial.print("1");  }
            else {                               Serial.print(" ");  }
          }
          Serial.print("\n");
       }
}
/*
 * 
 */
void escriureScreenLedStrip(){
/*
  byte matrixOrdenada[] =   {9,10,29,30,49,50,69,70,89,90,109,110,129,130,149,
            8,11,28,31,48,51,68,71,88,91,108,111,128,131,148,
            7,12,27,32,47,52,67,72,87,92,107,112,127,132,147,
            6,13,26,33,46,53,66,73,86,93,106,113,126,133,146,
            5,14,25,34,45,54,65,74,85,94,105,114,125,134,145,
            4,15,24,35,44,55,64,75,84,95,104,115,124,135,144,
            3,16,23,36,43,56,63,76,83,96,103,116,123,136,143,
            2,17,22,37,42,57,62,77,82,97,102,117,122,137,142,
            1,18,21,38,41,58,61,78,81,98,101,118,121,138,141,
            0,19,20,39,40,59,60,79,80,99,100,119,120,139,140};
*/
byte matrixOrdenada[] =   {149 , 148 , 147 , 146 , 145 , 144 , 143 , 142 , 141 , 140 ,
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
  

  byte quinPixel=0;
        for (int colunes = 0; colunes < MATRIU_WIDTH; colunes++) {
          for (int files = MATRIU_HEIGHT-1; files >= 0 ; files--) {
            // Compare bits 7-0 in byte
            if (screen[colunes] & (1 << files)) { matrix.setPixelColor(matrixOrdenada[quinPixel], 255, 255, 255); }
            else {                               matrix.setPixelColor(matrixOrdenada[quinPixel], 0, 0, 0); }

            //Serial.print(quinPixel);
            //Serial.print(" ");
            //Serial.println(matrixOrdenada[quinPixel]);
            quinPixel++;
          }
          //Serial.print("\n");
       }

  matrix.show();
  delay(100);

}

/*
 * 
 */
void ferCorrerScreen(){
  for (int columna = 0; columna < screenWidth+screenOffset-1; columna++) {
    screen[columna]=screen[columna+1];
  }
  screen[screenWidth+screenOffset-1]=0;
  posScreen = posScreen -1;
}



/*
 * 
 */
void escriureLletraSeleccionada(){
      for (int colunes = 0; colunes < ampladaFontAEscriure; colunes++) {
        //Serial.println(fontAEscriure[colunes]);
          for (int bits = 9; bits > -1; bits--) {
            // Compare bits 7-0 in byte
            if (fontAEscriure[colunes] & (1 << bits)) { Serial.print("1");  }
            else {                                      Serial.print(" ");  }
          }
          Serial.print("\n");
       }
}
