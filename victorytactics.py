import sys
import pygame
import traceback
from time import sleep
from random import *
from pygame import transform as rotate

start_text = ['Введите номер волны, с которой хотитите',
              'начать или Enter, если вы здесь впервые(<=54): ']

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

tut1 = pygame.image.load('media/screenshots/1.png')
tut2 = pygame.image.load('media/screenshots/2.png')
nl_image = pygame.image.load('media/other/next_level.png')
heart = pygame.image.load('media/other/health.png')

steps_sound = pygame.mixer.Sound('media/sounds/steps.wav')
slide_sound = pygame.mixer.Sound('media/sounds/slide.wav')
mega_victory_sound = pygame.mixer.Sound('media/sounds/mega_victory.wav')
victory_sound = pygame.mixer.Sound('media/sounds/victory.wav')
game_over_sound = pygame.mixer.Sound('media/sounds/game_over.wav')
click_sound = pygame.mixer.Sound('media/sounds/click.wav')
target1_sound = pygame.mixer.Sound('media/sounds/target1.wav')
target2_sound = pygame.mixer.Sound('media/sounds/target2.wav')

menu_music = pygame.mixer.Sound('media/sounds/menu.wav')
menu_music.set_volume(0.8)
pygame.mixer.music.load('media/sounds/main.wav')
pygame.mixer.music.set_volume(0.5)

buttons = pygame.sprite.Group()

home_button = pygame.sprite.Sprite(buttons)
home_button.image = pygame.image.load('media/buttons/home.png')
home_button.rect = home_button.image.get_rect()
home_button.rect.x, home_button.rect.y = 455, 320

restart_button = pygame.sprite.Sprite(buttons)
restart_button.image = pygame.image.load('media/buttons/restart.png')
restart_button.rect = restart_button.image.get_rect()
restart_button.rect.x, restart_button.rect.y = 600, 320

exit_button = pygame.sprite.Sprite(buttons)
exit_button.image = pygame.image.load('media/buttons/exit.png')
exit_button.rect = exit_button.image.get_rect()
exit_button.rect.x, exit_button.rect.y = 745, 320

HPnPWnRange = {'archer': [50, 35, 4], 'elven': [10, 80, 3],
               'knight': [100, 40, 1.5], 'orc': [85, 35, 1.5],
               'skeleton': [41, 35, 4]}
heroes = {}
victory, lose = [False] * 2


def terminate():
    pygame.quit()
    sys.exit()


def write():
    const_font = pygame.font.SysFont('gabriola', 52, bold=True)
    TEXT_y = 10
    for line in start_text:
        TEXT = const_font.render(line, 1, (255, 0, 0))
        TEXT_x = 640 - TEXT.get_width() // 2
        screen.blit(TEXT, (TEXT_x, TEXT_y))
        TEXT_y += 40


text_sprites = pygame.sprite.Group()


class Font(pygame.sprite.Sprite):
    def __init__(self, text, font, color, x, y):
        super().__init__(text_sprites)
        self.text = text
        self.image = font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def main_menu(from_pm=False):
    global game_number
    global start_screen_flag
    global new_game_flag
    if not from_pm:
        pygame.mixer.music.stop()
        menu_music.play(-1)
    start_bg = pygame.image.load('media/bg/start.jpg')
    screen.blit(start_bg, (0, 0))
    my_font = pygame.font.SysFont('gabriola', 72)
    lines = ['новая игра', 'продолжить игру', 'выбрать уровень', 'выйти']
    text_lines = []
    y = 180
    for line in lines:
        text_lines.append(Font(line, my_font, (230, 0, 0), 40, y))
        y += 72

    bg = pygame.Surface((int(text_lines[1].image.get_width()),
                         int(text_lines[1].image.get_height() / 1.2)))
    bg.set_alpha(64)
    bg.fill((255, 255, 255))

    running = True
    pos = (0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                for sprite in text_lines:
                    if sprite.rect.collidepoint(event.pos):
                        if sprite.text == 'новая игра':
                            new_game_flag = True
                            game_number = 1
                            file = open('media/level.txt', 'w')
                            file.write('1')
                            file.close()
                            running = False
                        elif sprite.text == 'продолжить игру':
                            game_number = int(open('media/level.txt').read())
                            new_game_flag = True
                            running = False
                        elif sprite.text == 'выбрать уровень':
                            start_screen_flag = True
                            running = False
                        elif sprite.text == 'выйти':
                            terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
        screen.blit(start_bg, (0, 0))
        text_sprites.draw(screen)
        for sprite in text_lines:
            if sprite.rect.collidepoint(pos):
                screen.blit(bg, (sprite.rect.x, sprite.rect.y + 7))
        pygame.display.flip()
    if not start_screen_flag:
        menu_music.stop()
        pygame.mixer.music.play(-1)


def start_screen():
    '''pygame.mixer.music.stop()
    menu_music.play(-1)'''
    start_bg = pygame.image.load('media/bg/start.jpg')
    screen.blit(start_bg, (0, 0))
    write()
    pygame.display.flip()
    running = True
    global game_number
    game_number = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                click_sound.play()
                try:
                    new = int(event.unicode)
                    game_number += str(new)
                    screen.blit(start_bg, (0, 0))
                    write()
                    const_font = pygame.font.SysFont('gabriola', 72, bold=True)
                    text = const_font.render(game_number, 1, (255, 0, 0))
                    text_x = 640 - text.get_width() // 2
                    screen.blit(text, (text_x, 400))
                    pygame.display.flip()
                except:
                    if event.unicode == '\r':
                        if game_number == '':
                            game_number = 1
                        else:
                            game_number = int(game_number)
                        if game_number > 54 and game_number != 228:
                            game_number = 54
                        elif game_number <= 0:
                            game_number = 1
                        file = open('media/level.txt', 'w')
                        file.write(str(game_number))
                        file.close()
                        running = False
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            game_number = game_number[:len(game_number) - 1]
            screen.blit(start_bg, (0, 0))
            write()
            const_font = pygame.font.SysFont('gabriola', 72, bold=True)
            text = const_font.render(game_number, 1, (255, 0, 0))
            text_x = 640 - text.get_width() // 2
            screen.blit(text, (text_x, 400))
            pygame.display.flip()
            sleep(0.2)
        if pygame.key.get_pressed()[pygame.K_DELETE]:
            game_number = ''
            screen.blit(start_bg, (0, 0))
            write()
            const_font = pygame.font.SysFont('gabriola', 72, bold=True)
            text = const_font.render(game_number, 1, (255, 0, 0))
            text_x = 640 - text.get_width() // 2
            screen.blit(text, (text_x, 400))
            pygame.display.flip()
            sleep(0.2)
    menu_music.stop()
    pygame.mixer.music.play(-1)
    new_game(game_number)


def tutorial():
    screen.blit(tut1, (0, 0))
    pygame.display.flip()
    running = True
    pygame.event.wait()
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
            running = False
            break
    screen.blit(tut2, (0, 0))
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
            return


def next_level():
    x = -1280
    screen.blit(nl_image, (x, 0))
    clock.tick()
    slide_sound.play()
    while x < 0:
        time = clock.tick() / 1000
        x += time * 2000
        screen.blit(nl_image, (int(x), 0))
        pygame.display.flip()
    x = 0
    screen.blit(nl_image, (int(x), 0))
    pygame.display.flip()
    sleep(3)


def pause_menu():
    pygame.mixer.music.stop()
    menu_music.play(-1)
    screen.blit(white_rect, (0, 0))
    const_font = pygame.font.SysFont('gabriola', 100, bold=True)
    my_font = pygame.font.SysFont('gabriola', 50, bold=True)
    inter = str(game_number) + '  уровень'
    text = const_font.render('Pause Menu', 1, (139, 0, 0))
    text2 = my_font.render(inter, 1, (139, 0, 0))
    text_x = 640 - text.get_width() // 2
    text2_x = 640 - text2.get_width() // 2
    screen.blit(text2, (text2_x, 30))
    screen.blit(text, (text_x, 100))
    buttons.draw(screen)
    pygame.display.flip()
    running = True
    global main_menu_flag
    global new_game_flag
    while running:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if home_button.rect.collidepoint(event.pos):
                main_menu_flag = True
                running = False
            elif restart_button.rect.collidepoint(event.pos):
                new_game_flag = True
                running = False
            elif exit_button.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.unicode == '\x1b':
                running = False
    if not main_menu_flag:
        menu_music.stop()
        pygame.mixer.music.play(-1)


def draw(animated=None):
    bg = pygame.image.load('media/bg/bg1.jpg')
    screen.blit(bg, (0, 0))
    board.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    for key, value in heroes.items():
        if key == animated:
            screen.blit(key.anim, value)
        else:
            screen.blit(key.stand, value)
            x, y = value
            screen.blit(health_bg, (x - 1, y - 8))
            pygame.draw.rect(screen, pygame.Color('brown'),
                             (x - 2, y - 9, 52, 7), 1)
            pygame.draw.rect(screen, (255, 0, 0),
                             (x - 1, y - 8, int(50 * key.hp / key.full_hp), 5))
            screen.blit(heart, (x - 6, y - 15))
    pygame.display.flip()


running = True

blue_rect = pygame.Surface((60, 60))  # the size of your rect
blue_rect.set_alpha(50)                # alpha level
blue_rect.fill(pygame.Color('blue'))           # this fills the entire surface
red_rect = pygame.Surface((60, 60))
red_rect.set_alpha(50)
red_rect.fill(pygame.Color('red'))
health_bg = pygame.Surface((50, 5))
health_bg.set_alpha(60)
health_bg.fill((255, 0, 0))
white_rect = pygame.Surface((1280, 720))
white_rect.set_alpha(200)
white_rect.fill((222, 184, 135))

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
        self.name = char
        self.full_hp = HPnPWnRange[char][0]
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
        self.hurt_sound = pygame.mixer.Sound('media/sounds/{}/hurt.wav'.
                                             format(char))
        self.attack_sound = pygame.mixer.Sound('media/sounds/{}/attack.wav'.
                                               format(char))

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
            played = False
            if board.board[y][x][-1] == 'attackable':
                i = 0
                board.clear()
                time = clock.tick(30)
                if self.name != 'archer' and self.name != 'skeleton':
                    self.attack_sound.play()
                while i < len(self.attack_anim):
                    time = clock.tick(30) / 1000
                    i = (i + time * 10)
                    if int(i % 12) == 8 and not played and (
                        self.name == 'archer' or self.name == 'skeleton'
                    ):
                        self.attack_sound.play()
                        played = True
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
        time = clock.tick(30)
        self.hurt_sound.play()
        while i <= 5:
            time = clock.tick(30) / 1000
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
        time = clock.tick(30)
        board.clear()
        steps_sound.play()
        while v_x != 0 or v_y != 0:
            pos = heroes[self]
            d_x, d_y = x1 - int(pos[0]), y1 - int(pos[1])
            if abs(d_x) <= 5:
                d_x = 0
                pos[0] = x1
                v_x = 0
            if abs(d_y) <= 5:
                d_y = 0
                pos[1] = y1
                v_y = 0
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
            time = clock.tick(30) / 1000
            i = (i + time * 10) % 9
            if v_x < 0:
                self.anim = rotate.flip(self.walk_anim[int(i)], 1, 0)
            else:
                self.anim = self.walk_anim[int(i)]
            pos[0] += v_x * time
            pos[1] += v_y * time
            heroes[self] = [int(pos[0]), int(pos[1])]
            draw(self)
        steps_sound.stop()
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
                                           format(char, str(i))),
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
            continue
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
            continue
        hero = min(attackables, key=lambda x: x.hp)
        board.board[hero.y][hero.x] = [board.board[hero.y][hero.x],
                                       'attackable']
        enemy.attack(hero.x, hero.y)
        attacked = True
        if attacked:
            return
    choosen_enemy = choice(enemies)
    x0, y0 = choosen_enemy.x, choosen_enemy.y
    variants = []
    for i in board.board:
        for object in i:
            if type(object) == Hero:
                variants.append((object,
                                 abs(object.x - x0) + abs(object.y - y0)))
    choosen_hero = min(variants, key=lambda x: x[1])[0]
    x1, y1 = choosen_hero.x, choosen_hero.y
    cells = choosen_enemy.reachable_cells()
    while len(cells) < 1:
        choosen_enemy = choice(enemies)
        x0, y0 = choosen_enemy.x, choosen_enemy.y
        variants = []
        for i in board.board:
            for object in i:
                if type(object) == Hero:
                    variants.append((object,
                                     abs(object.x - x0) + abs(object.y - y0)))
        choosen_hero = min(variants, key=lambda x: x[1])[0]
        x1, y1 = choosen_hero.x, choosen_hero.y
        cells = choosen_enemy.reachable_cells()
    choosen_cell = min([i for i in cells], key=lambda x: abs(x1 - x[0]) +
                       abs(y1 - x[1]))
    x, y = choosen_cell
    choosen_enemy.move(x, y)


def new_game(game_number):
    global board
    global heroes
    global code
    code = 0
    board = Board(19, 6)
    board.set_view(50, 330, 60)
    heroes = {}
    if game_number == 1:
        tutorial()
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
    elif game_number == 228:
        elf = Hero('elven', 0, 2)
        asd = Enemy('skeleton', 1, 3)
    elif game_number == 229:
        asd = Hero('elven', 0, 2)
    elif game_number == 1318:
        a = pygame.image.load('media/easter.jpg')
        a = pygame.transform.scale(a, (1280, 720))
        screen.blit(a, (0, 0))
        pygame.display.flip()
        sleep(3)
    else:
        heroes_names = ['archer', 'knight', 'elven']
        enemies = ['skeleton', 'orc']
        for i in range(game_number):
            x, y = randint(0, 8), randint(0, 5)
            while board.board[y][x] != 0:
                x, y = randint(0, 8), randint(0, 5)
            hero = Hero(choice(heroes_names), x, y)
            x, y = randint(10, 18), randint(0, 5)
            while board.board[y][x] != 0:
                x, y = randint(10, 18), randint(0, 5)
            enemy = Enemy(choice(enemies), x, y)
    draw()


pygame.display.set_caption('Victory Tactics')
pygame.display.set_icon(pygame.image.load('media/game_icon.ico'))
iter_count = 0
clock = pygame.time.Clock()
code = 0
game_number = None
start_screen_flag = False
new_game_flag = False
main_menu_flag = False
main_menu()

while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        click_sound.play()
        if event.button == 1:
            board.get_click(event.pos)
    elif event.type == pygame.KEYDOWN:
        if event.unicode == '\x1b':
            pause_menu()
    if main_menu_flag:
        main_menu_flag = False
        main_menu(True)
    if start_screen_flag:
        start_screen_flag = False
        start_screen()
    if new_game_flag:
        new_game_flag = False
        new_game(game_number)
    if victory:
        pygame.mixer.music.stop()
        game_number += 1
        file = open('media/level.txt', 'w')
        file.write(str(game_number))
        file.close()
        alpha_lvl = 0
        win_image = pygame.image.load('media/victory/1.jpg')
        win_image.set_alpha(alpha_lvl)
        screen.blit(win_image, (0, 0))
        pygame.display.flip()
        time = clock.tick(30)
        victory_sound.play()
        while alpha_lvl < 30:
            alpha_lvl += clock.tick(30) / 100
            win_image.set_alpha(int(alpha_lvl))
            screen.blit(win_image, (0, 0))
            pygame.display.flip()
        draw()
        next_level()
        new_game(game_number)
        victory = False
        pygame.mixer.music.play(-1)
    elif lose:
        pygame.mixer.music.stop()
        l1 = pygame.image.load('media/game_over/01.jpg')
        l2 = pygame.image.load('media/game_over/02.jpg')
        l3 = pygame.image.load('media/game_over/03.jpg')
        l4 = pygame.image.load('media/game_over/04.jpg')
        l_main = pygame.image.load('media/game_over/1.jpg')
        game_over = [l1, l2, l3, l4]
        game_over2 = [(l1, (0, 0)), (l4, (640, 360)),
                      (l2, (640, 0)), (l3, (0, 360))]
        game_over_sound.play()
        for l, pos in game_over2:
            alpha_lvl = 0
            time = clock.tick(30)
            while alpha_lvl < 200:
                alpha_lvl += clock.tick(30) / 1.5
                l.set_alpha(int(alpha_lvl))
                draw()
                screen.blit(l, pos)
                pygame.display.flip()
        draw()

        pos1 = [-640, -360]
        pos2 = [1280, -360]
        pos3 = [-640, 720]
        pos4 = [1280, 720]
        time = clock.tick(30)
        while pos1[0] < 0:
            time = clock.tick(30) / 1000
            pos1[0] += time * 320
            pos1[1] += time * 180
            pos2[0] += time * -320
            pos2[1] += time * 180
            pos3[0] += time * 320
            pos3[1] += time * -180
            pos4[0] += time * -320
            pos4[1] += time * -180
            screen.blit(l1, pos1)
            screen.blit(l2, pos2)
            screen.blit(l3, pos3)
            screen.blit(l4, pos4)
            pygame.display.flip()
        screen.blit(l_main, (0, 0))
        pygame.display.flip()
        i = clock.tick(30)
        i = 0
        while i < 3:
            i += clock.tick(30) / 1000
        new_game(game_number)
        lose = False
        pygame.mixer.music.play(-1)
    draw()

pygame.quit()
