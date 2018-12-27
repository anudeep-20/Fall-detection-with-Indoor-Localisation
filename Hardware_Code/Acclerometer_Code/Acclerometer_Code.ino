#include <TinyGPS++.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(3,4);
SoftwareSerial ss(0,1);

TinyGPSPlus gps;

void setup()
{
  mySerial.begin(9600);
  ss.begin(9600);
  pinMode(A1, OUTPUT);
}

void loop()
{
  mySerial.println(map(analogRead(A1), 332, 265, 0, 90));
  mySerial.print(";");
  while (ss.available() > 0){
    gps.encode(ss.read());
    if (gps.location.isUpdated()){
      mySerial.print(gps.location.lat(), 6);
      mySerial.print(";"); 
      mySerial.println(gps.location.lng(), 6);
    }
  }
}
