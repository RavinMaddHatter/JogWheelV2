#custom module imports
import BoardHandler
import resolveManager
#imports for gui
import pygame
import pygame_gui
import sys
from button import Button, Knob, Key, BigKnob
import pygame_menu
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
serialPorts=[]
port=""
JB=""
for port, desc, hwid in sorted(ports):
    serialPorts.append([port, desc, hwid])

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG_Keys = pygame.image.load("assets/Keypad_Background.png")

surface = pygame.display.set_mode((800, 600))

menueStates={}

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Not Implemented", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(400, 200))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(400, 400), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green",callback=main_menu)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                PLAY_BACK.checkForInput(PLAY_MOUSE_POS)

        pygame.display.update()
KnobLocations=[(177,113,),(287,113,),(450,113,),(560,115,)]

KeyLocations=[(177,225),(177,317),(177,401),(177,488),
              (272,225),(272,317),
              (367,317),
              (461,225),(461,317),
              (555,225),(555,317),(555,401),(555,488)]
def settings():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        SCREEN.blit(BG_Keys, (0, 0))

        OPTIONS_BACK = Button(image=None, pos=(400, 50), 
                            text_input="HOME", font=get_font(60), base_color="#d7fcd4", hovering_color="White",callback=main_menu)
    
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        KNOBS=[]
        for i in range(len(KnobLocations)):
            KNOBS.append(Knob(27, KnobLocations[i], "#00000000", "#dddddd90",
                              configKnob,get_font(10),
                              JB.getKnobSettings(i),i))
            KNOBS[i].changeColor(OPTIONS_MOUSE_POS)
            KNOBS[i].update(SCREEN)
        BIG_KNOB=BigKnob(105, (292,410), "#00000000", "#dddddd90",confingBigKnob,get_font(14),JB.getBigKnobSettings())
        BIG_KNOB.changeColor(OPTIONS_MOUSE_POS)
        BIG_KNOB.update(SCREEN)
        KEYS=[]
        for i in range(len(KeyLocations)):
            KEYS.append(Key((57,57),15,KeyLocations[i],#key size, corner radius, and location
                            "#00000000","#dddddd90",#normal/hover color
                            configKey,get_font(10),
                            JB.getKeysSettings(i),i))
            KEYS[i].changeColor(OPTIONS_MOUSE_POS)
            KEYS[i].update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS)
                BIG_KNOB.checkForInput(OPTIONS_MOUSE_POS)
                for KNOB in KNOBS:
                    KNOB.checkForInput(OPTIONS_MOUSE_POS)
                for KEY in KEYS:
                    KEY.checkForInput(OPTIONS_MOUSE_POS)
        
        pygame.display.update()
        
def confingBigKnob():
    global menueStates
    keyIndex=JB.bigKnobKey
    menueStates=keyIndex
    menu = pygame_menu.Menu('Big Knob Config', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)
    defaults=JB.getButtonState(keyIndex)
    bigKnob=JB.getBigKnobSettings()
    menu.add.text_input('Press Key:', default=bigKnob[0],onchange=setKey)
    menu.add.text_input('Frame Forward:', default=bigKnob[3],onchange=setFrameForward)
    menu.add.text_input('Frame Backward :', default=bigKnob[4],onchange=setFrameBackward)
    menu.add.text_input('Play:', default=bigKnob[5],onchange=setPlay)
    menu.add.text_input('Rewind:', default=bigKnob[6],onchange=setRewind)
    menu.add.text_input('stop:', default=bigKnob[7],onchange=setStop)

    menu.add.selector('Modifier :', [('none', keyIndex),
                                     ('alt', keyIndex),
                                     ('ctrl', keyIndex),
                                     ('shift', keyIndex)],
                      default=defaults[0],
                      onchange=setKeyModifier)
    menu.add.selector('detection :', [('Normal', keyIndex),
                                     ('Rising', keyIndex),
                                     ('Falling', keyIndex)],
                      default=defaults[1],
                      onchange=setKeyDetection)
    menu.add.button('Save', reloadSettings)
    menu.mainloop(surface)
def setFrameForward(value):
    print(value)
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKey("Forward",value)
def setFrameBackward(value):
    value=value.upper()
    
    if value in JB.keyToInt.keys():
        JB.setKey("Backward",value)
def setPlay(value):
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKey("Play",value)
def setRewind(value):
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKey("Reverse",value)
def setStop(value):
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKey("Stop",value)
    
def configKey(keyIndex):
    global menueStates
    keyIndex=JB.defaultKeyMap[keyIndex]
    menueStates=keyIndex
    menu = pygame_menu.Menu('Key Config', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)
    defaults=JB.getButtonState(keyIndex)
    menu.add.text_input('Key :', default=JB.getKeysSettings(keyIndex)[0],onchange=setKey)
    menu.add.selector('Modifier :', [('none', keyIndex),
                                     ('alt', keyIndex),
                                     ('ctrl', keyIndex),
                                     ('shift', keyIndex)],
                      default=defaults[0],
                      onchange=setKeyModifier)
    menu.add.selector('detection :', [('Normal', keyIndex),
                                     ('Rising', keyIndex),
                                     ('Falling', keyIndex)],
                      default=defaults[1],
                      onchange=setKeyDetection)
    menu.add.button('Save', reloadSettings)
    
    menu.mainloop(surface)
def configKnob(knob_index): 
    global menueStates
    knob_index=[JB.defaultKeyMap[knob_index],knob_index]
    menueStates=knob_index
    menu = pygame_menu.Menu('Knob Config', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)
    knobSetting=JB.getKnobSettings(knob_index[1])
    defaults=JB.getButtonState(knob_index[0])
    menu.add.text_input('Press Key :', default=knobSetting[0],onchange=setKnobKey)
    menu.add.text_input('CCW Key :', default=knobSetting[3],onchange=setKnobCCW)
    menu.add.text_input('CW Key :', default=knobSetting[4],onchange=setKnobCW)

    menu.add.selector('Press Modifier :', [('none', knob_index),
                                     ('alt', knob_index),
                                     ('ctrl', knob_index),
                                     ('shift', knob_index)],
                      default=defaults[0],
                      onchange=setKnobModifier)
    menu.add.selector('Press detection :', [('Normal', knob_index),
                                     ('Rising', knob_index),
                                     ('Falling', knob_index)],
                      default=defaults[1],
                      onchange=setKnobDetection)
    menu.add.button('Save', reloadSettings)
    menu.mainloop(surface)
def setKnobKey(value):
    global menueStates
    print(menueStates)
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKey("Button",value,channel=JB.knobSwMap[menueStates[0]])
def setKnobCCW(value):
    global menueStates
    knobSetting=JB.getKnobSettings(menueStates[1])
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKnob(menueStates[1],knobSetting[3],value)
def setKnobCW(value):
    global menueStates
    knobSetting=JB.getKnobSettings(menueStates[1])
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKnob(menueStates[1],value,knobSetting[4])
def setKnobModifier(value,text):
    global menueStates
    match value[1]:
        case 0:
            
            JB.setAltState(JB.knobSwMap[menueStates[1]],False)
            JB.setCtrlState(JB.knobSwMap[menueStates[1]],False)
            JB.setShiftState(JB.knobSwMap[menueStates[1]],False)
        case 1:
            JB.setAltState(JB.knobSwMap[menueStates[1]],True)
            JB.setCtrlState(JB.knobSwMap[menueStates[1]],False)
            JB.setShiftState(JB.knobSwMap[menueStates[1]],False)
        case 2:
            JB.setAltState(JB.knobSwMap[menueStates[1]],False)
            JB.setCtrlState(JB.knobSwMap[menueStates[1]],True)
            JB.setShiftState(JB.knobSwMap[menueStates[1]],False)
        case 3:
            JB.setAltState(JB.knobSwMap[menueStates[1]],False)
            JB.setCtrlState(JB.knobSwMap[menueStates[1]],False)
            JB.setShiftState(JB.knobSwMap[menueStates[1]],True)

def setKnobDetection(value,text):
    match value[1]:
        case 0:
            JB.normalKeyState(menueStates[1])
        case 1:
            JB.risingEdgeKeyState(menueStates[1])
        case 2:
            JB.fallingEdgeKeyState(menueStates[1])
def reloadSettings():
    JB.readSettings()
    settings()
def setKey(value):
    global menueStates
    value=value.upper()
    if value in JB.keyToInt.keys():
        JB.setKey("Button",value,channel=menueStates)
def setKeyModifier(value,chan):
    global menueStates
    match value[1]:
        case 0:
            
            JB.setAltState(menueStates,False)
            JB.setCtrlState(menueStates,False)
            JB.setShiftState(menueStates,False)
        case 1:
            JB.setAltState(menueStates,True)
            JB.setCtrlState(menueStates,False)
            JB.setShiftState(menueStates,False)
        case 2:
            JB.setAltState(menueStates,False)
            JB.setCtrlState(menueStates,True)
            JB.setShiftState(menueStates,False)
        case 3:
            JB.setAltState(menueStates,False)
            JB.setCtrlState(menueStates,False)
            JB.setShiftState(menueStates,True)
def setKeyDetection(value,text):
    match value[1]:
        case 0:
            JB.normalKeyState(menueStates)
        case 1:
            JB.risingEdgeKeyState(menueStates)
        case 2:
            JB.fallingEdgeKeyState(menueStates)
def startConnection():
    global JB
    print(port)
    JB=BoardHandler.jogBoard(port)
    settings()
def selectPort(value, number):
    global port
    print(value)
    port=value[0][1]

def init():
    surface.blit(BG,(0,0))
    menu = pygame_menu.Menu('Setup', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)
    selections=[]
    for device in serialPorts:
        selections.append((device[0],device[0]))
    menu.add.selector('Serial port :', selections,
                      onchange=selectPort)

    menu.add.button('Connect', startConnection)
    menu.mainloop(surface)
def main_menu():
    
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                            text_input="INTERACTIVE", font=get_font(60), base_color="#d7fcd4", hovering_color="White",callback=play)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 375), 
                            text_input="SETTINGS", font=get_font(60), base_color="#d7fcd4", hovering_color="White",callback=settings)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 500), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White",callback=quitGame)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                PLAY_BUTTON.checkForInput(MENU_MOUSE_POS)
                OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS)
                QUIT_BUTTON.checkForInput(MENU_MOUSE_POS)
                    

        pygame.display.update()

def quitGame():
    JB.disconnect()
    pygame.quit()
    sys.exit()

init()
