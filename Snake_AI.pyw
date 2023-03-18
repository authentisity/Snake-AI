import pygame
import random, time, math
import resources


pygame.init()
SCREEN_WIDTH = SCREEN_HEIGHT = BOARD_SIZE = MOVE_CAP = POPULATION_SIZE = 0
screen = None

default_font = pygame.font.Font(pygame.font.get_default_font(), 48)

class block:
            # Empty 1        Empty 2        Snake Body    Snake Head   Apple
    colors = [(124, 252, 0), (50, 196, 35), (75, 75, 75), (0, 0, 205), (255, 0, 0)]
    instances = []

    def __init__(self, id):
        self.base_color = self.color = block.colors[0] if (id[0] + id[1]) % 2 == 0 else block.colors[1]
        self.id = id
        self.surrounding = 0

        self.rect = (self.id[0] * SCREEN_WIDTH / BOARD_SIZE, self.id[1] * SCREEN_HEIGHT / BOARD_SIZE, SCREEN_WIDTH / BOARD_SIZE, SCREEN_HEIGHT / BOARD_SIZE)
        pygame.draw.rect(screen, self.color, self.rect)
        block.instances.append(self)

    def update(self, color = False):
        self.color = block.colors[color] if color else self.base_color
        pygame.draw.rect(screen, self.color, self.rect)
        return self
    
    @classmethod
    def find(cls, id):
        for i in cls.instances:
            if i.id == id:
                return i 
        return None


class NN:

    def __init__(self):
        pass

    def predict(self):
        pass

    def mutate(self):
        pass


class Snake:

    generation = 1
    instances = []

    def __init__(self):
        # default starting position
        self.length, self.head, self.direction = 3, [int(BOARD_SIZE / 2), BOARD_SIZE - 4], [0, -1]
        self.blocks = [block.find([self.head[0], self.head[1] + 2]).update(2), block.find([self.head[0], self.head[1] + 1]).update(2), block.find(self.head).update(3)]
        self.specimen, self.moves_remaining = len(Snake.instances) + 1, MOVE_CAP + 1
        self.brain = NN()
        Snake.instances.append(self)

    def add_block(self, inst):
        self.head = inst.id
        self.blocks.append(inst.update(3))
        self.blocks[-2].update(2)

    def remove_block(self):
        self.blocks.pop(0).update()

    def clear(self):
        for i in self.blocks:
            i.update()

    def update(self, direction):
        if direction != [-i for i in self.direction]:
            self.direction = direction
        new_block = block.find([i + j for i, j in zip(self.head, self.direction)])
        if new_block == None:
            return 1

        c = block.colors.index(new_block.color)
        if c <= 1:
            self.remove_block()
            self.add_block(new_block)
        elif c == 4:
            self.length += 1
            self.add_block(new_block)
            return 2
        elif c == 2:
            return 1

    @classmethod
    def regenerate(cls):
        # calculate fitness
        Snake.instances.sort(key=lambda x : x.length)
        print([i.length for i in Snake.instances])

        del Snake.instances
        Snake.instances = []
        for i in range(POPULATION_SIZE):
            Snake()
        Snake.generation += 1



class Apple:
    
    def __init__(self):
        self.pos = [int(BOARD_SIZE / 2), 1]
        block.find(self.pos).update(4)

    def update(self, snake):
        self.pos = random.choice([i.id for i in block.instances if i not in snake.blocks])
        block.find(self.pos).update(4)
    
    def clear(self):
        block.find(self.pos).update()




def main():
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    [[block([i, j]) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    [Snake() for i in range(POPULATION_SIZE)]
    game_over = False
    screen.blits([(default_font.render("Gen: 1", True, (0, 0, 0)), (0, SCREEN_HEIGHT)), (default_font.render("Specimen:", True, (0, 0, 0)), (SCREEN_WIDTH / 2, SCREEN_HEIGHT)), (default_font.render("Score:", True, (0, 0, 0)), (0, SCREEN_HEIGHT + 48)), (default_font.render("Turns left:", True, (0, 0, 0)), (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 48))])
    while True:
        for i in Snake.instances:
            apple = Apple()
            screen.fill((255, 255, 255), (SCREEN_WIDTH / 2 + 240, SCREEN_HEIGHT, 200, 48))
            screen.blit(default_font.render(str(i.specimen), True, (0, 0, 0)), (SCREEN_WIDTH / 2 + 240, SCREEN_HEIGHT))
            while not game_over:
                clock.tick(5)
                direction = i.direction
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            exit(0)
                        elif e.key == pygame.K_r:
                            return
                        elif e.key == pygame.K_UP:
                            direction = [0, -1]
                        elif e.key == pygame.K_DOWN:
                            direction = [0, 1]
                        elif e.key == pygame.K_LEFT:
                            direction = [-1, 0]
                        elif e.key == pygame.K_RIGHT:
                            direction = [1, 0]
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pressed = pygame.mouse.get_pressed()
                        if mouse_pressed[0] != 0:
                            pos = pygame.mouse.get_pos()
                            location = int(pos[0] / SCREEN_WIDTH * 10) + int(pos[1] / SCREEN_HEIGHT * 10) * 10
                            if location > 100:
                                break
                                game_over = True
                        if mouse_pressed[2] != 0:
                            pos = pygame.mouse.get_pos()
                    elif e.type == pygame.QUIT:
                        exit(0)


                result = i.update(direction)
                i.moves_remaining -= 1
                if result == 1:
                    break
                elif result == 2:
                    apple.update(i)
                    i.moves_remaining = MOVE_CAP
                if i.moves_remaining == 0:
                    break

                screen.fill((255, 255, 255), (160, SCREEN_HEIGHT + 48, 200, 48))
                screen.fill((255, 255, 255), (SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT + 48, 200, 48))
                screen.blits([(default_font.render(str(i.length - 3), True, (0, 0, 0)), (160, SCREEN_HEIGHT + 48)), (default_font.render(str(i.moves_remaining), True, (0, 0, 0)), (SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT + 48))])
                pygame.display.update()
               
            # clear visuals
            i.clear()
            apple.clear()

        # regenerate individuals
        Snake.regenerate()
        screen.fill((255, 255, 255), (130, SCREEN_HEIGHT, 200, 48))
        screen.blit(default_font.render(str(Snake.generation), True, (0, 0, 0)), (130, SCREEN_HEIGHT))

    while 1:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    exit(0)
                elif e.key == pygame.K_r:
                    return
            elif e.type == pygame.QUIT:
                exit(0)


def init(screenW = 800, screenH = 800, size = 10, move_cap = -1, population_size = 50):
    global SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE, screen, MOVE_CAP, POPULATION_SIZE
    # minimum game size: 10
    size = max(size, 10)
    SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE, MOVE_CAP, POPULATION_SIZE = round(screenW / float(size)) * size, round(screenH / float(size)) * size, size, move_cap, population_size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 200))
    pygame.display.set_caption("Snake")
    resources.init(screen)

def reset():
    block.instances = []

#edit training variables
init(size = 20, move_cap = 20, population_size = 2)


if __name__ == "__main__":
    while 1:
        main()
        reset()