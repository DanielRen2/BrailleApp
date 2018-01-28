// === Addititional Functions === //
struct LEDs {
  byte led;
  int state;
};

// ==== Setup LEDs
LEDs oo = {2 , 0};
LEDs ol = {3 , 0};
LEDs o2 = {4 , 0};
LEDs lo = {5 , 0};
LEDs ll = {6 , 0};
LEDs l2 = {7 , 0};

LEDs leds[] = {oo, ol, o2, l2, ll, lo};

void toggle(int l){
  //Serial.println("State: ");
  //Serial.println(leds[l].state);
  if (leds[l].state == 0){
    digitalWrite(leds[l].led, HIGH);
    leds[l].state = 1;
    //Serial.println(leds[l].state);
  }else{
    //Serial.println("ELSE");
    digitalWrite(leds[l].led, LOW);
    leds[l].state = 0;
  }
}

void setup() {
  // ==== Setup Arduino
  Serial.begin(9600);

  // ==== Setup Pins
  pinMode(2, OUTPUT); //(0,0)
  pinMode(3, OUTPUT); //(0,1)
  pinMode(4, OUTPUT); //(0,2)
  pinMode(5, OUTPUT); //(1,0)
  pinMode(6, OUTPUT); //(1,1)
  pinMode(7, OUTPUT); //(1,2)
}

void loop() {
  // Blink light Test Code
 

  byte i = 0;
  
  while(true){
    //Serial.println("Entering Loop");
    toggle(i);
    delay(100);
    i++;
    if (i >= 6){
      i = 0;
    }
  }
}


