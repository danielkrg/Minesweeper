import sys
print(sys.version)
import pygame
import os
import random
pygame.init()

LIGHT_GRAY = (210, 210, 210)
GRAY = (180, 180, 180)
DARK_GRAY = (90, 90, 90)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FONT = pygame.freetype.SysFont("freesans", 20)

GAME_OVER = False

X_OFFSET = 300
Y_OFFSET = 200
TILE_WIDTH = 30
TILE_HEIGHT = 30
WIN_WIDTH, WIN_HEIGHT = (1000, 700)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" %(300, 100)
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Minesweeper')

class Tile(): 
	def __init__(self, row, col):
		self.isBomb = False
		self.val = 0
		self.width, self.height = (TILE_WIDTH, TILE_HEIGHT)
		self.x, self.y = (X_OFFSET + row*self.width, Y_OFFSET + col*self.height)
		self.button = pygame.Rect(self.x, self.y, self.width, self.height)
		self.reveal = False
		self.flagged = False

	def draw(self, win):
		if self.flagged:
			pygame.draw.rect(win, BLUE, self.button)

		elif not self.reveal:
			pygame.draw.rect(win, GRAY, self.button)

		elif self.reveal:
			if self.isBomb:
				pygame.draw.rect(win, RED, self.button)
			else:
				pygame.draw.rect(win, LIGHT_GRAY, self.button)
				if self.val > 0:
					FONT.render_to(win, (self.x + TILE_WIDTH/3, self.y + TILE_HEIGHT/3), str(self.val), BLACK)

	def pressed(self, win):
		global GAME_OVER
		if GAME_OVER:
			return

		x, y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		inBound = x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height
		if inBound and click[0] and self.isBomb:
			GAME_OVER = True
			return
		if inBound and click[0] == 1 and not self.isBomb:
			self.reveal = True
		elif inBound and click[2] == 1:
			self.flagged = True

def unfold(win, tiles, row, col, rows, cols):
	for i in range(row - 1, row + 2):
		for j in range(col - 1, col + 2):
			if i >= 0 and j >= 0 and i < rows and j < cols:
				tiles[i][j].reveal = True

def reveal_all_bombs(win, tiles, rows, cols):
	for i in range(rows):
		for j in range(cols):
			if tiles[i][j].isBomb:
				tiles[i][j].reveal = True

def draw_window(win, tiles, rows, cols):
	win.fill(WHITE)

	if GAME_OVER:
		FONT.render_to(win, (500, 100), "GAME OVER", RED)
		reveal_all_bombs(win, tiles, rows, cols)
	for i in range(rows):
		for j in range(cols):
			tiles[i][j].draw(win)
			tiles[i][j].pressed(win)
			if not tiles[i][j].isBomb and tiles[i][j].reveal and tiles[i][j].val == 0:
				unfold(win, tiles, i, j, rows, cols)

	for i in range(rows + 1):
		pygame.draw.line(win, DARK_GRAY, (X_OFFSET, Y_OFFSET + i*TILE_HEIGHT), (X_OFFSET + cols*TILE_WIDTH, Y_OFFSET + i*TILE_HEIGHT))

	for i in range(cols + 1):
		pygame.draw.line(win, DARK_GRAY, (X_OFFSET + i*TILE_WIDTH, Y_OFFSET), (X_OFFSET + i*TILE_WIDTH, Y_OFFSET + rows*TILE_HEIGHT))

	pygame.display.update()

def main():

	GAME_OVER = False

	rows, cols = (8, 8)
	numBombs = 10
	tiles = [[Tile(i, j) for i in range(cols)] for j in range(rows)]

	numRemaining = numBombs
	while numRemaining > 0:
		row, col = (random.randint(0, rows - 1), random.randint(0, cols - 1))
		if not tiles[row][col].isBomb:
			tiles[row][col].isBomb = True

			for i in range(row - 1, row + 2):
				for j in range(col - 1, col + 2):
					if i >= 0 and j >= 0 and i < rows and j < rows:
						if not tiles[i][j].isBomb:
							tiles[i][j].val += 1
						else:
							tiles[i][j].val = 0

			numRemaining -= 1
	
	clock = pygame.time.Clock()
	clock.tick(200)

	run = True
	while run:
		clock.tick(30)
		ev = pygame.event.get()
		for event in ev:
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			draw_window(win, tiles, rows, cols)
main()
