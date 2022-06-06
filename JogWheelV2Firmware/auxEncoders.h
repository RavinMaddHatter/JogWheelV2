#define timeBetweenReads 60
long knobPositions[3];
long prevKnobPositions[3]={0,0,0};
Encoder knobs[3]={Encoder(topKnobA, topKnobB),
                  Encoder(middleKnobA, middleKnobB),
                  Encoder(lowerKnobA, lowerKnobB)};


elapsedMillis auxEncoderTime;
long prevKnobPos[3];
void readAuxEncoders(){
  if(auxEncoderTime>=timeBetweenReads){
    knobPositions[0] = knobs[0].read();
    knobPositions[1] = knobs[1].read();
    knobPositions[2] = knobs[2].read();
    
    for(int i =0;i<3;i++){
      if (abs(knobPositions[i]-prevKnobPositions[i])>3){
        
        //knobs[i].write(0);
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
