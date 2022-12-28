const int busyPin = A5;
const int PTTPin = 9;

String PTTValue = "";
bool busyStatus = false;

void setup() {
  // initialize serial
  Serial.begin(9600);
  // initialize pin
  pinMode(PTTPin, OUTPUT);
  digitalWrite(PTTPin, LOW);
}

void loop() {
  // Read busy status
  int busyValue = analogRead(busyPin);
  //Serial.println(busyValue);
  if (busyValue > 400 && !busyStatus) {
    busyStatus = true;
    Serial.write("t");
    delay(1000);
  } else if (busyValue < 400 && busyStatus) {
    busyStatus = false;
    Serial.write("f");
    delay(1000);
  }

  // Read PTT status
  while (Serial.available() > 0) {
    PTTValue += char(Serial.read());
    delay(20);
  }

  if (PTTValue.length() > 0) {
  
    if(PTTValue == "t\n"){
      digitalWrite(PTTPin, HIGH);
    }
    if(PTTValue == "f\n"){
      digitalWrite(PTTPin, LOW);
    }
    
  }
  PTTValue = "";
}
