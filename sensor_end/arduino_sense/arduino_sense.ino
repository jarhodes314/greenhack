
const int thermo_pos = A0;
float tempc;
float vout;

void setup() {
  pinMode(thermo_pos, INPUT);
  Serial.begin(9600);

}

void loop() {
  vout = analogRead(thermo_pos);
  Serial.print("Thermostat position: ");
  Serial.println(vout);
  delay(1000);
}
