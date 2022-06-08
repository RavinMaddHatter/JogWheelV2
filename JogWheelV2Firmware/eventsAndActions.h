

void eventLoop(){
  if(eventQued&&(taskTimer>=eventTime)){
    callTask();
    eventQued = false;
  }
  if (Serial.available() > 0){
    String cmd;
    int pinNo;
    int value;
    byte bvalue;
    commandRecieved=Serial.readStringUntil("\0");
    commandRecieved.trim();

    cmd=commandRecieved.substring(0,commandRecieved.indexOf(" "));
    commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
    switch(cmd[0]){
      case 'b':
        pinNo=commandRecieved.substring(0,commandRecieved.indexOf(" ")).toInt();
        commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
        value=commandRecieved.toInt();
        Serial.print("Setting button ");
        Serial.print(pinNo);
        Serial.print(" to: ");
        Serial.println(value);
        SwitchAssignments[pinNo]=value;
        writeIntIntoEEPROM(switchAssignmentAddr[pinNo],value);
        //printSettings();
        break;
      case 'B':
        pinNo=commandRecieved.substring(0,commandRecieved.indexOf(" ")).toInt();
        commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
        value=commandRecieved.toInt();
        bvalue = value & 0xFF;
        Serial.print("Setting button Function ");
        Serial.print(pinNo);
        Serial.print(" to: ");
        Serial.println(bvalue,BIN);
        SwitchFunctions[pinNo]=bvalue;
        EEPROM.write(switchFunctionAddr[pinNo],bvalue);
        //printSettings();
        break;
      case 'k'://knob not written
        pinNo=commandRecieved.substring(0,commandRecieved.indexOf(" ")).toInt();
        commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
        
        value=commandRecieved.substring(0,commandRecieved.indexOf(" ")).toInt();
        commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
        knobAssignmets[pinNo][0]=value;
        writeIntIntoEEPROM(knobAssignmetsAddr[pinNo][0],value);
        Serial.print("Setting knob ");
        Serial.print(pinNo);
        Serial.print(" CCW to: ");
        Serial.print(value);
        Serial.print(" CW to: ");
        value=commandRecieved.toInt();
        knobAssignmets[pinNo][1]=value;
        Serial.println(value);
        writeIntIntoEEPROM(knobAssignmetsAddr[pinNo][1],value);
        //printSettings();
        break;
      case 'f'://frame forward
        value=commandRecieved.toInt();
        writeIntIntoEEPROM(frameForwardAddr,value);
        frameForward=value;
        break;
      case 'F'://play forward
        value=commandRecieved.toInt();
        frameBack=value;
        writeIntIntoEEPROM(frameBackAddr, value);
        break;
      case 'r'://frame back
        value=commandRecieved.toInt();
        increasePlaySpeed=value;
        writeIntIntoEEPROM(increasePlaySpeedAddr,value);
        break;
      case 'R'://play backwards
        value=commandRecieved.toInt();
        increaseReverseSpeed=value;
        writeIntIntoEEPROM(increaseReverseSeepdAddr, value);
        break;
      case 's'://stop
        value=commandRecieved.toInt();
        stopPlayback=value;
        writeIntIntoEEPROM(stopPlaybackAddr, value);
        break;
      case 'p'://print settings
        printSettings();
        break;
      case 'S'://togle UART Socket mode Sock
        normalMode=!normalMode;
        break;
      case 'd':
        Serial.println("reseting keys to default values");
        setDefaultValues();
        initKeybindings();
        printSettings();
        break;
      default:
        Serial.println("This is the help file, if you dont know what you are doing you must type things exactly, everyting before the colon is the command");
        Serial.println("d: Set the default setting for the hotkeys");
        Serial.println("b XX YY: Sets a button to a new key, XX can be any number between 0 and 17, YY you need to look up the value for the key in https://www.pjrc.com/teensy/usb_keyboard.html you will have to look in the source files");
        Serial.println("B XX YY: Sets the function for a Key, XX can be any number between 0 and 17, YY is a bit feild. A binary number is made where 1 is each mode you want enabled and 0 is for that mode to be disabled [Alt, Ctrl, Shift, UnAssigned, Normal key, Rising Edge button push,Falling Edge Button Push,UnAssigned]");        
        Serial.println("k XX YY ZZ: XX defines the Knob, YY defines the Counter Clock Wise button, ZZ defines the Clock Wise Button");
        Serial.println("f XX: set frame forward key to XX");
        Serial.println("F XX: set Play forward key to XX");
        Serial.println("r XX: set frame back key to XX");
        Serial.println("R XX: set play back key to XX");
        Serial.println("s XX: set stop key to XX");
        Serial.println("p : print the whole ");
      
        
    }
  }
  
  
}
