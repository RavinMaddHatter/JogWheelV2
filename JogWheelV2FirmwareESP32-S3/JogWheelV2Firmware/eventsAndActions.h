

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
    commandRecieved = Serial.readStringUntil('\0');
    commandRecieved.trim();

    cmd=commandRecieved.substring(0,commandRecieved.indexOf(" "));
    commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
    switch(cmd[0]){
      case 'b':
        pinNo=commandRecieved.substring(0,commandRecieved.indexOf(" ")).toInt();
        commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
        value=commandRecieved.toInt();
        USBSerial.print("Setting button ");
        USBSerial.print(pinNo);
        USBSerial.print(" to: ");
        USBSerial.println(value);
        SwitchAssignments[pinNo]=value;
        writeIntIntoEEPROM(switchAssignmentAddr[pinNo],value);
        break;
      case 'B':
        pinNo=commandRecieved.substring(0,commandRecieved.indexOf(" ")).toInt();
        commandRecieved.remove(0,commandRecieved.indexOf(" ")+1);
        value=commandRecieved.toInt();
        bvalue = value & 0xFF;
        USBSerial.print("Setting button Function ");
        USBSerial.print(pinNo);
        USBSerial.print(" to: ");
        USBSerial.println(bvalue,BIN);
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
        USBSerial.print("Setting knob ");
        USBSerial.print(pinNo);
        USBSerial.print(" CCW to: ");
        USBSerial.print(value);
        USBSerial.print(" CW to: ");
        value=commandRecieved.toInt();
        knobAssignmets[pinNo][1]=value;
        USBSerial.println(value);
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
        increasePlaySpeed=value;
        writeIntIntoEEPROM(increasePlaySpeedAddr, value);
        break;
      case 'r'://frame back
        value=commandRecieved.toInt();
        frameBack=value;
        writeIntIntoEEPROM(frameBackAddr,value);
        USBSerial.print("setting revers\n\r");
        USBSerial.println(frameBackAddr);
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
        USBSerial.println("reseting keys to default values");
        setDefaultValues();
        initKeybindings();
        printSettings();
        break;
      default:
        USBSerial.println("This is the help file, if you dont know what you are doing you must type things exactly, everyting before the colon is the command");
        USBSerial.println("d: Set the default setting for the hotkeys");
        USBSerial.println("b XX YY: Sets a button to a new key, XX can be any number between 0 and 17, YY you need to look up the value for the key in https://www.pjrc.com/teensy/usb_keyboard.html you will have to look in the source files");
        USBSerial.println("B XX YY: Sets the function for a Key, XX can be any number between 0 and 17, YY is a bit feild. A binary number is made where 1 is each mode you want enabled and 0 is for that mode to be disabled [Alt, Ctrl, Shift, UnAssigned, Normal key, Rising Edge button push,Falling Edge Button Push,UnAssigned]");        
        USBSerial.println("k XX YY ZZ: XX defines the Knob, YY defines the Counter Clock Wise button, ZZ defines the Clock Wise Button");
        USBSerial.println("f XX: set frame forward key to XX");
        USBSerial.println("F XX: set Play forward key to XX");
        USBSerial.println("r XX: set frame back key to XX");
        USBSerial.println("R XX: set play back key to XX");
        USBSerial.println("s XX: set stop key to XX");
        USBSerial.println("p : print the whole");        
    }
  }
  
  
}
