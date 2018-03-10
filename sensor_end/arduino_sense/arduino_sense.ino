#include <StaticThreadController.h>
#include <Thread.h>
#include <ThreadController.h>
#include <ArduinoJson.h>
#include <Adafruit_BME280.h>
#include <Servo.h>
#include <pt.h>  


const int thermo_pos = A0;
const int buzzer = 8;
Servo servo;
float tempc;
float vout;
boolean t;

#define BME_SCK 4
#define BME_MISO 7
#define BME_MOSI 5
#define BME_CS 6

#define SEALEVELPRESSURE_HPA (1013.25)

static struct pt pt1, pt2;
int i = 0;
Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI
int pos = 0;

Thread buzzerThread = Thread();
Thread servoThread = Thread();


void setup() {
  pinMode(thermo_pos, INPUT);
  pinMode(buzzer, OUTPUT);

  PT_INIT(&pt1);
  PT_INIT(&pt2);
  
  servo.attach(11);
  
  Serial.begin(9600);
}

void loop() {
  t = false;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();

  JsonObject& sensor1 = root.createNestedObject("1");
  sensor1["sensor"] = "potentiometer";
  sensor1["data"] = analogRead(thermo_pos);

  JsonObject& sensor2 = root.createNestedObject("2");
  sensor2["sensor"] = "temperature";
  sensor2["data"] = bme.readTemperature();

  JsonObject& sensor3 = root.createNestedObject("3");
  sensor3["sensor"] = "humidity";
  sensor3["data"] = bme.readHumidity();

  
  if (Serial.available()){
    Serial.read();

    
    //buzzer_melody();
    //sweep_servo();
   
   // tbuzzer_melody(&pt1);
   // tsweep_servo(&pt2);
    t = true;
    both_things();
  }
  root.printTo(Serial);
  Serial.println();
  if (t) delay(0);
  else delay(1000);
  noTone(buzzer);
}

void buzzer_melody(){
    tone(buzzer,440);
    t = true;
    tone(buzzer,261);    
    // Waits some time to turn off
    delay(200);
    //Turns the buzzer off
    noTone(buzzer); 
    // Sounds the buzzer at the frequency relative to the note D in Hz   
    tone(buzzer,293);             
    delay(200);    
    noTone(buzzer); 
    // Sounds the buzzer at the frequency relative to the note E in Hz
    tone(buzzer,329);      
    delay(200);
    noTone(buzzer);     
    // Sounds the buzzer at the frequency relative to the note F in Hz
    tone(buzzer,349);    
    delay(200);    
    noTone(buzzer); 
    // Sounds the buzzer at the frequency relative to the note G in Hz
    tone(buzzer,392);            
    delay(200);
    noTone(buzzer); 
 }

void sweep_servo(){
        for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}


static int tbuzzer_melody(struct pt *pt){
  static unsigned long timestamp = 0;
    PT_BEGIN(pt);
    while(Serial.available()){
      if (Serial.available()){
      tone(buzzer,440);
      t = true;
      tone(buzzer,261);    
      // Waits some time to turn off
      timestamp = millis();
      PT_WAIT_UNTIL(pt, millis() - timestamp > 200|| Serial.available());
      //Turns the buzzer off
      noTone(buzzer); 
      // Sounds the buzzer at the frequency relative to the note D in Hz   
      tone(buzzer,293);             
      timestamp = millis();
      PT_WAIT_UNTIL(pt, millis() - timestamp > 200 || Serial.available());   
      noTone(buzzer); 
       // Sounds the buzzer at the frequency relative to the note E in Hz
      tone(buzzer,329);      
      timestamp = millis();
      PT_WAIT_UNTIL(pt, millis() - timestamp > 200|| Serial.available());    
      noTone(buzzer);     
      // Sounds the buzzer at the frequency relative to the note F in Hz
      tone(buzzer,349);    
      timestamp = millis();
      PT_WAIT_UNTIL(pt, millis() - timestamp > 200|| Serial.available());    
      noTone(buzzer); 
      // Sounds the buzzer at the frequency relative to the note G in Hz
      tone(buzzer,392);            
      timestamp = millis();
      PT_WAIT_UNTIL(pt, millis() - timestamp > 200|| Serial.available());
      noTone(buzzer);
      
    }
    }
    PT_END(pt); 
 }

static int tsweep_servo(struct pt *pt){
  static unsigned long timestamp = 0;
  PT_BEGIN(pt)
  while(Serial.available()){
    if (Serial.available()){
    for (pos = 0; pos < 180; pos += 30) { 
      servo.write(pos);   
      timestamp = millis();
      //delay(15);                       
      PT_WAIT_UNTIL(pt,millis() - timestamp>40|| Serial.available());
      }
    for (pos = 180; pos > 0; pos -= 30) { 
      servo.write(pos);
      timestamp = millis();
      //delay(15);
      PT_WAIT_UNTIL(pt,millis() - timestamp>40|| Serial.available());
    }
  }
  }
  PT_END(pt);
}

void both_things(){
  int pos = servo.read();
  int i;
  for(int x=0;x<1000;x++){
    
    if (x % 249 == 0){
      if (x/249 % 2 ==0 ){
        servo.write(150);
      } else {
        servo.write(0);
      }
      }
/*    if (x % 15 == 0){
      i = x/15;
      if (i/180 % 2 ==0){
        pos += 30; 
      } else {
        pos -= 30;
      }
      servo.write(pos);
    }
*/
    if (x == 0) tone(buzzer,261);
    if (x == 200) tone(buzzer,293);
    if (x == 400) tone(buzzer,329);
    if (x == 600) tone(buzzer,349);
    if (x == 795) tone(buzzer,392);
    if (x == 1000) noTone(buzzer);


    
    delay(1);
    
  }

}


