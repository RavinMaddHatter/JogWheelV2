#define knob1A 5
#define knob1B 4 
#define knob3A 17
#define knob3B 18
#define knob4A 21
#define knob4B 21
#define knob2A 1
#define knob2B 2
#define wheelA 10
#define wheelB 11

#define leftButtonsA 0
#define leftButtonsB 8
#define leftButtonsC 9
#define leftButtons1 3
#define leftButtons2 7
#define leftButtons3 6
//
#define rightButtonsA 23
#define rightButtonsB 20
#define rightButtonsC 14
#define rightButtons1 15
#define rightButtons2 16
#define rightButtons3 19


//old
//#define knob1A 17 
//#define knob1B 16 
//#define knob2A 11
//#define knob2B 10
//#define knob3A 15
//#define knob3B 14
//#define wheelA 0
//#define wheelB 1
//#define bigWheelButtonPin 9
//#define bottomKnobButtonPin 12
//#define middleKnobButtonPin 8
//#define topKnobButtonPin 13
//#define leftButtonsA 23
//#define leftButtonsB 22
//#define leftButtonsC 18
//#define leftButtons1 21
//#define leftButtons2 20
//#define leftButtons3 19
//#define rightButtonsA 2
//#define rightButtonsB 6
//#define rightButtonsC 7
//#define rightButtons1 3
//#define rightButtons2 5
//#define rightButtons3 4

byte mat1RowPins[]={leftButtonsA, leftButtonsB, leftButtonsC};
byte mat2RowPins[] = {rightButtonsA, rightButtonsB, rightButtonsC};
byte mat1ColPins[] = {leftButtons1, leftButtons2, leftButtons3};
byte mat2ColPins[] = {rightButtons1, rightButtons2, rightButtons3};

//const byte keyMatrix[2][3][3] = {
//  {
//    {0, 0, 0},
//    {0, 0, 0},
//    {0, 0, 0}
//  },
//  {
//    {0, 0, 17},
//    {0, 0, 15},
//    {0, 0, 9}
//  }
//};

const byte keyMatrix[2][3][3] = {
  {
    {13, 14, 0},
    {1, 4, 3},
    {2, 5, 6}
  },
  {
    {10, 15, 16},
    {8, 7, 9},
    {11, 12, 17}
  }
};
