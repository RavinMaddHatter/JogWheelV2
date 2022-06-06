

// keyPress(i,switchStates[i],lastSwitchStates[i],debouncedSwitchStates[i],lastDebouncedSwitchStates[i]);
void keyPress(int i, bool state,bool prevState, bool dbState, bool preveDbState)
{
  //normal Keys
  if bitRead(SwitchFunctions[i],3){//checks to see if it is a normal switch
    if(dbState){
      if bitRead(SwitchFunctions[i],7){//checks for alt function
        Keyboard.press(MODIFIERKEY_ALT);
      }
      if bitRead(SwitchFunctions[i],6){
        Keyboard.press(MODIFIERKEY_CTRL);
      }
      if bitRead(SwitchFunctions[i],5){
        Keyboard.press(MODIFIERKEY_SHIFT);
      }
      Keyboard.press(SwitchAssignments[i]);
    }
    else{
      if bitRead(SwitchFunctions[i],7){//checks for alt function
        Keyboard.release(MODIFIERKEY_ALT);
      }
      if bitRead(SwitchFunctions[i],6){
        Keyboard.release(MODIFIERKEY_CTRL);
      }
      if bitRead(SwitchFunctions[i],5){
        Keyboard.release(MODIFIERKEY_SHIFT);
      }
      Keyboard.release(SwitchAssignments[i]);
    }
  }
  //rising edge
  if bitRead(SwitchFunctions[i],2){
    if( dbState && state && (dbState!=preveDbState)){
      if bitRead(SwitchFunctions[i],7){//checks for alt function
        Keyboard.press(MODIFIERKEY_ALT);
      }
      if bitRead(SwitchFunctions[i],6){
        Keyboard.press(MODIFIERKEY_CTRL);
      }
      if bitRead(SwitchFunctions[i],5){
        Keyboard.press(MODIFIERKEY_SHIFT);
      }
      Keyboard.press(SwitchAssignments[i]);
      Keyboard.release(SwitchAssignments[i]);
      if bitRead(SwitchFunctions[i],7){
        Keyboard.release(MODIFIERKEY_ALT);
      }
      if bitRead(SwitchFunctions[i],6){
        Keyboard.release(MODIFIERKEY_CTRL);
      }
      if bitRead(SwitchFunctions[i],5){
        Keyboard.release(MODIFIERKEY_SHIFT);
      }
    }
  }
  //falling edge
  if bitRead(SwitchFunctions[i],1){
    if( !dbState && !state && (dbState!=preveDbState)){
      if bitRead(SwitchFunctions[i],7){//checks for alt function
        Keyboard.press(MODIFIERKEY_ALT);
      }
      if bitRead(SwitchFunctions[i],6){
        Keyboard.press(MODIFIERKEY_CTRL);
      }
      if bitRead(SwitchFunctions[i],5){
        Keyboard.press(MODIFIERKEY_SHIFT);
      }
      Keyboard.press(SwitchAssignments[i]);
      Keyboard.release(SwitchAssignments[i]);
      if bitRead(SwitchFunctions[i],7){
        Keyboard.release(MODIFIERKEY_ALT);
      }
      if bitRead(SwitchFunctions[i],6){
        Keyboard.release(MODIFIERKEY_CTRL);
      }
      if bitRead(SwitchFunctions[i],5){
        Keyboard.release(MODIFIERKEY_SHIFT);
      }
    }
  }
}
