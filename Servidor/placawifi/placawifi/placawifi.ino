//gràfic amb els pins de la placa
//https://programarfacil.com/podcast/nodemcu-tutorial-paso-a-paso/

//Fer el que diu a Installing with Boards Manager
//https://github.com/esp8266/Arduino

//classe webserver exemples
//https://github.com/esp8266/Arduino/tree/master/libraries/ESP8266WebServer/examples

//No sé si realment cal: m'he posat la llibreria wifiwebserver que té url:
//https://github.com/khoih-prog/WiFiWebServer
//(Té molts exemples)

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>

ESP8266WiFiMulti wifiMulti;     // Create an instance of the ESP8266WiFiMulti class, called 'wifiMulti'

ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

const int led = 2; //aquest és el led de la placa

 //int blin = 0;

void handleRoot();              // function prototypes for HTTP handlers
void handleLED();
//void blonkLED();
void handleNotFound();

void setup(void){
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');

  pinMode(led, OUTPUT);

  wifiMulti.addAP("NASDECACADEVACA", "aquesteselpassword");   // add Wi-Fi networks you want to connect to
  //wifiMulti.addAP("XXXXXB", "GR0XXXXXX1");
  //wifiMulti.addAP("BXXXXse42", "XXXXXXXXXXXiana");
  Serial.println("Connecting ...");
  int i = 0;
  while (wifiMulti.run() != WL_CONNECTED) { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks, and connect to the strongest of the networks above
    delay(250);
    Serial.print('.');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());              // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // Send the IP address of the ESP8266 to the computer

  if (MDNS.begin("provaLED")) {              // Start the mDNS responder for esp8266.local
    Serial.println("mDNS responder started");
  } else {
    Serial.println("Error setting up MDNS responder!");
  }

  server.on("/", HTTP_GET, handleRoot);     // Call the 'handleRoot' function when a client requests URI "/"
  server.on("/LED", HTTP_POST, handleLED);  // Call the 'handleLED' function when a POST request is made to URI "/LED"
  server.onNotFound(handleNotFound);        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"
  server.on("/patata", handlePatata);
  //server.on("/postplain/", handlePlain);
  server.on("/postform/", handleForm);


  server.begin();                           // Actually start the server
  Serial.println("HTTP server started");
}

void loop(void){
  
  MDNS.update();
  server.handleClient();                    // Listen for HTTP requests from clients
}

void handleRoot() {                         // When URI / is requested, send a web page with a button to toggle the LED
  server.send(200, "text/html", "<form action=\"/LED\" method=\"POST\"></BR></BR></HR><input type=\"submit\" value=\"Toggle LED\"></form>");
}

void handleLED() {
  // If a POST request is made to URI /LED
  digitalWrite(led,!digitalRead(led));      // Change the state of the LED
  server.sendHeader("Location","/");  
  Serial.println("Apagar/Encendre");   // Add a header to respond with a new location for the browser to go to the home page again
  server.send(303);                         // Send it back to the browser with an HTTP status 303 (See Other) to redirect
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}





const String postForms = "<html>\
  <head>\
    <title>ESP8266 Web Server POST handling</title>\
    <style>\
      body { background-color: #cccccc; font-family: Arial, Helvetica, Sans-Serif; Color: #000088; }\
    </style>\
  </head>\
  <body>\
    <h1>POST form data to /postform/</h1><br>\
    <form method=\"post\" enctype=\"application/x-www-form-urlencoded\" action=\"/postform/\">\
      <input type=\"text\" name=\"hello\" value=\"world\"><br>\
      <input type=\"submit\" value=\"Submit\">\
    </form>\
  </body>\
</html>";
/*    <h1>POST plain text to /postplain/</h1><br>\
    <form method=\"post\" enctype=\"text/plain\" action=\"/postplain/\">\
      <input type=\"text\" name=\'{\"hello\": \"world\", \"trash\": \"\' value=\'\"}\'><br>\
      <input type=\"submit\" value=\"Submit\">\
    </form>\*/


void handlePatata() {
  digitalWrite(led, 1);
  server.send(200, "text/html", postForms);
  digitalWrite(led, 0);
}

/*void handlePlain() {
  if (server.method() != HTTP_POST) {
    digitalWrite(led, 1);
    server.send(405, "text/plain", "Method Not Allowed");
    digitalWrite(led, 0);
  } else {
    digitalWrite(led, 1);
    server.send(200, "text/plain", "POST body was:\n" + server.arg("plain"));
    digitalWrite(led, 0);
  }
}*/

void handleForm() {
  if (server.method() == HTTP_GET) {
    String message = "GET form was:\n"+  String(server.args()) + "\n";
    for (uint8_t i = 0; i < server.args(); i++) { 
      message += " " + server.argName(i) + ": " + server.arg(i) + "\n"; 
      if (server.argName(i) == "PINUP"){ digitalWrite(server.arg(i).toInt(), 1);
      }else if (server.argName(i) == "PINDWN"){ digitalWrite(server.arg(i).toInt(), 0); }
    }

    message += " <form method=\"GET\" enctype=\"text/plain\" action=\"/postform/\">\
      <input type=\"text\" name=\'PINUP\' value=\'2'><br>\
      <input type=\"submit\" value=\"Submit\">\
    </form>";

    message += " <form method=\"GET\" enctype=\"text/plain\" action=\"/postform/\">\
      <input type=\"text\" name=\'PINDWN\' value=\'2'><br>\
      <input type=\"submit\" value=\"Submit\">\
    </form>";

    server.send(200, "text/html", message);
  }
  else if (server.method() != HTTP_POST) {
    digitalWrite(led, 1);
    server.send(405, "text/plain", "Method Not Allowed");
    digitalWrite(led, 0);
  } else {
    digitalWrite(led, 1);
    String message = "POST form was:\n"+  String(server.args()) + "\n";
    for (uint8_t i = 0; i < server.args(); i++) { message += " " + server.argName(i) + ": " + server.arg(i) + "\n"; }
    server.send(200, "text/plain", message);
    digitalWrite(led, 0);
  }
}
