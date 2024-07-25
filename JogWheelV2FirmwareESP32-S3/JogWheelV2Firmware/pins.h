#define knob1A 12
#define knob1B 13
#define knob3A 11
#define knob3B 10
#define knob4A 18
#define knob4B 15
#define knob2A 7
#define knob2B 6
#define wheelA 34
#define wheelB 33

#define leftButtonsA 9
#define leftButtonsB 14
#define leftButtonsC 39
#define leftButtons1 21
#define leftButtons2 48
#define leftButtons3 47
//
#define rightButtonsA 4
#define rightButtonsB 45
#define rightButtonsC 38
#define rightButtons1 3
#define rightButtons2 8
#define rightButtons3 5

byte mat1RowPins[]={leftButtonsA, leftButtonsB, leftButtonsC};
byte mat2RowPins[] = {rightButtonsA, rightButtonsB, rightButtonsC};
byte mat1ColPins[] = {leftButtons1, leftButtons2, leftButtons3};
byte mat2ColPins[] = {rightButtons1, rightButtons2, rightButtons3};

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
