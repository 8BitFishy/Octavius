#include <IRremote.h>
#include <string.h>
int button = 99;
int IR_RECEIVE_PIN = 11;
IRrecv IrReceiver(IR_RECEIVE_PIN);

int boolaction = 0;


class Device {
  public:
    String id;
    long irremote;
    bool state;
    int onpin;
    int offpin;

    Device() {}

    Device(String a, long b, bool c, int d, int e) {
      id = a;
      irremote = b;
      state = c;
      onpin = d;
      offpin = e;
    }

};


Device devicelist[5];



void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
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


  IrReceiver.enableIRIn();  // Start the receiver
  IrReceiver.blink13(true); // Enable feedback LED



  devicelist[0] = Device("one", 16738455, false, 2, 3);
  devicelist[1] = Device("two", 16750695, false, 4, 5);
  devicelist[2] = Device("three", 16756815, false, 6, 7);
  devicelist[3] = Device("four", 16724175, false, 8, 9);
  devicelist[4] = Device("five", 16718055, false, 10, 11);


  for (int i = 0; i < 6; i++) {
    Serial.print("Device ");
    Serial.print(devicelist[i].id);
    Serial.print(", ir ");
    Serial.println(devicelist[i].irremote);
  }

  /*

    Device device1;
    Device device2;
    Device device3;
    Device device4;
    Device device5;
    Device device6;

    device1.id = 'one';
    device1.irremote = 16738455;
    device1.state = false;
    device1.onpin = 2;
    device1.offpin = 3;

    device2.id = 'two';
    device2.irremote = 16750695;
    device2.state = false;
    device2.onpin = 4;
    device2.offpin = 5;

    device3.id = 'three';
    device3.irremote = 16756815;
    device3.state = false;
    device3.onpin = 6;
    device3.offpin = 7;

    device4.id = 'four';
    device4.irremote = 16724175;
    device4.state = false;
    device4.onpin = 8;
    device4.offpin = 9;

    device5.id = 'five';
    device5.irremote = 16718055;
    device5.state = false;
    device5.onpin = 2;
    device5.offpin = 3;

    device6.id = 'six';
    device6.irremote = 16743045;
  */

}



int buttonselect(long irvalue) {

  for (int i = 0; i < 6; i++) {
    delay(100);
    Serial.println(i);
    Serial.print("Comparing ");
    Serial.print(irvalue);
    Serial.print(" - ");
    Serial.println(devicelist[i].irremote);
    if (irvalue == devicelist[i].irremote) {
      devicelist[i].state = !devicelist[i].state;
      Serial.print("Button ");
      Serial.print(devicelist[i].id);
      Serial.print(" turned ");
      if (devicelist[i].state) {
        Serial.println("on");
        activateremote(devicelist[i].onpin);
        break;
      }
      else {
        Serial.println("off");
        activateremote(devicelist[i].offpin);
        break;
      }
    }
    else {
      Serial.println("Not a match");
    }
    if (i == 5) {
      break;
    }
  }

  return;

}



void activateremote(int plugpin) {
  digitalWrite(plugpin, HIGH);
  delay(500);
  digitalWrite(plugpin, LOW);
  return;
}




void converttarget(int target, int boolaction) {

  int plugpin = (target * 2) + boolaction;
  Serial.println(plugpin);

  activateremote(plugpin);

  return;
}



void loop() {



  if (Serial.available() > 0) {
    String s = Serial.readStringUntil('\n');
    int index = s.indexOf(' ');
    String listid = s.substring(0, index);
    int target = listid.toInt();
    String action = s.substring(index + 1);

    if (action == "on") {
      boolaction = 0;
    }

    else if (action = "off") {
      boolaction = 1;
    }

    converttarget(target, boolaction);

  }


  else if (IrReceiver.decode()) {
    long x = IrReceiver.results.value;
    Serial.print("Irvalue ");
    Serial.print(x);
    Serial.println(" received");

    button = buttonselect(x);

    Serial.print("Button ");
    Serial.print(button);
    Serial.println(" pressed");

    IrReceiver.resume(); // Receive the next value
  }
  delay(100);

}
