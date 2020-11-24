int boolaction = 0;

void setup(){

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  Serial.begin(9600);

}


void activateremote(int plugpin){
  digitalWrite(plugpin, HIGH);
  delay(500);
  digitalWrite(plugpin, LOW);
  return;
}




void converttarget(int target,int boolaction){
 
    int plugpin = (target*2)+boolaction;
    Serial.println(plugpin);
    
    activateremote(plugpin);

    return;
}



void loop(){
  
  if(Serial.available()>0){
    String s = Serial.readStringUntil('\n');
    int index = s.indexOf(' ');    
    String listid = s.substring(0, index);
    int target = listid.toInt();
    String action = s.substring(index+1);
    
    if(action == "on"){
      boolaction = 0;
    }
    
    else if (action = "off"){
      boolaction = 1;
    }
    
    converttarget(target, boolaction);
    
  }

}



