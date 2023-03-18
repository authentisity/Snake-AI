import pygame, math

global screen

def init(scr):
    global screen
    screen = scr


class input_box():
    instances = []
    def __init__(self, pos, size, filler = "Enter text here", color = (155, 155, 155), title = "Input"):
        self.pos, self.size = pos, (size[0] * 25, size[1])
        self.filler, self.color, self.title = filler, color, title
        pygame.draw.rect(screen, (0, 0, 0), (self.pos, self.size), 1)
        screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] * 0.9)).render(self.title, True, self.color), (self.pos[0], self.pos[1] - self.size[1]))
        screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] * 0.9)).render(self.filler, True, self.color), (self.pos[0], self.pos[1] + self.size[1] * 0.05))
        self.caplock, self.text= False, ""
        self.id = len(input_box.instances)
        input_box.instances.append(self)

    def __call__(self):
        return self.id
    
    @classmethod
    def get_selected(cls, pos):
        for i in cls.instances:
            for j in (0, 1):
                if i.pos[j] > pos[j] or i.pos[j] + i.size[j] < pos[j]:
                    break
            else:
                return i
        return None

    def update(self, char = 0x110000):
        if char == pygame.K_RETURN:
            return self.text
        elif char == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif char == pygame.K_LSHIFT or char == pygame.K_RSHIFT:
            self.caplock = not self.caplock
        elif char < 0x110000:
            self.text += chr(char - (32 if (self.caplock and char > 96 and char < 123) else 0))
        screen.fill((255, 255, 255), (self.pos, self.size))
        pygame.draw.rect(screen, (0, 0, 0), (self.pos, self.size), 1)
        if self.text != "":
            screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] * 0.9)).render(self.text, True, (0, 0, 0)), (self.pos[0], self.pos[1] + self.size[1] * 0.05))
        else:
            screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] * 0.9)).render(self.filler, True, self.color), (self.pos[0], self.pos[1] + self.size[1] * 0.05))

    def clear(self):
        self.caplock, self.text= False, ""
        screen.fill((255, 255, 255), (self.pos, self.size))
        pygame.draw.rect(screen, (0, 0, 0), (self.pos, self.size), 1)
        screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] * 0.9)).render(self.filler, True, self.color), (self.pos[0], self.pos[1] + self.size[1] * 0.05))


class slider():

    instances = []

    def __init__(self, pos, txt, size = (200, 200), bar_color = (155, 155, 155), lever_color = (0, 0, 0)):
        self.x, self.y = pos
        self.size = size
        self.bar_color, self.lever_color = bar_color, lever_color
        self.bar = pygame.draw.rect(screen, self.bar_color, (self.x, self.y, int(self.size[0] / 3), self.size[1]))
        self.lever = pygame.draw.rect(screen, self.lever_color, (self.x - self.size[0] / 3, self.y + self.size[1], self.size[0], int(self.size[1] / 20)))
        self.rect_title = screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] / len(txt))).render(txt, True, (0, 0, 0)), (self.x - self.size[1] / 6, self.y - self.size[1] / 3))
        self.value = 0
        screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] / 5)).render(str("{:.2f}".format(self.value)), True, (0, 0, 0)), self.lever.move(0, self.size[1] / 20))
        slider.instances.append(self)

    def update(self, pos):
        x, y = pos
        if abs(x - self.x - self.size[0] * 0.2) < self.size[0] * 0.6:
            if y < self.y - self.size[1] * 0.2 or y > self.y + self.size[1] * 1.2:
                return
            if y < self.y:
                y = self.y
            elif y > self.y + self.size[1]:
                y = self.y + self.size[1]
            screen.fill((255, 255, 255), self.lever.inflate(0, int(self.size[1] / 5)).move(0, self.size[1] / 10))
            self.value = 100 - (y - self.y) / self.size[1] * 100
            pygame.draw.rect(screen, self.bar_color, self.bar)
            self.lever = pygame.draw.rect(screen, self.lever_color, (self.x - self.size[0] / 3, y, self.size[0], int(self.size[1] / 20)))
            screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] / 5)).render(str("{:.2f}".format(self.value)), True, (0, 0, 0)), self.lever.move(0, self.size[1] / 20))

    def update_title(self, title = None):
        if title == None:
            return
        screen.fill((255, 255, 255), self.rect_title)
        self.rect_title = screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[1] / len(title))).render(title, True, (0, 0, 0)), (self.x - self.size[1] / 6, self.y - self.size[1] / 3))
    
class button():

    instances = []
    def __init__(self, pos, size, color = (255, 0, 0), txt = "Title"):
        self.pos, self.size, self.color, self.txt = pos, size, color, txt
        self.rect = pygame.draw.rect(screen, self.color, (self.pos, self.size))
        screen.blit(pygame.font.Font(pygame.font.get_default_font(), int(self.size[0] / len(self.txt) * 2)).render((self.txt), True, (0, 0, 0)), self.rect)
        button.instances.append(self)

    def update(self, pos):
        if self.rect.contains(pos, (0, 0)):
            return True
        return False