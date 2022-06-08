#import pygame
import serial
import json
import time




## Things that i want.
## rebind from files
## uart socket based gui override to provide better controll

class jogBoard:
    def __init__(self, port):
        self.defaultKeyMap=[0,1,2,3,#buttons collumn 1
                         4,5,#buttons collumn 2
                         6,#buttons collumn 3
                         7,8,#buttons collumn 4
                         9,10,11,12]#buttons collumn 5
        self.bigKnobKey=17# Bit button
        self.knobSwMap = [13,14,15,16]#bigNode
        self.keyToInt={}
        with open("keyboard.json","r") as file:
            self.keyToInt=json.load(file)
            if len(self.keyToInt.keys())==0:
                print("no keyboard description found")
        self.intToKey = {y: x for x, y in self.keyToInt.items()}
        self.port=port
        self.serial=serial.Serial(port,timeout=1)
        self.functions={}
        self.functions["Knob"]={}
        self.functions["Button"]={}
        self.functions["Forward"]={}
        self.functions["Reverse"]={}
        self.functions["Backward"]={}
        self.functions["Play"]={}
        self.functions["Stop"]={}
        self.readSettings()
    def readSettings(self):
        print("reading input")
        self.serial.reset_input_buffer()
        self.serial.write(b'p\n\r')
        startTime=time.time()
        keepReading=True
        
        while (time.time()-startTime)<5 and keepReading:
            line=self.serial.readline().decode()
            line=line.replace("\r\n","")
            vals=line.split(": ")
            if "END OF SETTINGS" in line:
                keepReading=False
            elif len(vals)>1:
                if "Forward" in vals[0]:
                    self.functions["Forward"]["key"]=self.intToKey[int(vals[1])]
                elif "Backward" in vals[0]:
                    self.functions["Backward"]["key"]=self.intToKey[int(vals[1])]
                elif "Play" in vals[0]:
                    self.functions["Play"]["key"]=self.intToKey[int(vals[1])]
                elif "Reverse" in vals[0]:
                    self.functions["Reverse"]["key"]=self.intToKey[int(vals[1])]
                elif "Stop" in vals[0]:
                    self.functions["Stop"]["key"]=self.intToKey[int(vals[1])]
                elif "Button" in vals[0]:
                    number=int(vals[0].split("-")[1])
                    self.functions["Button"][number]={}
                    self.functions["Button"][number]["Key"]=self.intToKey[int(vals[1])]
                    vals[2]="0"*(8-len(vals[2]))+vals[2]
                    self.functions["Button"][number]["Function"]=vals[2]
                elif "Knob" in vals[0]:
                    number=int(vals[0].split("-")[1])
                    self.functions["Knob"][number]={}
                    self.functions["Knob"][number]["Key1"]=self.intToKey[int(vals[1])]
                    self.functions["Knob"][number]["Key2"]=self.intToKey[int(vals[2])]
                    
                
    def saveState(self,channel,style="Button"):
        
        self.serial.write(("B {} {}\n\r".format(channel,int(self.functions[style][channel]["Function"],2))).encode())
    def getButtonState(self,channel,style="Button"):
        bits = self.functions[style][channel]["Function"]
        mod=0
        state=0
        if bits[0] == "1":
            mod=1
        elif bits[1] == "1":
            mod=2
        elif bits[2] == "1":
            mod=3
        if bits[4] == "1":
            state=0
        elif bits[5] == "1":
            state=1
        elif bits[6] == "1":
            state=2
        return [mod, state]
    def setAltState(self,channel,state,style="Button"):
        bits = self.functions[style][channel]["Function"]
        if state:
            bits = bits[:0] + "1" + bits[1:]
        else:
            bits = bits[:0] + "0" + bits[1:]
        self.functions[style][channel]["Function"]=bits
        self.saveState(channel)
    def setCtrlState(self,channel,state,style="Button"):
        bits = self.functions[style][channel]["Function"]
        if state:
            bits = bits[:1] + "1" + bits[2:]
        else:
            bits = bits[:1] + "0" + bits[2:]
        self.functions[style][channel]["Function"]=bits
        self.saveState(channel)
    def setShiftState(self,channel,state,style="Button"):
        bits = self.functions[style][channel]["Function"]
        bits=(8-len(bits))*'0'+bits
        if state:
            bits = bits[:2] + "1" + bits[3:]
        else:
            bits = bits[:2] + "0" + bits[3:]
        self.functions[style][channel]["Function"]=bits
        self.saveState(channel)
    def normalKeyState(self,channel,style="Button"):
        bits = self.functions[style][channel]["Function"]
        bits=bits[0:4]+"1000"
        self.functions[style][channel]["Function"]=bits
        self.saveState(channel)
    def risingEdgeKeyState(self,channel,style="Button"):
        bits = self.functions[style][channel]["Function"]
        bits=bits[0:4]+"0100"
        self.functions[style][channel]["Function"]=bits
        self.saveState(channel)
    def fallingEdgeKeyState(self,channel,style="Button"):
        bits = self.functions[style][channel]["Function"]
        bits = bits[0:4]+"0010"
        self.functions[style][channel]["Function"]=bits
        self.saveState(channel)
    def setKey(self,style,key,channel=0):
        if style in self.functions.keys():
            if key in self.keyToInt.keys():
                match style:
                    case "Forward":
                        self.serial.write(("f "+str(self.keyToInt[key])).encode())
                    case "Backward":
                        self.serial.write(("r "+str(self.keyToInt[key])).encode())
                    case "Play":
                        self.serial.write(("F "+str(self.keyToInt[key])).encode())
                    case "Reverse":
                        self.serial.write(("R "+str(self.keyToInt[key])).encode())
                    case "Stop":
                        self.serial.write(("s "+str(self.keyToInt[key])).encode())
                    case "Button":
                        command="b {} {}\n\r".format(channel,self.keyToInt[key])
                        self.serial.write(command.encode())
                    case "Knob":
                        command="b {} {}\n\r".format(channel,self.keyToInt[key])
                        self.serial.write(command.encode())
                #self.readSettings()
    def setKnob(self,channel,key_forward,key_backward):
        command="k {} {} {}\n\r".format(channel,self.keyToInt[key_backward],self.keyToInt[key_forward])
        self.serial.write(command.encode())
    def disconnect(self):
        self.serial.close()
    def getKeysSettings(self,key_setting):
        mappedKey=self.defaultKeyMap[key_setting]
        keyValue=self.functions["Button"][mappedKey]["Key"]
        keyFunction=self.parseFunction(self.functions["Button"][mappedKey]["Function"])
        return [keyValue,keyFunction[0],keyFunction[1]]
    def getKnobSettings(self,knob_number):
        mappedKey=self.defaultKeyMap[knob_number]
        keyValue=self.functions["Button"][mappedKey]["Key"]
        keyFunction=self.parseFunction(self.functions["Button"][mappedKey]["Function"])
        fwd=self.functions["Knob"][knob_number]["Key1"]
        rv=self.functions["Knob"][knob_number]["Key2"]
        return [keyValue,keyFunction[0],keyFunction[1],fwd,rv]
    def getBigKnobSettings(self):
        keyValue=self.functions["Button"][self.bigKnobKey]["Key"]
        keyFunction=self.parseFunction(self.functions["Button"][self.bigKnobKey]["Function"])
        stpFwd=self.functions["Forward"]["key"]
        stpBck=self.functions["Backward"]["key"]
        play=self.functions["Play"]["key"]
        reverse=self.functions["Reverse"]["key"]
        stop=self.functions["Stop"]["key"]
        return [keyValue,keyFunction[0],keyFunction[1],stpFwd,stpBck,play,reverse,stop]
    def parseFunction(self,function):
        modifiers=""
        op=""
        if function[0] =="1":
            modifiers+="alt+"
        if function[1] =="1":
            modifiers+="ctrl+"
        if function[2] =="1":
            modifiers+="shft+"
        if function[6]=="1":
            op="falling"
        if function[5]=="1":
            op="rising"
        if function[4]=="1":
            op=""
            
        return [modifiers,op]
    def listOfKeys(self):
        return list(self.keyToInt.keys())

if __name__=="__main__":
    jb=jogBoard("COM3")
    jb.fallingEdgeKeyState(0)
    time.sleep(0.1)
    jb.risingEdgeKeyState(1)
    time.sleep(1)
    jb.readSettings()
    print(json.dumps(jb.functions,indent=2))
    jb.disconnect()

