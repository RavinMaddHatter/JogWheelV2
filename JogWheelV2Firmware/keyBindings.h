#include <EEPROM.h>

#define frameForwardDefault KEY_RIGHT
#define frameBackDefault KEY_LEFT
#define increasePlaySpeedDefault KEY_L
#define increaseReverseSpeedDefault KEY_J
#define stopPlaybackDefault KEY_K
#define frameForwardAddr 0
#define frameBackAddr 2
#define increasePlaySpeedAddr 4
#define increaseReverseSeepdAddr 6
#define stopPlaybackAddr 8
const byte defaultSwitchFunctions[] = {8,  8,  8, 68,  36,  36,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8};//functions are bit feilds [alt,ctrl, shift, UnAssigned,normal,risingEdge,FallingEdge,UnAssigned]
const int switchFunctionAddr[]   = {83, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82};
const int switchAssignmentAddr[] ={10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44};

const int defaultSwitchAssignments[] = {
  KEY_0, 
  KEY_1, 
  KEY_2, 
  KEY_BACKSLASH, // 3 key on my setup
  KEY_LEFT_BRACE, //1 key on my setup
  KEY_RIGHT_BRACE, //2 key on my setup
  KEY_6, //down key on my setup
  KEY_7, 
  KEY_8, 
  KEY_9,
  KEY_A, //left key on my setup
  KEY_B, 
  KEY_C, 
  KEY_D, //up arrow on my setup
  KEY_E, // right arrow on my setup
  KEY_F, 
  KEY_G, //escape key on my setup
  KEY_H  // I wired the big knob click into the circuit, even though pressing it is physically impossible
  };

const int keyAssignmentAddr[4] = {46,48, 50, 52};
const int defaultkeyAssignments[4]= {KEY_K,KEY_2,KEY_3,KEY_K};

const int knobAssignmetsAddr[3][2] = {{54,56},{58,60},{62,64}};
const int defaultknobAssignmets[3][2]={
                          {KEY_J, KEY_L},//Top
                          {KEY_RIGHT_BRACE, KEY_LEFT_BRACE},//midle
                          {KEY_DOWN, KEY_UP}//bottom
                          };

                          
int frameForward;
int frameBack;
int increasePlaySpeed;
int increaseReverseSpeed;
int stopPlayback;
int SwitchAssignments[18];
int SwitchFunctions[18];
int keyAssignments[4]; 
int knobAssignmets[3][2];
void writeIntIntoEEPROM(int address, int number)
{ 
  byte byte1 = number >> 8;
  byte byte2 = number & 0xFF;
  EEPROM.write(address, byte1);
  EEPROM.write(address + 1, byte2);
}
int readIntFromEEPROM(int address)
{
  byte byte1 = EEPROM.read(address);
  byte byte2 = EEPROM.read(address + 1);
  return (byte1 << 8) + byte2;
}

void setDefaultValues(){
  writeIntIntoEEPROM(frameForwardAddr,frameForwardDefault);
  writeIntIntoEEPROM(frameBackAddr, frameBackDefault);
  writeIntIntoEEPROM(increasePlaySpeedAddr,increasePlaySpeedDefault);
  writeIntIntoEEPROM(increaseReverseSeepdAddr, increaseReverseSpeedDefault);
  writeIntIntoEEPROM(stopPlaybackAddr, stopPlaybackDefault);
  for(int i=0;i<4;i++){
    writeIntIntoEEPROM(keyAssignmentAddr[i],defaultkeyAssignments[i]);
  }
  for(int i=0;i<18;i++){
    writeIntIntoEEPROM(switchAssignmentAddr[i],defaultSwitchAssignments[i]);
    EEPROM.write(switchFunctionAddr[i],defaultSwitchFunctions[i]);
  }
  for(int i = 0; i<3;i++){
    for(int j=0; j<2;j++){
      writeIntIntoEEPROM(knobAssignmetsAddr[i][j],defaultknobAssignmets[i][j]);
    }
  }
}
void printSettings(){
  Serial.print("Forward: "); 
  Serial.println(frameForward);
  Serial.print("Backward: "); 
  Serial.println(frameBack);
  Serial.print("Play: "); 
  Serial.println(increasePlaySpeed); 
  Serial.print("Reverse: "); 
  Serial.println(increaseReverseSpeed);
  Serial.print("Stop: "); 
  Serial.println(stopPlayback);
  for(int i=0;i<18;i++){
    Serial.print("Button-"); 
    Serial.print(i); 
    Serial.print(": "); 
    Serial.print(SwitchAssignments[i]);
    Serial.print(" : "); 
    Serial.println(SwitchFunctions[i],BIN);
  }
  Serial.println("Key Matrix ");
  for(int i = 0; i<3;i++){
      Serial.print("Knob-");
      Serial.print(i);
      Serial.print(": ");
      Serial.print(knobAssignmets[i][0]);
      Serial.print(" : ");
      Serial.println(knobAssignmets[i][1]);
  }
  Serial.println("END OF SETTINGS");
}
void initKeybindings(){
  frameForward=readIntFromEEPROM(frameForwardAddr);
  frameBack=readIntFromEEPROM(frameBackAddr);
  increasePlaySpeed=readIntFromEEPROM(increasePlaySpeedAddr);
  increaseReverseSpeed=readIntFromEEPROM(increaseReverseSeepdAddr);
  stopPlayback=readIntFromEEPROM(stopPlaybackAddr);
  
  for(int i=0;i<4;i++){
    keyAssignments[i]=readIntFromEEPROM(keyAssignmentAddr[i]);
  }
  for(int i=0;i<18;i++){
    SwitchAssignments[i]=readIntFromEEPROM(switchAssignmentAddr[i]);
    SwitchFunctions[i]=EEPROM.read(switchFunctionAddr[i]);
  }
  for(int i = 0; i<3;i++){
    for(int j=0; j<2;j++){
      knobAssignmets[i][j]=readIntFromEEPROM(knobAssignmetsAddr[i][j]);
    }
  }
  printSettings();
}
