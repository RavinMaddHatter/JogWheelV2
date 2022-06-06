#import pygame
import serial
import json
import time




## Things that i want.
## Interactive key rebinding
## rebind from files
## uart socket based gui override to provide better controll

class jogBoard:
    def __init__(self, port):
        self.keyToInt={}
        with open("keyboard.json","r") as file:
            self.keyToInt=json.load(file)
            if len(self.keyToInt.keys())==0:
                print("no keyboard description found")
        self.intToKey = {y: x for x, y in self.keyToInt.items()}
        self.port=port
        self.serial=serial.Serial(port,timeout=1)
        self.functions={}
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
            elif len(vals)==2:
                self.functions[vals[0]]=self.intToKey[int(vals[1])]
                print(vals[0]+": "+self.functions[vals[0]])
            elif len(vals)==3:
                bits=(8-len(vals[2]))*'0'+vals[2]
                self.functions[vals[0]]=[self.intToKey[int(vals[1])],bits]
                print(vals[0]+": "+self.intToKey[int(vals[1])]+" : "+self.functions[vals[0]][1])
    def saveState(self,function):
        function=function
        pin=function[-1]
        self.serial.write(("B {} {}\n\r".format(pin,int(self.functions[function][1],2))).encode())
    def setAltState(self,function,state):
        bits = self.functions[function][1]
        if state:
            bits[0]="1"
        else:
            bits[0]="0"
        self.functions[function][1]=bits
        self.saveState(function)
    def setCtrlState(self,function,state):
        bits = self.functions[function][1]
        if state:
            bits[1]="1"
        else:
            bits[1]="0"
        self.functions[function][1]=bits
        self.saveState(function)
    def setShiftState(self,function,state):
        bits = self.functions[function][1]
        bits=(8-len(bits))*'0'+bits
        if state:
            bits[2]="1"
        else:
            bits[2]="0"
        self.functions[function][1]=bits
        self.saveState(function)
    def normalKeyState(self,function):
        bits = self.functions[function][1]
        bits=bits[0:4]+"1000"
        self.functions[function][1]=bits
    def risingEdgeKeyState(self,function):
        bits = self.functions[function][1]
        bits=bits[0:4]+"0100"
        self.functions[function][1]=bits
        self.saveState(function)
    def fallingEdgeKeyState(self,function):
        bits = self.functions[function][1]
        bits = bits[0:4]+"0010"
        self.functions[function][1] = bits
        self.saveState(function)
    def setKey(self,function,key):
        if function in self.functions.keys():
            if key in self.keyToInt.keys():
                match function:
                    case "Frame forward key":
                        self.serial.write(("f "+str(self.keyToInt[key])).encode())
                    case "Frame backward key":
                        self.serial.write(("r "+str(self.keyToInt[key])).encode())
                    case "play key":
                        self.serial.write(("F "+str(self.keyToInt[key])).encode())
                    case "reverse key":
                        self.serial.write(("R "+str(self.keyToInt[key])).encode())
                    case "stop key":
                        self.serial.write(("s "+str(self.keyToInt[key])).encode())
                    case "simple button 0":
                        self.serial.write(("b 0 "+str(self.keyToInt[key])).encode())
                    case "simple button 1":
                        self.serial.write(("b 1 "+str(self.keyToInt[key])).encode())
                    case "simple button 2":
                        self.serial.write(("b 2 "+str(self.keyToInt[key])).encode())
                    case "simple button 3":
                        self.serial.write(("b 3 "+str(self.keyToInt[key])).encode())
                    case "simple button 4":
                        self.serial.write(("b 4 "+str(self.keyToInt[key])).encode())
                    case "simple button 5":
                        self.serial.write(("b 5 "+str(self.keyToInt[key])).encode())
                    case "simple button 6":
                        self.serial.write(("b 6 "+str(self.keyToInt[key])).encode())
                    case "simple button 7":
                        self.serial.write(("b 7 "+str(self.keyToInt[key])).encode())
                    case "simple button 8":
                        self.serial.write(("b 8 "+str(self.keyToInt[key])).encode())
                    case "simple button 9":
                        self.serial.write(("b 9 "+str(self.keyToInt[key])).encode())
                    case "simple button 10":
                        self.serial.write(("b 10 "+str(self.keyToInt[key])).encode())
                    case "simple button 11":
                        self.serial.write(("b 11 "+str(self.keyToInt[key])).encode())
                    case "simple button 12":
                        self.serial.write(("b 12 "+str(self.keyToInt[key])).encode())
                    case "simple button 13":
                        self.serial.write(("b 13 "+str(self.keyToInt[key])).encode())
                    case "simple button 14":
                        self.serial.write(("b 14 "+str(self.keyToInt[key])).encode())
                    case "simple button 15":
                        self.serial.write(("b 15 "+str(self.keyToInt[key])).encode())
                    case "simple button 16":
                        self.serial.write(("b 16 "+str(self.keyToInt[key])).encode())   
                    case "simple button 17":
                        self.serial.write(("b 17 "+str(self.keyToInt[key])).encode())                     
                self.readSettings()
    def disconnect(self):
        self.serial.close()
    def listOfKeys(self):
        return list(self.keyToInt.keys())

if __name__=="__main__":
    jb=jogBoard("COM3")
    jb.fallingEdgeKeyState("simple button 0")
    time.sleep(0.1)
    jb.risingEdgeKeyState("simple button 1")
    time.sleep(1)
    jb.readSettings()
    jb.disconnect()

