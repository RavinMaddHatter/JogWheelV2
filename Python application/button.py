import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color,callback):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.callback = callback
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.callback()
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class Knob():
    def __init__(self, radius, pos, base_color, hovering_color,callback,font,settings,knob_index):
        self.radius = radius
        self.knob_index=knob_index
        self.font=font
        self.key=settings[0]
        self.rev=settings[3]
        self.fwd=settings[4]
        self.callback = callback
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.base_color, self.hovering_color = base_color, hovering_color
        self.surface = pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface,self.base_color,(self.radius,self.radius),self.radius)
        self.line1 = self.font.render(self.key, True, "Black")
        self.line2 = self.font.render(self.rev, True, "Black")
        self.line3 = self.font.render(self.fwd, True, "Black")
    def update(self, screen):
        screen.blit(self.surface,(self.x_pos,self.y_pos,))
        borders=self.surface.get_rect()
        size=self.line1.get_rect()
        x=self.x_pos+(borders[2]-size[2])/2
        y=self.y_pos+(borders[3]-size[3])/2
        screen.blit(self.line1,(x,y,))
        screen.blit(self.line2,(self.x_pos,y,))
        size=self.line3.get_rect()
        x=self.x_pos+borders[2]-size[2]
        screen.blit(self.line3,(x,y,))
    def checkForInput(self, position):
        if position[0] in range(self.x_pos, self.x_pos+self.radius*2) and position[1] in range(self.y_pos, self.y_pos+self.radius*2):
            self.callback(self.knob_index)
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.x_pos, self.x_pos+self.radius*2) and position[1] in range(self.y_pos, self.y_pos+self.radius*2):
            pygame.draw.circle(self.surface,self.hovering_color,(self.radius,self.radius),self.radius)
        else:
            pygame.draw.circle(self.surface,self.base_color,(self.radius,self.radius),self.radius)


class BigKnob():
    def __init__(self, radius, pos, base_color, hovering_color,callback,font,settings):
        
        self.radius = radius
        self.font=font
        self.key=settings[0]
        self.rev=settings[3]
        self.fwd=settings[4]
        self.play=settings[5]
        self.reverse=settings[6]
        self.callback = callback
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.base_color, self.hovering_color = base_color, hovering_color
        self.surface = pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface,self.base_color,(self.radius,self.radius),self.radius)
        self.line1 = self.font.render(self.key, True, "Black")
        self.line2 = self.font.render(self.reverse, True, "Black")
        self.line3 = self.font.render(self.play, True, "Black")
        self.line4 = self.font.render(self.rev, True, "Black")
        self.line5 = self.font.render(self.fwd, True, "Black")
    def update(self, screen):
        screen.blit(self.surface,(self.x_pos,self.y_pos,))
        borders=self.surface.get_rect()
        size=self.line1.get_rect()
        x=self.x_pos+(borders[2]-size[2])/2
        y=self.y_pos+(borders[3]-size[3])/2
        screen.blit(self.line1,(x,y,))
        screen.blit(self.line2,(self.x_pos,y,))
        size=self.line3.get_rect()
        x=self.x_pos+borders[2]-size[2]
        screen.blit(self.line3,(x,y,))
        y=self.y_pos+(borders[3]-size[3])/4
        x=self.x_pos+borders[2]-size[2]
        screen.blit(self.line4,(self.x_pos+borders[2]*.1,y,))
        size=self.line5.get_rect()
        x=self.x_pos+borders[2]*.9-size[2]
        screen.blit(self.line5,(x,y,))
    def checkForInput(self, position):
        if position[0] in range(self.x_pos, self.x_pos+self.radius*2) and position[1] in range(self.y_pos, self.y_pos+self.radius*2):
            self.callback()
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.x_pos, self.x_pos+self.radius*2) and position[1] in range(self.y_pos, self.y_pos+self.radius*2):
            pygame.draw.circle(self.surface,self.hovering_color,(self.radius,self.radius),self.radius)
        else:
            pygame.draw.circle(self.surface,self.base_color,(self.radius,self.radius),self.radius)




class Key():
    def __init__(self, size,corner_radius, pos, base_color, hovering_color,callback,font,key_function,keyIndex):
        self.size = size
        self.keyIndex=keyIndex
        self.callback = callback
        self.radius=corner_radius
        self.key=key_function[0]
        self.function=key_function[1]
        self.state=key_function[2]
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font=font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(self.surface,self.base_color,pygame.Rect((0,0),self.size),border_radius=self.radius)
        self.line1 = self.font.render(self.key, True, "Black")
        self.line2 = self.font.render(self.function, True, "Black")
        self.line3 = self.font.render(self.state, True, "Black")
    def update(self, screen):
        screen.blit(self.surface,(self.x_pos,self.y_pos,))
        sizekey=self.surface.get_rect()
        sizetext=self.line1.get_rect()
        screen.blit(self.line1,(self.x_pos+(sizekey[2]-sizetext[2])/2,self.y_pos+20,))
        sizetext=self.line2.get_rect()
        screen.blit(self.line2,(self.x_pos+(sizekey[2]-sizetext[2])/2,self.y_pos+5,))
        
        sizetext=self.line3.get_rect()
        screen.blit(self.line3,(self.x_pos+(sizekey[2]-sizetext[2])/2,self.y_pos+35,))
    def checkForInput(self, position):
        if position[0] in range(self.x_pos, self.x_pos+self.size[0]) and position[1] in range(self.y_pos, self.y_pos+self.size[1]):
            self.callback(self.keyIndex)
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.x_pos, self.x_pos+self.size[0]) and position[1] in range(self.y_pos, self.y_pos+self.size[1]):
            pygame.draw.rect(self.surface,self.hovering_color,pygame.Rect((0,0),self.size),border_radius=self.radius)
        else:
            pygame.draw.rect(self.surface,self.base_color,pygame.Rect((0,0),self.size),border_radius=self.radius)

