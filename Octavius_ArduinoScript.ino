void setup(){
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  Serial.begin(9600);

}


void loop(){
  if(Serial.available()>0){
    String s = Serial.readStringUntil('\n');

    if(s == "light on"){

      digitalWrite(2, HIGH);
      delay(500);
      digitalWrite(2, LOW);

    }
    if(s == "light off"){

      digitalWrite(4, HIGH);
      delay(500);
      digitalWrite(4, LOW);
    }
  }

}


