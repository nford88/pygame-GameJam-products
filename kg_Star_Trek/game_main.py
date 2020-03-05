import pygame
import pygame.mixer
from pygame.locals import *
import random

pygame.init()

HEIGHT = 1200
WIDTH = 800
window = pygame.display.set_mode((HEIGHT, WIDTH))
GAME_OVER = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 180, 94)
BRIGHT_BLUE = (0, 0, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 220, 0)
CORAL = (255, 99, 71)

clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((HEIGHT, WIDTH))

title_image = pygame.image.load("images/title.png")
victory_image = pygame.image.load("images/victory.png")
gameover_image = pygame.image.load("images/gameover.png")
pygame.display.set_caption("Star Trek Battle")
fed_ship = pygame.image.load("images/fed_ship.png")
klingon_ship = pygame.image.load("images/klingon_ship.png")
ida =  pygame.image.load("images/ida_resized.png")
kirk =  pygame.image.load("images/kirk_resized.png")


explosion_image = pygame.image.load("images/blast.png")
small_text = pygame.font.Font("freesansbold.ttf", 14)
hull_text = pygame.font.Font("freesansbold.ttf", 12)
sp_text = pygame.font.Font("freesansbold.ttf", 12)
scan_text = pygame.font.Font("freesansbold.ttf", 12)

fed_hull = 100
fed_sensor_strength = 1
fed_weapon = 8
fed_repair = 11
fed_spare_parts = 4

fed_scan_sound = "sounds/tos_scanner.wav"
fed_weapon_sound = "sounds/tos_ship_phaser_1.wav"
fed_repair_sound = "sounds/force_field_hit.wav"

klingon_hull = 100
klingon_sensor_strength = 1
klingon_weapon = 10
klingon_repair = 8
klingon_spare_parts = 4

# klingon_scan_sound = "sounds/klingon_disruptor_clean.mp3"
# klingon_weapon_sound = "sounds/klingon_disruptor_clean.mp3"
# klingon_repair_sound = "sounds/klingon_disruptor_clean.mp3"

explosion_sound = "sounds/largeexplosion1.wav"
intro_sound = "sounds/intro.wav"
play_explosion = True
intro = True

def star_field(number_of_stars):
    for star in range(0, number_of_stars):
        pygame.draw.rect(window, WHITE, (random.randint(1, HEIGHT), random.randint(1, WIDTH), 2, 2))
def game_title(x, y):
    gameDisplay.blit(title_image, (x, y))

def victory_title(x, y):
    gameDisplay.blit(victory_image, (x, y))
def game_over(x, y):
    gameDisplay.blit(gameover_image, (x, y))

def fed_ship_function(x, y):
    gameDisplay.blit(fed_ship, (x, y))
def klingon_ship_function(x, y):
    gameDisplay.blit(klingon_ship, (x, y))
def ida_function(x, y):
    gameDisplay.blit(ida, (x, y))
def kirk_function(x, y):
    gameDisplay.blit(kirk, (x, y))

def ship_explosion(x, y):
    gameDisplay.blit(explosion_image, (x, y))

def button(x, y, height, width, colour, hover_colour, label):
    if x + height > mouse[0] > x and y + width > mouse[1] > y:
        pygame.draw.rect(gameDisplay, hover_colour, (x, y, height, width))
    else:
        pygame.draw.rect(gameDisplay, colour, (x, y, height, width))
    textSurf, textRect = button_text_objects(label, small_text)
    textRect.center = ((x+25), (y+20))
    gameDisplay.blit(textSurf, textRect)
def button_text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def hull_text_objects(text, font):
    textSurface = font.render(text, True, YELLOW)
    return textSurface, textSurface.get_rect()
def display_hull(x, y, hull):
    textSurf2, textRect2 = hull_text_objects(hull, hull_text)
    textRect2.center = (x, y)
    gameDisplay.blit(textSurf2, textRect2)

def sp_text_objects(text, font):
    textSurface = font.render(text, True, BRIGHT_GREEN)
    return textSurface, textSurface.get_rect()
def display_sp(x, y, sp):
    textSurf2, textRect2 = sp_text_objects(sp, sp_text)
    textRect2.center = (x, y)
    gameDisplay.blit(textSurf2, textRect2)

def scan_text_objects(text, font):
    textSurface = font.render(text, True, CORAL)
    return textSurface, textSurface.get_rect()
def display_scan(x, y, scan):
    textSurf2, textRect2 = scan_text_objects(scan, scan_text)
    textRect2.center = (x, y)
    gameDisplay.blit(textSurf2, textRect2)

def increase_sensor_strenght(sensor_strength):
    if sensor_strength < 4:
        new_sensor_strength = sensor_strength + 1
        print("sensor strength boosted from factor {} to factor {}".format(sensor_strength, new_sensor_strength))
        return new_sensor_strength
    else:
        print("Sensors at maximum power!")
        return sensor_strength
def decrease_enemy_sensor_strenght(sensor_strength):
    if sensor_strength > 1:
        new_sensor_strength = sensor_strength - 1
        print("sensor strength countered from factor {} to factor {}".format(sensor_strength, new_sensor_strength))
        return new_sensor_strength
    else:
        print("Enemy Sensors at minimum power!")
        return sensor_strength

def repair_hull(hull, repair_value):
    if hull < 100:
        new_hull = hull + repair_value
        if new_hull > 100:
            new_hull = 100
        return new_hull
    else:
        print("Hull is at maximum")
        return hull

def calculate_damage_to_ship(hull, weapon, sensor_strength):
    hit = random.randint(sensor_strength, 10)
    print("random ({}/4 -> 10) = {}".format(sensor_strength, hit))
    if hit > 5:
        print("Hit!")
        print("Previous Hull: {}".format(hull))
        print("Weapon hit: {}".format(weapon))
        hull = hull - weapon
        print("Current Hull: {}".format(hull))
        if hull < 0:
            pygame.mixer.music.load(explosion_sound)
            pygame.mixer.music.play()
    else:
        print("Missed!")
    return hull

def klingon_action(klingon_hull, fed_hull, klingon_spare_parts, klingon_sensor_strength, fed_sensor_strength):
    print("** Enemy Action **")
    print("hull:{} - SP:{}".format(klingon_hull, klingon_spare_parts))
    if klingon_hull <= 80:
        if klingon_spare_parts > 0:
            print("1")
            choice = random.randint(1, 10)
        else:
            print("2")
            choice = random.randint(1, 8)
    else:
        print("3")
        choice = random.randint(1, 8)

    print("choice: {}".format(choice))
    # 1-2 = Scan
    # 3-7 = Fire
    # 9-10 = Repair
    if choice <= 2:
        print("Enemy Scan")
        # pygame.mixer.music.load(klingon_scan_sound)
        # pygame.mixer.music.play()
        new_klingon_sensor_strength = increase_sensor_strenght(klingon_sensor_strength)
        new_fed_sensor_strength = decrease_enemy_sensor_strenght(fed_sensor_strength)
        pygame.draw.line(window, Color("orange"), (90, 250), (4500, 800), 2)
        pygame.draw.line(window, Color("orange"), (90, 250), (2300, 1800), 2)
        # pygame.draw.line(window, Color("yellow"), (1, 10), (900, 450), 2)
        # pygame.draw.line(window, Color("yellow"), (250, 150), (110, 410), 2)
        return klingon_hull, fed_hull, klingon_spare_parts, new_klingon_sensor_strength, new_fed_sensor_strength
    elif choice <= 8:
        print("Enemy Fire")
        # pygame.mixer.music.load(klingon_weapon_sound)
        # pygame.mixer.music.play()
        new_fed_hull = calculate_damage_to_ship(fed_hull, fed_weapon, fed_sensor_strength)
        pygame.draw.line(window, Color("green"), (10, 200), (3000, 1000), 2)
        pygame.draw.line(window, Color("green"), (10, 270), (2500, 800), 2)
        # pygame.mixer.music.load(fed_taking_dmg)
        # pygame.mixer.music.play()
        return klingon_hull, new_fed_hull, klingon_spare_parts, klingon_sensor_strength, fed_sensor_strength
    elif choice <= 10:
        print("Repair")
        # pygame.mixer.music.load(klingon_repair_sound)
        # pygame.mixer.music.play()
        if klingon_spare_parts > 0:
            new_klingon_spare_parts = klingon_spare_parts - 1
            new_klingon_hull = repair_hull(klingon_hull, klingon_repair)
            pygame.draw.rect(gameDisplay, (255, 0, 0), (40, 180, 160, 3))
            pygame.draw.rect(gameDisplay, (255, 0, 0), (40, 300, 160, 3))
            return new_klingon_hull, fed_hull, new_klingon_spare_parts, klingon_sensor_strength, fed_sensor_strength
        else:
            return klingon_hull, fed_hull, klingon_spare_parts, klingon_sensor_strength, fed_sensor_strength

while not GAME_OVER:

    window.fill(BLACK)
    if intro:
        pygame.mixer.music.load(intro_sound)
        pygame.mixer.music.play()
        intro = False

    ida_function(10, 10)
    display_hull(44, 140, "{}".format("Nuntuk (IDA)"))
    kirk_function(1050, 550)
    display_hull(1095, 720, "{}".format("Kirk (James.T)"))

    star_field(30)
    game_title(510, 5)

    if fed_hull > 0:
        fed_ship_function(900, 400)
    else:
        ship_explosion(700, 300)
        game_over(475, 300)
        if play_explosion:
            pygame.mixer.music.load(explosion_sound)
            pygame.mixer.music.play()
            play_explosion = False

    if klingon_hull > 0:
        klingon_ship_function(5, 200)
    else:
        victory_title(270, 200)
        ship_explosion(-120, 10)
        if play_explosion:
            pygame.mixer.music.load(explosion_sound)
            pygame.mixer.music.play()
            play_explosion = False

    display_hull(910, 410, "Hull:{}%".format(fed_hull))
    display_scan(990, 410, "Sensors:{}/4".format(fed_sensor_strength))
    display_sp(1070, 410, "Repair:{}".format(fed_spare_parts))

    display_hull(35, 185, "Hull:{}%".format(klingon_hull))
    display_scan(110, 185, "Sensors:{}/4".format(klingon_sensor_strength))
    display_sp(190, 185, "Repairs:{}".format(klingon_spare_parts))

    for event in pygame.event.get():
        # print("event: {}".format(event))
        if event.type == pygame.QUIT:
            GAME_OVER = True

        if event.type == MOUSEBUTTONDOWN:
            print("** Player Action **")
            mouse_position = pygame.mouse.get_pos()
            x = mouse_position[0]
            y = mouse_position[1]

            if (x >= 860 and x <= 910) and (y >= 650 and y <= 690):
                print("SCAN")
                pygame.draw.line(window, Color("yellow"), (1, 420), (900, 450), 2)
                pygame.draw.line(window, Color("yellow"), (1, 10), (900, 450), 2)
                pygame.draw.line(window, Color("yellow"), (250, 150), (110, 410), 2)
                pygame.mixer.music.load(fed_scan_sound)
                pygame.mixer.music.play()
                fed_sensor_strength = increase_sensor_strenght(fed_sensor_strength)
                klingon_sensor_strength = decrease_enemy_sensor_strenght(klingon_sensor_strength)

            if (x >= 920 and x <= 970) and (y >= 650 and y <= 690):
                print("FIRE")
                pygame.draw.line(window, Color("red"), (130, 240), (900, 450), 2)
                klingon_hull = calculate_damage_to_ship(klingon_hull, fed_weapon, fed_sensor_strength)
                pygame.mixer.music.load(fed_weapon_sound)
                pygame.mixer.music.play()

            if (x >= 980 and x <= 1030) and (y >= 650 and y <= 690):
                print("REPAIR")
                if fed_hull < 100:
                    if fed_spare_parts > 0:
                        pygame.draw.rect(gameDisplay, (0, 255, 0), (920, 430, 220, 2))
                        pygame.draw.rect(gameDisplay, (0, 255, 0), (920, 520, 220, 2))
                        fed_hull = repair_hull(fed_hull, fed_repair)
                        fed_spare_parts = fed_spare_parts - 1
                        pygame.mixer.music.load(fed_repair_sound)
                        pygame.mixer.music.play()
                        if fed_hull > 100:
                            fed_hull = 100
                else:
                    print("Hull is already maximum")

            print("\n")
            klingon_hull, fed_hull, klingon_spare_parts, klingon_sensor_strength, fed_sensor_strength = klingon_action(klingon_hull, fed_hull, klingon_spare_parts, klingon_sensor_strength, fed_sensor_strength)
            print("\n")

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print("Click: {}".format(click))
    # print("mouse: {}".format(mouse))

    button(860, 650, 50, 40, BLUE, BRIGHT_YELLOW, "Scan")
    button(920, 650, 50, 40, BLUE, BRIGHT_RED, "Fire")
    button(980, 650, 50, 40, BLUE, BRIGHT_GREEN, "Repair")

    pygame.display.update()
    clock.tick(7)

pygame.quit()
quit()
