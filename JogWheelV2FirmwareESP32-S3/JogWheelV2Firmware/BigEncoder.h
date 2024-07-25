
long bigWheelPos = 0;
long prevBigWheelPos = 0;
int bigWheelDir=0;
long bigWheelDetentVel=0;
//Big Wheel state machine definitions
int bigWheelState = 0;
#define frameForwardMaxSpeed 75
#define playForwardSpeed 150

Encoder wheel(wheelA, wheelB);
elapsedMillis bigWheelDeltaTime;
#define bigWheelTimeout 50




int bigWheelIdleMode(float wheelSpeed){
  int stateChange=0;
  int nextState=0;
  
  if (abs(wheelSpeed)>0){
    stateChange=1;
    if (abs(wheelSpeed)>frameForwardMaxSpeed){
      stateChange=2;
    }
    if(wheelSpeed<0.01){
      stateChange=stateChange*-1;
    }
  }
  switch (stateChange){
    case 1:
      Serial.println("frame forward");
      Keyboard.press(frameForward);
      Keyboard.release(frameForward);
      break;
    case -1:
      Serial.println("frame backward ");
      Keyboard.press(frameBack);
      Keyboard.release(frameBack);
      break;
    case 2:
      Serial.println("move to play");
      Keyboard.press(increasePlaySpeed);
      Keyboard.release(increasePlaySpeed);
      
      nextState=1;
      break;
    case -2:
      Serial.println("move to reverse play");
      Keyboard.press(increaseReverseSpeed);
      Keyboard.release(increaseReverseSpeed);
      nextState=1;
      break;
  }
  return nextState;
}

int bigWheelPlayMode(float wheelSpeed){
  int nextState=1;
  int stateChange=0;
  if (abs(wheelSpeed)<frameForwardMaxSpeed){
    stateChange=-1;
  }
  if (abs(wheelSpeed)>playForwardSpeed*1.25){//adding histerisis
    stateChange=1;
  }
  switch (stateChange){
    case 1:
      nextState=2;
      if(wheelSpeed>0){
        Keyboard.press(KEY_LEFT_SHIFT);
        Keyboard.press(increasePlaySpeed);
        Keyboard.release(increasePlaySpeed);
        Keyboard.release(KEY_LEFT_SHIFT);
        
        
      }else{
        Keyboard.press(KEY_LEFT_SHIFT);
        Keyboard.press(increaseReverseSpeed);
        Keyboard.release(increaseReverseSpeed);
        Keyboard.release(KEY_LEFT_SHIFT);
      }
      //nextState=2;
      break;
    case -1:
      Keyboard.press(stopPlayback);
      Keyboard.release(stopPlayback);
      nextState=0;
      break;
  }
  return nextState;
}
int doubleSpeedPlay(float wheelSpeed){
  int nextState=2;
  
  if (abs(wheelSpeed)<playForwardSpeed){
    nextState=1;
    if(wheelSpeed>0){
      Keyboard.press(increasePlaySpeed);
      Keyboard.release(increasePlaySpeed);
    }else{
      Keyboard.press(increaseReverseSpeed);
      Keyboard.release(increaseReverseSpeed);
    }
  }
  return nextState;

}

void processBigWheel(){
  bigWheelPos=wheel.read();
  
  if (bigWheelDeltaTime>=bigWheelTimeout){
    if(bigWheelPos>prevBigWheelPos){
      bigWheelDir=1;
    }
    else{
      bigWheelDir=-1;
    }
    float wheelSpeed=1000*float(bigWheelPos-prevBigWheelPos)/bigWheelDeltaTime;
    // big wheel statemaching
    //The big wheel works by pressing j or l to speed up or slow down play back. it is not ideal but it is the best we can do without 
    // the secret sauce black magic has as hardware hooks and to be fair, their hardware is their buisness model. I dont expect them to 
    //Expose that.
    if(normalMode){
    int stateChange=0;
      switch (bigWheelState){
        case 0:
          bigWheelState=bigWheelIdleMode(wheelSpeed);
          break;
        case 1:
          bigWheelState=bigWheelPlayMode(wheelSpeed);
          break;
          
        case 2:
          bigWheelState=doubleSpeedPlay(wheelSpeed);
          break;
            
        
      }
    }

    prevBigWheelPos=bigWheelPos;//sets for next loop
    bigWheelDeltaTime=0;//resets for next loop
  }
}
