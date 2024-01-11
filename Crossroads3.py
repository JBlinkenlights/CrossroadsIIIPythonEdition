import pygame
import sys
import os
import random
from pygame.locals import *
from pygame.colordict import THECOLORS

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

pic_dir = 'assets/img/'
snd_dir = 'assets/sound/'


def image(filename):
    return pygame.image.load(pic_dir + filename)


def color_img_list(lst, clr):
    for img in lst:
        arr = pygame.surfarray.pixels3d(img)
        arr[:, :, 0] = clr[0]
        arr[:, :, 1] = clr[1]
        arr[:, :, 2] = clr[2]
    return lst


def sound_effect(filename):
    return pygame.mixer.Sound(snd_dir + filename)


def delta_to_direction(dx, dy, last_direction):
    if dx == dy == 0:
        is_moving = False
        direction = last_direction
    else:
        is_moving = True
        if dx > 0 and dy == 0:
            direction = 'right'
        elif dx < 0 and dy == 0:
            direction = 'left'
        elif dx == 0 and dy < 0:
            direction = 'up'
        elif dx == 0 and dy > 0:
            direction = 'down'
        else:
            direction = last_direction
    return is_moving, direction


def direction_to_delta(is_moving, direction):
    dx = dy = 0
    if not is_moving:
        dx = dy = 0
    else:
        if direction == 'right':
            dx = 1
            dy = 0
        elif direction == 'left':
            dx = -1
            dy = 0
        elif direction == 'up':
            dx = 0
            dy = -1
        elif direction == 'down':
            dx = 0
            dy = 1
        else:
            dx = dy = 0
    return dx, dy


def get_position_in_direction(direction, dist):
    if direction == 'left':
        rel_x = -dist
        rel_y = 0
    elif direction == 'right':
        rel_x = dist
        rel_y = 0
    elif direction == 'up':
        rel_x = 0
        rel_y = -dist
    elif direction == 'down':
        rel_x = 0
        rel_y = dist
    else:
        rel_x = rel_y = 0
    return rel_x, rel_y


def is_opposite_direction(we, they):
    opposite_directions = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }
    opst_dr = opposite_directions[we]
    if opst_dr != they:
        return False
    return True


def get_opposite_direction(dr):
    opposite_directions = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }
    opst_dr = opposite_directions[dr]
    return opst_dr


def get_direction(x1, y1, x2, y2):  # this is a bit oversimplified, but I think I can use it.
    if x2 < x1:
        dr_x = 'left'
    else:
        dr_x = 'right'
    if y2 < y1:
        dr_y = 'up'
    else:
        dr_y = 'down'
    return dr_x, dr_y


def read_levels_file(filename):
    assert os.path.exists(filename), 'Cannot find level file.'
    map_file = open(filename, 'r')
    content = map_file.readlines() + ['\r\n']
    map_file.close()

    levels = []
    level_names = []
    level_num = 0
    map_text_lines = []
    map_objects = []

    for line_number in range(len(content)):

        line = content[line_number].rstrip('\r\n')

        if ';' in line:  # comments in the file
            line = line[:line.find(';')]
        elif '$' in line:  # denotes title of level
            level_names.append(line.split('$', 1)[1])
        elif line != '':  # this line is not empty, it is part of a level map
            map_text_lines.append(line)
        elif line == '' and len(map_text_lines) > 0:
            map_width = -1
            max_width = game_width
            for i in range(len(map_text_lines)):
                if len(map_text_lines[i]) > map_width:
                    map_width = len(map_text_lines[i])
            assert map_width <= max_width, 'One of your levels is longer than %d characters. ' \
                                           'Please fix.' % game_width
            for i in range(len(map_text_lines)):
                map_text_lines[i] += '.' * (max_width - len(map_text_lines[i]))

            for x in range(len(map_text_lines[0])):
                map_objects.append([])
            for y in range(len(map_text_lines)):
                for x in range(map_width):
                    map_objects[x].append(map_text_lines[y][x])

            wall_map = []
            for x in range(max_width):
                for y in range(len(map_objects[x])):
                    if map_objects[x][y] in '.':
                        pass
                    elif map_objects[x][y] in '0':  # this is a wall
                        wall_map.append((x, y))

            level = {
                'name': level_names[level_num],
                'map': wall_map
            }

            levels.append(level)

            map_text_lines = []
            map_objects = []
            level_num += 1

    return levels


def render_level(lvl):
    for wall in lvl['map']:
        wall_x = wall[0] * img_side
        wall_y = wall[1] * img_side
        w = Wall(wall_x, wall_y)


def place_sprites(cls, num):
    for x in range(0, num):
        to_place = cls(0, 0)
        good_pos = False
        while not good_pos:
            x = random.randint(0, window_width)
            y = random.randint(0, window_height)
            to_place.rect.x, to_place.rect.y = x, y
            for gp in game_groups:
                for other_sprites in gp.sprites():
                    if to_place.rect.colliderect(other_sprites.rect) or other_sprites != to_place:
                        continue
            good_pos = True


def render_text(font, text, x, y, clr, surf):
    text = font.render(text, True, clr)
    rect = text.get_rect()
    rect.center = (x, y)
    surf.blit(text, rect)


def increment_list(val, lst):
    new_val = val
    new_val += 1
    if new_val > len(lst):
        new_val = 0
    return new_val


def terminate():
    pygame.quit()
    sys.exit()


# fonts
bahn = pygame.font.SysFont('Bahnschrift', 90)
bahn_small = pygame.font.SysFont('Bahnschrift', 16)
# colors
black = THECOLORS['black']
white = THECOLORS['white']
grey = THECOLORS['grey43']
blue = THECOLORS['blue']
red = THECOLORS['red2']
yellow = THECOLORS['yellow3']
dark_green = THECOLORS['darkolivegreen']
purple = THECOLORS['purple']
# image lists
player_1_imgs = [image('Player1.png'), image('Player2.png')]
player_2_imgs = [image('Player1.png'), image('Player2.png')]
player_lsts = [player_1_imgs, player_2_imgs]

lemonshark_imgs = [image('LemonShark1.png'), image('LemonShark2.png')]
skullface_imgs = [image('SkullFace1.png'), image('SkullFace2.png')]
catfish_imgs = [image('Catfish1.png')]
rubberhead_imgs = [image('rubberhead1.png'), image('rubberhead2.png')]
laser_imgs = [image('Laser2.png')]
bomb_imgs = [pygame.image.load('assets/img/Explosion' + str(x) + '.png') for x in range(0, 8)]
spar_imgs = [pygame.image.load('assets/img/spar' + str(x + 1) + '.png') for x in range(0, 6)]
wall_imgs = [image('Wall.png')]
# sound
gun_sfx = sound_effect('retro_laser_01.ogg')
bounce_laser_sfx = sound_effect('laser_bounce_1.ogg')
bomb_arm_sfx = sound_effect('weapswitch.ogg')
bomb_beep_sfx = sound_effect('bombBeep.ogg')
bomb_sfx = sound_effect('explosion.ogg')
die_lemonshark_sfx = sound_effect('mutantdie.ogg')
die_skullface_sfx = sound_effect('skullDie.ogg')
fish_run_sfx = sound_effect('fishRun.wav')
die_rubberhead_sfx = sound_effect('bug_04.ogg')
spar_collect_sfx = sound_effect('spar_collect.ogg')
menu_scroll_sfx = sound_effect('menu_scroll.ogg')
menu_select_sfx = sound_effect('menu_select.ogg')
game_exit_sfx = sound_effect('game_exit.ogg')


# window properties
img_side = 28
game_width = 54
game_height = 26
window_width = img_side * game_width
window_height = img_side * game_height
half_win_w = window_width / 2
half_win_h = window_height / 2
display_surface = pygame.display.set_mode((window_width, window_height))
display_rect = display_surface.get_rect()
screen = pygame.display
screen.set_caption('Crossroads')

target_fps = 30
game_clock = pygame.time.Clock()

pygame.joystick.init()
all_ctls = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for x in range(0, len(all_ctls)):
    all_ctls[x].init()
if not all_ctls:
    raise IndexError('Please plug in a controller.')

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
scenery_group = pygame.sprite.Group()
goal_group = pygame.sprite.Group()
game_groups = [player_group, enemy_group, weapon_group, scenery_group, goal_group]


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, gp, health, img_list, clr=None):
        super(Sprite, self).__init__(gp)

        self.kind = self.__class__.__name__

        self.health = health
        if self.health == -1:
            self.can_kill = False
        else:
            self.can_kill = True
        self.vulnerable_to = ['None']
        self.dying = False

        if clr is not None:
            self.images_list = color_img_list(img_list, clr)
        else:
            self.images_list = img_list
        self.ani_index = 0
        self.image = self.images_list[self.ani_index]
        self.image_rotatable = True
        self.ani_timer = 0

        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_moving = False
        self.direction = 'right'
        self.speed = 4

    def can_be_killed_by(self, queried_kind):
        for deadly_kind in self.vulnerable_to:
            if queried_kind == deadly_kind:
                return True
        return False

    def check_for_damage(self, sprt):
        kind = sprt.kind
        if self.can_be_killed_by(kind):
            if kind == 'Bomb':
                self.health -= 10
            else:
                self.health -= 1

    def get_health(self, old_health):
        if self.can_kill and old_health <= 0:
            health = 0
            if self.alive():
                self.dying = True
                self.die()
        else:
            health = old_health
        return health

    def die(self):
        self.kill()

    def get_ctl(self):
        is_moving = False
        direction = 'right'
        return is_moving, direction

    def move(self, is_moving, direction):
        dx, dy = direction_to_delta(is_moving, direction)
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
        self.on_move()

    def move_single_axis(self, dx, dy):
        self.rect.x += (dx * self.speed)
        self.rect.y += (dy * self.speed)
        for gp in game_groups:
            for s in gp.sprites():
                if self.rect.colliderect(s.rect) and not s == self:
                    collided_self = None
                    collided_other = None
                    if not s.kind == ('Laser' or 'Bomb'):
                        rect_snap = True
                    else:
                        rect_snap = False

                    if dx > 0:  # Moving right; Hit the left side of the wall
                        if rect_snap:
                            self.rect.right = s.rect.left
                        collided_self = 'right'
                        collided_other = 'left'
                    if dx < 0:  # Moving left; Hit the right side of the wall
                        if rect_snap:
                            self.rect.left = s.rect.right
                        collided_self = 'left'
                        collided_other = 'right'
                    if dy > 0:  # Moving down; Hit the top side of the wall
                        if rect_snap:
                            self.rect.bottom = s.rect.top
                        collided_self = 'down'
                        collided_other = 'up'
                    if dy < 0:  # Moving up; Hit the bottom side of the wall
                        if rect_snap:
                            self.rect.top = s.rect.bottom
                        collided_self = 'up'
                        collided_other = 'down'

                    if collided_self is not None:
                        self.on_collide(s, collided_self)
                    if collided_other is not None:
                        s.on_collide(self, collided_other)

    def on_move(self):
        pass

    def on_collide(self, sprt, drct):
        self.check_for_damage(sprt)

    def get_image_index(self, is_moving, current_index):
        new_index = current_index
        if is_moving and self.ani_timer == 0:
            new_index += 1
            self.ani_timer = 10
        if new_index > len(self.images_list) - 1:
            new_index = 0
        if self.ani_timer > 0:
            self.ani_timer -= 1
        return new_index

    def rotate_sprite(self, surf, rect, direction):
        if self.image_rotatable:
            d_map = {
                'right': 0,
                'up': 90,
                'left': 180,
                'down': 270
            }
            angle = d_map[direction]
            rot_surf = pygame.transform.rotate(surf, angle)
            rot_rect = rot_surf.get_rect(center=rect.center)
        else:
            rot_surf = surf
            rot_rect = rect
        return rot_surf, rot_rect

    def on_update(self, is_moving, direction):
        pass

    def update(self, *args):
        # get motion variables
        self.is_moving, self.direction = self.get_ctl()

        # set image and rotation
        self.ani_index = self.get_image_index(self.is_moving, self.ani_index)
        self.image = self.images_list[self.ani_index]
        self.image, self.rect = self.rotate_sprite(self.image, self.rect, self.direction)

        # handle health and subclass-specific commands
        self.health = self.get_health(self.health)
        self.on_update(self.is_moving, self.direction)

        # move the sprite
        self.move(self.is_moving, self.direction)


class Player(Sprite):
    def __init__(self, x, y, ctl_num, clr):
        super(Player, self).__init__(x, y, player_group, 100, player_lsts[ctl_num], clr)
        self.ctl = all_ctls[ctl_num]
        self.clr = clr
        self.vulnerable_to = ['Lemonshark', 'Laser', 'Bomb', 'Skullface', 'Catfish', 'Rubberhead']
        self.trigger_timer = 0
        self.bomb_timer = 0
        self.speed = 6

    def check_for_damage(self, sprt):
        kind = sprt.kind
        if self.can_be_killed_by(kind):
            if kind == 'Bomb':
                self.health -= 10
            elif kind == 'Laser' and sprt.shooter == self and sprt.count_to_deadly > 0:
                pass
            else:
                self.health -= 1

    def get_ctl(self):
        hat = self.ctl.get_hat(0)
        is_moving, direction = delta_to_direction(hat[0], -hat[1], self.direction)
        return is_moving, direction

    def get_trigger(self, mv, dr):
        laser_on = self.ctl.get_button(1)
        bomb_on = self.ctl.get_button(3)
        if laser_on and self.trigger_timer <= 0:
            spawn_x, spawn_y = get_position_in_direction(dr, 30)
            gun_sfx.play()
            l = Laser(self.rect.x + spawn_x, self.rect.y + spawn_y, dr, self)
            self.trigger_timer = 8
        if bomb_on and self.bomb_timer <= 0:
            spawn_x, spawn_y = get_position_in_direction(dr, 60)
            bomb_arm_sfx.play()
            b = Bomb(self.rect.center[0] + spawn_x, self.rect.center[1] + spawn_y, dr)
            self.bomb_timer = 100
        if self.trigger_timer > 0:
            self.trigger_timer -= 1
        if self.bomb_timer > 0:
            self.bomb_timer -= 1

    def on_update(self, is_moving, direction):
        self.get_trigger(is_moving, direction)


class Lemonshark(Sprite):
    def __init__(self, x, y):
        super(Lemonshark, self).__init__(x, y, enemy_group, 1, lemonshark_imgs, yellow)
        self.vulnerable_to = ['Laser', 'Bomb']
        self.speed = 4

    def get_ctl(self):
        is_moving = True
        if not random.randint(0, 10):
            dr_list = ['right', 'up', 'left', 'down']
            direction = random.choice(dr_list)
        else:
            direction = self.direction
        return is_moving, direction

    def die(self):
        die_lemonshark_sfx.play()
        self.kill()


class Skullface(Sprite):
    def __init__(self, x, y):
        super(Skullface, self).__init__(x, y, enemy_group, 9, skullface_imgs, white)
        self.last_moving = True
        self.speed = 2
        self.vulnerable_to = ['Laser', 'Bomb']

    def get_ctl(self):
        if not random.randint(0, 10):
            is_moving = False
        else:
            is_moving = True
        self.last_moving = is_moving
        if not random.randint(0, 20):
            dr_list = ['right', 'up', 'left', 'down']
            direction = random.choice(dr_list)
        else:
            direction = self.direction
        return is_moving, direction

    def die(self):
        die_skullface_sfx.play()
        self.kill()


class Catfish(Sprite):
    def __init__(self, x, y):
        super(Catfish, self).__init__(x, y, enemy_group, 5, catfish_imgs, dark_green)
        self.speed = 25
        self.direction = 'right'

        self.runtime = 100
        self.panictime = 0
        alert_range = 40
        self.alert_rect = pygame.Rect(self.rect.x - alert_range, self.rect.y - alert_range, self.rect.width + alert_range, self.rect.height + alert_range)
        self.alert_rect.center = self.rect.center

        self.flee_dr = 'left'
        self.flee_dr_counter = 10

        self.vulnerable_to = ['Laser', 'Bomb']

    def get_ctl(self):
        is_moving = True
        direction = self.direction
        return is_moving, direction

    def get_image_index(self, is_moving, current_index):
        return current_index

    def on_update(self, is_moving, direction):
        if self.panictime > 0:
            self.panictime -= 1
            self.speed = 25
        else:
            self.speed = 0.5
        self.alert_rect.center = self.rect.center

    def get_escape_direction(self, no_go_dr):
        to_flee = no_go_dr
        while to_flee == no_go_dr:
            dr_lst = ['left', 'up', 'right', 'down']
            to_flee = random.choice(dr_lst)
        return to_flee

    def on_collide(self, sprt, direction):
        kind = sprt.kind
        self.check_for_damage(sprt)
        self.direction = self.get_escape_direction(direction)
        if self.can_be_killed_by(kind) or kind == 'Player':
            self.panictime = self.runtime
            fish_run_sfx.play()
        if self.panictime > 0 and kind == 'Catfish' and self.alert_rect.colliderect(sprt.rect):
            sprt.panictime = self.runtime


class Rubberhead(Sprite):
    def __init__(self, x, y):
        super(Rubberhead, self).__init__(x, y, enemy_group, 1, rubberhead_imgs, purple)
        self.current_dr = self.direction
        self.vulnerable_to = ['Laser', 'Bomb']
        self.target = random.choice(player_group.sprites())

    def get_ctl(self):
        is_moving = True
        if not random.randint(0, 20):
            if not random.randint(0, 4):
                dr_list = ['right', 'up', 'left', 'down']
            else:
                dr_x, dr_y = 0, 0
                if self.target is not None:
                    dr_x, dr_y = get_direction(self.rect.x, self.rect.y, self.target.rect.x, self.target.rect.y)
                dr_list = [dr_x, dr_y]
            direction = random.choice(dr_list)
        else:
            direction = self.direction
        return is_moving, direction

    def on_update(self, is_moving, direction):
        self.current_dr = direction
        if self.target not in player_group.sprites():
            try:
                self.target = random.choice(player_group.sprites())
            except IndexError:
                self.target = None

    def on_collide(self, sprt, drct):
        if sprt.kind == 'Laser':
            if is_opposite_direction(drct, self.direction):
                self.check_for_damage(sprt)
                sprt.health -= 1
            elif sprt.course_lock_timer == 0:
                sprt.set_course = get_opposite_direction(sprt.set_course)
                bounce_laser_sfx.play()
                sprt.course_lock_timer = 4
        else:
            self.check_for_damage(sprt)

    def die(self):
        die_rubberhead_sfx.play()
        self.kill()


class Laser(Sprite):
    def __init__(self, x, y, dr, shooter):
        super(Laser, self).__init__(x, y, weapon_group, 1, laser_imgs)
        self.course_lock_timer = 0
        self.set_course = dr
        self.speed = 15
        self.shooter = shooter
        self.count_to_deadly = 10
        self.vulnerable_to = ['Player', 'Lemonshark', 'Laser', 'Wall', 'Bomb', 'Skullface', 'Catfish', 'Spar']

    def get_ctl(self):
        is_moving = True
        direction = self.set_course
        return is_moving, direction

    def on_update(self, is_moving, direction):
        if self.count_to_deadly > 0:
            self.count_to_deadly -= 1
        if self.course_lock_timer > 0:
            self.course_lock_timer -= 1

    def on_collide(self, sprt, drct):
        if sprt == self.shooter and self.count_to_deadly > 0:
            pass
        else:
            self.check_for_damage(sprt)

    def die(self):
        self.kill()


class Bomb(Sprite):
    def __init__(self, x, y, dr):
        super(Bomb, self).__init__(x, y, weapon_group, 1, bomb_imgs)
        self.speed = 30
        self.mv = True
        self.dr = dr
        self.image_rotatable = False
        self.vulnerable_to = ['Lemonshark', 'Laser', 'Player', 'Skullface', 'Catfish', 'Rubberhead', 'Spar']
        self.lock1 = False
        self.counter = 0
        self.time_to_live = 30

    def on_move(self):
        if not self.dying:
            pygame.draw.arc(display_surface, red, self.rect, 0, self.time_to_live / 3, 6)

    def get_image_index(self, is_moving, current_index):
        return current_index

    def get_ctl(self):
        is_moving = self.mv
        direction = self.dr
        return is_moving, direction

    def on_update(self, is_moving, direction):
        if self.speed > 0:
            self.speed -= 1
        else:
            self.mv = False
        if self.time_to_live > 0:
            self.time_to_live -= 1
            bomb_beep_sfx.stop()
            bomb_beep_sfx.play()
        else:
            self.die()

    def on_collide(self, sprt, drct):
        self.check_for_damage(sprt)
        self.speed = 0

    def die(self):
        bomb_beep_sfx.stop()
        self.speed = 0
        self.ani_index = self.counter + 1
        if not self.lock1:
            self.rect.x -= 40
            self.rect.y -= 60
            self.lock1 = True
        if self.counter == 0:
            bomb_sfx.play()
        if self.counter == 7:
            self.kill()
        self.counter += 1


class Wall(Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__(x, y, scenery_group, -1, wall_imgs, grey)


class Spar(Sprite):
    def __init__(self, x, y):
        super(Spar, self).__init__(x, y, goal_group, 1, spar_imgs, white)
        self.vulnerable_to = ['Player']

    def get_ctl(self):
        is_moving = False
        for s in scenery_group.sprites():
            if self.rect.colliderect(s.rect):
                is_moving = True
        if not display_rect.contains(self.rect):
            is_moving = True
        directions = ['right', 'up']
        direction = random.choice(directions)
        return is_moving, direction

    def get_image_index(self, is_moving, current_index):
        new_index = current_index + 1
        if new_index > len(self.images_list) - 1:
            new_index = 0
        return new_index

    def die(self):
        spar_collect_sfx.play()
        self.kill()


class MenuItem:
    def __init__(self, *args):
        is_list = True
        try:
            for x in args[0]:
                pass
        except:
            is_list = False
        if not is_list:
            self.options = []
            for opt in args:
                self.options.append(opt)
        else:
            self.options = args[0]
        self.index = 0
        self.value = self.options[self.index]
        self.color_norm = white
        self.color_selected = red
        self.color = white

    def selected(self, is_selected):
        if is_selected:
            self.color = self.color_selected
        else:
            self.color = self.color_norm

    def increment(self):
        self.index += 1
        if self.index > len(self.options) - 1:
            self.index = 0
        self.value = self.options[self.index]


levels_list = read_levels_file('assets/levels.txt')
enumerated_levels = []
for n in range(0, len(levels_list)):
    enumerated_levels.append(n)
level_index = MenuItem(enumerated_levels)

# menu settable params
two_players = MenuItem(False, True)
music = MenuItem(True, False)
start_game = MenuItem(False, True)
end_game = MenuItem(False, True)

menu = True
new_game = False
run_game = False
victory_music = False

menu_index = 0
menu_items = [two_players, music, level_index, start_game, end_game]
btn_timer = 0
btn_down = False
pygame.mixer.music.set_volume(0.4)
playing = False
level_object = None

while True:
    if menu:
        if not playing:
            pygame.mixer.music.load('assets/sound/retro_music/title.wav')
            pygame.mixer.music.play(-1)
            playing = True
            victory_music = False
        display_surface.fill(black)
        select_up = select_down = select_enter = False
        btn_down = False
        if btn_timer > 0:
            btn_timer -= 1

        ctl = all_ctls[0]
        if btn_timer <= 0:
            select_up = ctl.get_hat(0)[1] > 0
            select_down = ctl.get_hat(0)[1] < 0
            select_enter = ctl.get_button(0)

        if select_up or select_down or select_enter:
            btn_timer = 10

        if select_up:
            menu_index -= 1
            menu_scroll_sfx.play()
        elif select_down:
            menu_index += 1
            menu_scroll_sfx.play()
        elif select_enter:
            menu_items[menu_index].increment()
            menu_select_sfx.play()

        if menu_index > len(menu_items) - 1:
            menu_index = 0

        for item in menu_items:
            if item == menu_items[menu_index]:
                item.selected(True)
            else:
                item.selected(False)

        level_object = levels_list[level_index.value]

        if start_game.value:
            pygame.mixer.music.stop()
            playing = False
            for x in range(0, 40):
                display_surface.fill(black)
                render_text(bahn, 'Crossroads III', half_win_w, half_win_h - (half_win_h / 2) - (x * 10), white,
                            display_surface)
                screen.flip()
                game_clock.tick(target_fps)
            menu = False
            new_game = True
        if end_game.value:
            terminate()

        render_text(bahn, 'Crossroads III', half_win_w, half_win_h - (half_win_h / 2), white, display_surface)
        render_text(bahn_small, 'After All These Years', half_win_w, half_win_h - (half_win_h / 2) + 70, white, display_surface)
        render_text(bahn_small, 'Two Player Mode: ' + str(two_players.value), half_win_w, half_win_h,
                    two_players.color, display_surface)
        render_text(bahn_small, 'Music: ' + str(music.value), half_win_w, half_win_h + 30, music.color,
                    display_surface)
        render_text(bahn_small, 'Level: ' + str(level_object['name']), half_win_w, half_win_h + 60, level_index.color,
                    display_surface)
        render_text(bahn_small, 'Start Game', half_win_w, half_win_h + 90, start_game.color, display_surface)
        render_text(bahn_small, 'Quit', half_win_w, half_win_h + 120, end_game.color, display_surface)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

    if new_game:
        for gp in game_groups:
            gp.empty()
        player_red = Player(300, 350, 0, red)
        if two_players.value:
            player_blue = Player(400, 350, 1, blue)

        render_level(level_object)

        place_sprites(Lemonshark, 20)
        place_sprites(Skullface, 20)
        place_sprites(Catfish, 30)
        place_sprites(Rubberhead, 10)
        place_sprites(Spar, 30)

        if music.value and not playing:
            playlist = ['assets/sound/retro_music/level1.wav', 'assets/sound/retro_music/level2.wav',
                        'assets/sound/retro_music/level3.wav']
            pygame.mixer.music.load(random.choice(playlist))
            pygame.mixer.music.play(-1)
            playing = True
            victory_music = False

        new_game = False
        run_game = True

    if run_game:
        display_surface.fill(black)

        # screen wraparound code
        for group in game_groups:
            for sprite in group.sprites():
                screen_wrap_cushion = 5
                wrap_left = wrap_up = -screen_wrap_cushion
                wrap_right = window_width + screen_wrap_cushion
                wrap_down = window_height + screen_wrap_cushion
                if sprite.rect.x > wrap_right:
                    sprite.rect.x = wrap_left
                elif sprite.rect.x < wrap_left:
                    sprite.rect.x = wrap_right
                elif sprite.rect.y > wrap_down:
                    sprite.rect.y = wrap_up
                elif sprite.rect.y < wrap_up:
                    sprite.rect.y = wrap_down

        # regular update
        for group in game_groups:
            if group.sprites():
                group.update()
            group.draw(display_surface)

        # health meters for the players
        for index, p in enumerate(player_group):
            render_text(bahn_small, str(p.health) + '%', p.rect.center[0], p.rect.center[1] - 30, p.clr,
                        display_surface)

        if not goal_group.sprites():
            render_text(bahn, 'You win!', half_win_w, half_win_h, white, display_surface)
            if not victory_music:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets/sound/retro_music/victory.ogg')
                pygame.mixer.music.play()
                victory_music = True
            if enemy_group.sprites():
                for e in enemy_group.sprites():
                    e.kill()
        elif not player_group.sprites():
            render_text(bahn, 'You lose!', half_win_w, half_win_h, white, display_surface)

        # check for system events from controller
        if all_ctls[0].get_button(6) == 1 or not player_group.sprites():
            pygame.mixer.music.stop()
            playing = False
            for x in range(0, 40):
                display_surface.fill(black)
                game_exit_sfx.play()
                render_text(bahn, 'Crossroads III', half_win_w, half_win_h - (half_win_h / 2) - 400 + (x * 10),
                            white, display_surface)
                screen.flip()
                game_clock.tick(target_fps)

            start_game.increment()
            menu = True
            run_game = False
        else:
            menu = False
            run_game = True
        # check for system events from computer
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        # refresh
    screen.flip()
    game_clock.tick(target_fps)
