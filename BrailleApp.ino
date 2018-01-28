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

LEDs leds[] = {oo, ol, o2, lo, ll, l2};

void toggle(int l){
  if (leds[l].state == 0){
    digitalWrite(leds[l].led, HIGH);
    leds[l].state = 1;
  }else{
    digitalWrite(leds[l].led, LOW);
    leds[l].state = 0;
  }
}

// ==== Main ==== //
void setup() {
  // ==== Setup Arduino
  Serial.begin(9600);
  Serial.write('1');
  Serial.read();
  // ==== Setup Pins
  pinMode(2, OUTPUT); //(0,0)
  pinMode(3, OUTPUT); //(0,1)
  pinMode(4, OUTPUT); //(0,2)
  pinMode(5, OUTPUT); //(1,0)
  pinMode(6, OUTPUT); //(1,1)
  pinMode(7, OUTPUT); //(1,2)

  pinMode(8, INPUT);
}

void loop() {
  while(true){
    byte readByte;

    if (Serial.available() > 0){
        while(Serial.available() < 1){}
        readByte = Serial.read();
        
        if (readByte == '1'){
          toggle(0);
        }else if(readByte == '2'){
          toggle(1);
        }else if(readByte == '3'){
          toggle(2);
        }else if(readByte == '4'){
          toggle(3);
        }else if(readByte == '5'){
          toggle(4);
        }else if(readByte == '6'){
          toggle(5);
        }else if(readByte == '0'){
          while(digitalRead(8) != HIGH){}
          while(digitalRead(8) != LOW){}
          //Gets signal for a new letter
          for(int i=0; i<6; i++){
            if (leds[i].state == 1){
              //digitalWrite(7, HIGH);
              toggle(i);
            }
          }
        }
        Serial.write('2');
    }
  }//End While Loop
}//End void Loop


