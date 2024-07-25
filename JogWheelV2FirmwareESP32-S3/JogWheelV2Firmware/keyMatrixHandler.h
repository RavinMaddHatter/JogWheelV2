
bool prevSwState[18];//Where we will store the reads from last loop
bool dBSwState[18];//= {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};//where we wil store the debounced state
bool prevDBSwState[18];//where we will store the previous debounced state 
elapsedMillis timeSinceLastChange[18];//Stores time of last transition, if the state is stil the same we will declare the button pressed
elapsedMillis keymatriclastcheck;
#define stablizationTime 50//how long the state must be stable before button is pressed
#define checkInterval 10
void initKeyMatrix(){
  for (int i = 0; i < 3; i++) {
    pinMode(mat1RowPins[i], OUTPUT);
    pinMode(mat2RowPins[i], OUTPUT);
    digitalWrite(mat1RowPins[i], HIGH);
    digitalWrite(mat2RowPins[i], HIGH);
    pinMode(mat1ColPins[i], INPUT_PULLUP);
    pinMode(mat2ColPins[i], INPUT_PULLUP);
    
  }

  for (int row = 0; row < 3; row++){
    for (int col = 0; col < 3; col++){
      USBSerial.print("mat: 0 ");
      USBSerial.print("row: ");
      USBSerial.print(row);
      USBSerial.print("col: ");
      USBSerial.write(col);
      USBSerial.print("index: ");
      USBSerial.println(keyMatrix[0][row][col]);
    }
  }
  for (int row = 0; row < 3; row++){
    for (int col = 0; col < 3; col++){
      USBSerial.print("mat: 1");
      USBSerial.print(" row: ");
      USBSerial.print(row);
      USBSerial.print(" col: ");
      USBSerial.print(col);
      USBSerial.print(" index: ");
      USBSerial.println(keyMatrix[1][row][col]);
    }
  }
}



bool switchpins[18];

void handleMatrix(){
  if(keymatriclastcheck>checkInterval) {
    bool switchStates[18];
    for (int row = 0; row < 3; row++) {
      digitalWrite(mat1RowPins[row], LOW);//set the pin we want to read low
      digitalWrite(mat2RowPins[row], LOW);//set the pin we want to read low
      for (int col = 0; col < 3; col++) {
        
        switchStates[keyMatrix[0][row][col]]= !digitalRead(mat1ColPins[col]);//Sets switch state to current inverted measurement
        switchStates[keyMatrix[1][row][col]]= !digitalRead(mat2ColPins[col]);//Sets switch state to current inverted measurement
        
      }
      digitalWrite(mat1RowPins[row], HIGH);//set the pint back to high to prevent misreads
      digitalWrite(mat2RowPins[row], HIGH);//set the pint back to high to prevent misreads
    }
  
    for (int swIndex=0; swIndex<18;swIndex++){
      if (switchStates[swIndex] != prevSwState[swIndex]) {
        timeSinceLastChange[swIndex] = 0;//Reset ever transition
      }
      if (timeSinceLastChange[swIndex] >= stablizationTime) {// Check that the timeout has occured
        dBSwState[swIndex] = switchStates[swIndex];
  
      }
      if(normalMode){
        keyPress(swIndex, switchStates[swIndex], prevSwState[swIndex], dBSwState[swIndex], prevDBSwState[swIndex]);
      }
      prevDBSwState[swIndex] = dBSwState[swIndex];
      prevSwState[swIndex] = switchStates[swIndex];
      
    }
    keymatriclastcheck=0;
  }
  
}
