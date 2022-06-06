#include <Encoder.h>
typedef void (*taskPointer) ();
taskPointer callTask;
elapsedMillis taskTimer;
long eventTime = 0;
bool eventQued = false;
String commandRecieved;

bool normalMode = true;

void setDelayedFunctionCall(long msDelay,taskPointer task ){
  callTask = task;
  eventQued = true;
  eventTime = msDelay;
}
#include "keyBindings.h"
#include "actions.h"

#include "pins.h"
#include "BigEncoder.h"
#include "auxEncoders.h"
#include "simpleButtons.h"
#include "keyMatrixHandler.h"
#include "eventsAndActions.h"



elapsedMillis SocketTiming;
#define socketUpdateRate 50


//bool systemLocked=false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while ( !Serial ) ;  
  setupSimpleButtons();//from "simpleButtons.h"
  initKeyMatrix();//from keyMatrixHandler.h
//  setDefaultValues();
  initKeybindings();
  
}
  
  


void loop() {
  
  // put your main code here, to run repeatedly:
  processBigWheel();//from "BigEncoder.h"
  readAuxEncoders();//from "auxEncoders.h"
  handleButtons();//from "simpleButtons.h"
  handleMatrix();
  eventLoop();
  //
  if (SocketTiming>= socketUpdateRate){
    if(!normalMode){
      Serial.print("BWP ");
      Serial.print(bigWheelPos);
      Serial.print(" ENP ");
      Serial.print(knobPositions[0]);
      Serial.print(" ");
      Serial.print(knobPositions[1]);
      Serial.print(" ");
      Serial.print(knobPositions[2]);
      Serial.print(" SW");
      for(int i=0; i<18;i++){
        Serial.print(" ");
        Serial.print(dBSwState[i]);
      }
      
      Serial.println("");
    }
    SocketTiming=0;
  }
}
