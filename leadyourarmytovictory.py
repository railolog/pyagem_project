import pygame
from random import *
import traceback
from pygame import transform as rotate
game_number = input('''Введите номер волны, с которой хотитите
начать или Enter, если хотите начать новую игру(<=54): ''')
if game_number == '':
    game_number = 1
else:
    game_number = int(game_number)
if game_number > 54:
    game_number = 54
pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

HPnPWnRange = {'archer': [50, 35, 4], 'elven': [10, 80, 3],
               'knight': [100, 40, 1.5], 'orc': [85, 35, 1.5],
               'skeleton': [41, 35, 4]}
heroes = {}
victory, lose = [False] * 2
mouse_im = pygame.image.load('media/mouse_im.png')


def draw(animated=None):
    bg = pygame.image.load('media/bg/bg1.jpg')
    screen.blit(bg, (0, 0))
    board.render()
    for key, value in heroes.items():
        if key == animated:
            screen.blit(key.anim, value)
        else:
            screen.blit(key.stand, value)
    screen.blit(mouse_im, mouse_pos)
    pygame.display.flip()


running = True

blue_rect = pygame.Surface((60, 60))  # the size of your rect
blue_rect.set_alpha(50)                # alpha level
blue_rect.fill(pygame.Color('blue'))           # this fills the entire surface
red_rect = pygame.Surface((60, 60))
red_rect.set_alpha(50)
red_rect.fill(pygame.Color('red'))

color = pygame.Color('white')
hsv = color.hsva
color.hsva = (hsv[0], hsv[1], hsv[2] - 15, hsv[3])


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.s = pygame.Surface((60, 60))
        self.s.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.s, (255, 255, 255), (0, 0, 60, 60), 2)
        self.s.set_alpha(100)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def reset(self):
        for x in range(19):
            for y in range(6):
                self.board[y][x] = 0

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                x1 = x * self.cell_size + self.left
                y1 = y * self.cell_size + self.top
                w = 2
                if self.board[y][x] == 'reachable':
                    screen.blit(blue_rect, (x1, y1))
                try:
                    if self.board[y][x][-1] == 'attackable':
                        screen.blit(red_rect, (x1, y1))
                except TypeError:
                    pass
                screen.blit(self.s, (x1, y1))

    def get_cell(self, mouse_pos):
        rel_x, rel_y = mouse_pos[0] - self.left, mouse_pos[1] - self.top
        if self.width * self.cell_size < rel_x or rel_x < 0\
           or rel_y < 0 or rel_y > self.height * self.cell_size:
            return None
        else:
            return (rel_x // self.cell_size, rel_y // self.cell_size)

    def on_click(self, cell_coords):
        x, y = cell_coords[0], cell_coords[1]
        global code
        if code == 0:
            if type(self.board[y][x]) == Hero:
                self.board[y][x].reachable_cells()
                self.board[y][x].attackable_cells()
                self.chosen_hero = self.board[y][x]
                code += 1
        elif code == 1:
            if self.board[y][x] == 'reachable':
                self.chosen_hero.move(x, y)
                code = 2
            elif type(self.board[y][x]) == Hero:
                board.clear()
                code = 0
            elif self.board[y][x] == 0:
                return
            try:
                if self.board[y][x][-1] == 'attackable':
                    self.chosen_hero.attack(x, y)
                    code = 2
            except TypeError:
                pass
            board.on_click([x, y])
        elif not any(type(self.board[y][x]) == Enemy
                     for x in range(19)for y in range(6)):
            global victory
            victory = True
            return
        elif code == 2:
            code = 0
            AI()
        if not any(type(self.board[y][x]) == Hero
                   for x in range(19)for y in range(6)):
            global lose
            lose = True

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                try:
                    if type(self.board[y][x][-1]) == str:
                        self.board[y][x] = self.board[y][x][0]
                    if type(self.board[y][x]) == str:
                        self.board[y][x] = 0
                except TypeError:
                    if type(self.board[y][x]) == str:
                        self.board[y][x] = 0


vals = {'archer': 13, 'elven': 7, 'knight': 9, 'orc': 7, 'skeleton': 14}


class Hero:
    def __init__(self, char, x, y):
        self.hp, self.pw = HPnPWnRange[char][:2]  # задаем очки здоровья и силы
        self.stand = pygame.image.load('media/{}/walk/1.png'.format(char))
        self.walk_anim = [pygame.image.load
                          ('media/{}/walk/{}.png'.
                           format(char, str(i))) for i in range(1, 10)]
        self.attack_anim = [pygame.image.load
                            ('media/{}/attack/{}.png'.format(char, str(i)))
                            for i in range(1, vals[char])]
        self.hurt_anim = [pygame.image.load
                          ('media/{}/hurt/{}.png'.format(char, str(i)))
                          for i in range(1, 7)]
        self.x, self.y = x, y
        heroes[self] = [self.x * 60 + board.left + 2,
                        self.y * 60 + board.top + 5]
        board.board[y][x] = self
        self.Range = HPnPWnRange[char][2]

    def reachable_cells(self):
        for x in range(19):
            for y in range(6):
                hypo = int(((x - self.x)**2 + (y - self.y)**2)**0.5)
                if hypo <= 3 and board.board[y][x] == 0:
                    board.board[y][x] = 'reachable'

    def attackable_cells(self):
        for x in range(19):
            for y in range(6):
                hypo = int(((x - self.x)**2 + (y - self.y)**2)**0.5)
                if hypo <= self.Range and type(board.board[y][x]) == Enemy:
                    board.board[y][x] = [board.board[y][x], 'attackable']

    def attack(self, x, y):
        try:
            if board.board[y][x][-1] == 'attackable':
                i = 0
                board.clear()
                time = clock.tick()
                while i < len(self.attack_anim):
                    time = clock.tick() / 1000
                    i = (i + time * 10)
                    if self.x > x:
                        self.anim = rotate.flip(self.
                                                attack_anim
                                                [int(i %
                                                     len(self.attack_anim))],
                                                1, 0)
                    else:
                        self.anim = self.attack_anim[int(i %
                                                         len(self.attack_anim))]
                    draw(self)
                board.board[y][x].hurt(self.pw)
        except TypeError:
            pass

    def hurt(self, power):
        self.hp -= power
        i = 0
        time = clock.tick()
        while i <= 5:
            time = clock.tick() / 1000
            i = (i + time * 10)
            self.anim = self.hurt_anim[int(i % 6)]
            draw(self)
        if self.hp <= 0:
            board.board[self.y][self.x] = 0
            del heroes[self]

    def move(self, x, y):
        v_x, v_y = [None] * 2
        x1 = x * 60 + board.left + 2
        y1 = y * 60 + board.top + 5
        i = 0
        time = clock.tick()
        board.clear()
        while v_x != 0 or v_y != 0:
            pos = heroes[self]
            d_x, d_y = x1 - int(pos[0]), y1 - int(pos[1])
            if d_x < 0:
                v_x = -35
            elif d_x > 0:
                v_x = 35
            else:
                v_x = 0
            if d_y < 0:
                v_y = -35
            elif d_y > 0:
                v_y = 35
            else:
                v_y = 0
                if d_x < 0:
                    v_x = -60
                if d_x > 0:
                    v_x = 60
            if v_x == 0:
                if d_y < 0:
                    v_y = -60
                if d_y > 0:
                    v_y = 60
            time = clock.tick() / 1000
            i = (i + time * 10) % 9
            if v_x < 0:
                self.anim = rotate.flip(self.walk_anim[int(i)], 1, 0)
            else:
                self.anim = self.walk_anim[int(i)]
            pos[0] += v_x * time
            pos[1] += v_y * time
            heroes[self] = [int(pos[0]), int(pos[1])]
            draw(self)
        board.board[y][x], board.board[self.y][self.x] = self, 0
        self.x, self.y = x, y


class Enemy(Hero):
    def __init__(self, char, x, y):
        super().__init__(char, x, y)
        if char == 'orc':
            self.stand = rotate.flip(pygame.image.load
                                     ('media/{}/walk/1.png'.format(char)), 1, 0)
            self.walk_anim = [rotate.flip(pygame
                                          .image.load('media/{}/walk/{}.png'.
                                                      format(char, str(i))),
                                          1, 0) for i in range(1, 10)]
            self.attack_anim = [rotate.flip(pygame.
                                            image.load('media/{}/attack/{}.png'
                                                       .format(char, str(i))),
                                            1, 0) for i in range(1, vals[char])]
            self.hurt_anim = [rotate.flip(pygame.image.load
                                          ('media/{}/hurt/{}.png'.
                                           format(char,str(i))),
                                          1, 0) for i in range(1, 7)]
        self.attack_anim = [rotate.flip(i, 1, 0) for i in self.attack_anim]
        self.walk_anim = [rotate.flip(i, 1, 0) for i in self.walk_anim]

    def attackable_heroes(self):
        attackables = []
        for x in range(19):
            for y in range(6):
                hypo = int(((x - self.x)**2 + (y - self.y)**2)**0.5)
                if hypo <= self.Range and type(board.board[y][x]) == Hero:
                    attackables.append(board.board[y][x])
        return attackables

    def reachable_cells(self):
        reachables = []
        for x in range(19):
            for y in range(6):
                hypo = int(((x - self.x)**2 + (y - self.y)**2)**0.5)
                if hypo <= 3 and board.board[y][x] == 0:
                    reachables.append((x, y))
        return reachables


def AI():
    enemies = []
    attacked = False
    for char in heroes.keys():
        if type(char) == Enemy:
            enemies.append(char)
    for enemy in enemies:
        attackables = enemy.attackable_heroes()
        if len(attackables) == 0:
            break
        for hero in attackables:
            if hero.hp - enemy.pw <= 0:
                board.board[hero.y][hero.x] = [board.board[hero.y][hero.x],
                                               'attackable']
                enemy.attack(hero.x, hero.y)
                attacked = True
            if attacked:
                return
    for enemy in enemies:
        attackables = enemy.attackable_heroes()
        if len(attackables) == 0:
            break
        hero = min(attackables, key=lambda x: x.hp)
        board.board[hero.y][hero.x] = [board.board[hero.y][hero.x],
                                       'attackable']
        enemy.attack(hero.x, hero.y)
        attacked = True
        if attacked:
            return
    choosen_enemy = choice(enemies)
    x, y = choice(choosen_enemy.reachable_cells())
    choosen_enemy.move(x, y)


def new_game(game_number):
    global board
    global heroes
    board = Board(19, 6)
    board.set_view(50, 330, 60)
    heroes = {}
    if game_number == 1:
        screen.blit(tut1, (0, 0))
        pygame.display.flip()
        i = 0
        time = clock.tick()
        while i < 5000:
            i += clock.tick()
            pygame.display.flip()
        screen.fill((0, 0, 0))
        screen.blit(tut2, (0, 0))
        pygame.display.flip()
        i = 0
        time = clock.tick()
        while i < 5000:
            i += clock.tick()
            pygame.display.flip()
        archer = Hero('archer', 5, 3)
        knight = Hero('knight', 7, 2)
        elven = Hero('elven', 6, 5)
        skeleton = Enemy('skeleton', 15, 0)
        orc = Enemy('orc', 17, 4)
    elif game_number == 2:
        draw()
        elf = Hero('elven', 0, 2)
        for y in range(6):
            qwe = Hero('knight', 4, y)
        for y in range(0, 6, 2):
            asd = Hero('archer', 2, y)
        for y in range(6):
            qwe = Enemy('orc', 14, y)
        for y in range(0, 6, 2):
            asd = Enemy('skeleton', 16, y)
    else:
        heroes = ['archer', 'knight', 'elven']
        enemies = ['skeleton', 'orc']
        for i in range(game_number):
            x, y = randint(0, 8), randint(0, 5)
            while board.board[y][x] != 0:
                x, y = randint(0, 8), randint(0, 5)
            hero = Hero(choice(heroes), x, y)
            x, y = randint(10, 18), randint(0, 5)
            while board.board[y][x] != 0:
                x, y = randint(10, 18), randint(0, 5)
            enemy = Enemy(choice(enemies), x, y)


clock = pygame.time.Clock()
code = 0
pygame.mouse.set_visible(False)
mouse_pos = [0, 0]
tut1 = pygame.image.load('media/screenshots/1.png')
tut2 = pygame.image.load('media/screenshots/2.png')
new_game(game_number)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos           
        if event.type == pygame.ACTIVEEVENT:
            if event.gain == 0:
                mouse_pos = -50, -50
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_click(event.pos)
    if victory:
        game_number += 1
        win_image = pygame.image.load('media/victory/1.jpg')
        i = 0
        screen.blit(win_image, (0, 0))
        pygame.display.flip()
        time = clock.tick()
        while i < 5:
            i += clock.tick() / 1000
        new_game(game_number)
        victory = False
    if lose:
        game_over = pygame.image.load('media/game_over/1.jpg')
        i = 0
        screen.blit(game_over, (0, 0))
        pygame.display.flip()
        time = clock.tick()
        while i < 5:
            i += clock.tick() / 1000
        new_game(game_number)
        lose = False
    draw()


pygame.quit()
