# Bomb Catcher Game
import sys, random, time, pygame
from pygame.locals import *

def print_text(font, x, y, text, color=(255, 255, 255)):
	imgText = font.render(text, True, color)
	screen.blit(imgText, (x, y))

def velocity(lives, score):
	initalVel = vel_y
	initalVel += (lives * score) / 20
	return initalVel
	
#main program begins
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Ida the Oil Hunter")
font1 = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 72)
pygame.mouse.set_visible(False)
white = 255, 255, 255
red = 220, 50, 50
yellow = 230, 230, 50
black = 0, 0, 0
background = pygame.image.load('norway_map.jpg')
bus = pygame.image.load('bus_Sprite_Ida1.png')
oil = pygame.image.load('oil_trans.png')

lives = 3
score = 0
game_over = True
mouse_x = mouse_y = 0
pos_x = 0
pos_y = 490
bomb_x = random.randint(0, 600)
bomb_y = 0
vel_y = 7.0

#repeating loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		elif event.type == MOUSEMOTION:
			mouse_x, mouse_y = event.pos
			move_x, move_y = event.rel
		elif event.type == MOUSEBUTTONUP:
			if game_over:
				game_over = False
				lives = 3
				score = 0
				
	keys = pygame.key.get_pressed()
	if keys[K_ESCAPE]:
		sys.exit()
		
	screen.fill((0, 0, 0))
	screen.blit(background, (0, 0))

	if game_over:
		screen.fill((255, 255, 255))
		if lives == 0:
			print_text(font2, 150, 100, ("BARRELS :  " + str(score)) , color=(0, 0, 100))
			vel_y = 7.0
		print_text(font2, 50, 320, "IDA THE OIL HUNTER", color=(197, 13, 13))
		print_text(font2, 140, 400, "CLICK TO PLAY", color=(197, 13, 13))
	else:
		#move the bomb
		bomb_y += vel_y
		#has the player missed the bomb?
		if bomb_y > 600:
			bomb_x = random.randint(0, 600)
			bomb_y = -50
			lives -= 1
			if lives == 0:
				game_over = True
		#see if player has caught the bomb
		elif bomb_y > pos_y:
			if bomb_x > pos_x and bomb_x < pos_x + 120:
				score += 10
				bomb_x = random.randint(0, 600)
				bomb_y = -50
				vel_y = velocity(lives, score)
		#draw the bomb
		screen.blit(oil, (bomb_x, int(bomb_y)))
		#set basket position
		pos_x = mouse_x
		if pos_x < 0:
			pos_x = 0
		elif pos_x > 600:
			pos_x = 600
		#draw the basket
		screen.blit(bus, (pos_x, pos_y))
	#print # of lives
	print_text(font1, 0, 0, "LIVES: " + str(lives))
	#print scores
	print_text(font1, 500, 0, "BARRELS: " + str(score))
	pygame.display.update()