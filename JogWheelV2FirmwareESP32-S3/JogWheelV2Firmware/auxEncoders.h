#define timeBetweenReads 10
long knobPositions[4];
long prevKnobPositions[4]={0,0,0,0};


Encoder knobs[4]={Encoder(knob1A, knob1B),
                  Encoder(knob2A, knob2A),
                  Encoder(knob3A, knob3B),
                  Encoder(knob4A, knob4B)};


elapsedMillis auxEncoderTime;
long prevKnobPos[4];
void readAuxEncoders(){
  if(auxEncoderTime>=timeBetweenReads){
    knobPositions[0] = knobs[0].read();
    knobPositions[1] = knobs[1].read();
    knobPositions[2] = knobs[2].read();
    knobPositions[3] = knobs[3].read();
    
    for(int i =0;i<4;i++){
      if (abs(knobPositions[i]-prevKnobPositions[i])>3){
        if(knobPositions[i]>prevKnobPositions[i]){
          Serial.print("knob ");
          Serial.print(i);
          Serial.print(" sending ");
          Serial.println(knobAssignmets[i][1]);
          Keyboard.press(knobAssignmets[i][1]);
          Keyboard.release(knobAssignmets[i][1]);
        }else{
          Keyboard.press(knobAssignmets[i][0]);
          Keyboard.release(knobAssignmets[i][0]);
        
        }
        prevKnobPositions[i]=knobPositions[i];
      }
    }
    

    auxEncoderTime=0;
  }
}
