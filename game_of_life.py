from glob import glob
import random
import time
import pygame

import cv2

pygame.init()

width = 1200
height = 1200
tile_size = 10

grid_width = int(width/tile_size)
grid_height = int(height/tile_size)

# Colors for the games
tile_color = (0, 0, 0)
display_color = (255, 255, 255)
grid_color = (200, 200, 200)

screen = pygame.display.set_mode((width, height))
screen.fill(display_color)

tiles = []

grid = [[0 for x in range(grid_width)] for y in range(grid_height)]
backup_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

def get_image():
	# TODO: Clean up
	global grid
	global backup_grid
	global grid_width
	global grid_height

	originalImage = cv2.imread(
		'/Users/ahalat/Downloads/test.jpg')
	grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

	(_, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 255, cv2.THRESH_BINARY)

	width = blackAndWhiteImage.shape[1]
	height = blackAndWhiteImage.shape[0]

	grid_width = int(width/tile_size)
	grid_height = int(height/tile_size)

	grid = [row[:] for row in blackAndWhiteImage]
	backup_grid = [row[:] for row in blackAndWhiteImage]

	# loop over the image
	for x in range(0, height, tile_size):
		for y in range(0, width, tile_size):
			if blackAndWhiteImage[x][y] == 0:
				grid[int(x/tile_size)][int(y/tile_size)] = 1
				backup_grid[int(x/tile_size)][int(y/tile_size)] = 1
			else:
				grid[int(x/tile_size)][int(y/tile_size)] = 0
				backup_grid[int(x/tile_size)][int(y/tile_size)] = 0

	screen = pygame.display.set_mode((width , height))
	screen.fill(display_color)

def grid_lines():
	# Drawing the Lines for each grid box
	for x in range(0, width, tile_size):
		pygame.draw.line(screen, grid_color, (x, 0), (x, height))
	for y in range(0, height, tile_size):
		pygame.draw.line(screen, grid_color, (0, y), (width, y))

def draw_tile(x, y, color):
	pygame.draw.rect(screen, color, (x * tile_size, y * tile_size, tile_size, tile_size))

def draw_grid():
	for x in range(grid_height):
		for y in range(grid_width):
			if grid[x][y] == 1:
				# Color to Black
				draw_tile(y, x, tile_color)
			else:
				# Color to White
				draw_tile(y, x, display_color)

def initialize_glider():
	x = int(grid_width/2)
	y = int(grid_height/2)

	grid[x + 0][y + 1] = 1
	grid[x + 1][y + 2] = 1
	grid[x + 2][y + 0] = 1
	grid[x + 2][y + 1] = 1
	grid[x + 2][y + 2] = 1


def initialize_osilator():
	x = int(grid_width/2)
	y = int(grid_height/2)

	grid[x + 0][y + 1] = 1
	grid[x + 0][y + 2] = 1
	grid[x + 0][y + 3] = 1

def initialize_state():
	for x in range(grid_height):
		for y in range(grid_width):
			random_num = random.random()
			if random_num < 0.2:
				grid[x][y] = 1
				backup_grid[x][y] = 1


def get_live_neighbours(x, y):
	num_live = 0

	for i in range(-1, 2):
		for j in range(-1, 2):
			if (i == 0 and j == 0) or (x - i < 0) or (x + i >= grid_height) or (y - j < 0) or (y + j >= grid_width):
				continue
			if is_alive(x + i, y + j):
				num_live += 1

	return num_live


def is_alive(x, y):
	return grid[x][y] == 1

def kill_tile(x, y):
	backup_grid[x][y] = 0

def revive_tile(x, y):
	backup_grid[x][y] = 1

def update():
	for x in range(grid_height):
		for y in range(grid_width):
			live_neighbours = get_live_neighbours(x, y)
			if (is_alive(x, y) and (live_neighbours < 2 or live_neighbours > 3)):
				kill_tile(x, y)
			if (not is_alive(x, y) and live_neighbours == 3):
				revive_tile(x, y)


if __name__ == '__main__':
	pygame.display.set_caption('Game of Life')
	# clock = pygame.time.Clock()
	running = True

	get_image()

	# initialize_state()
	# initialize_osilator()
	# initialize_glider()
	draw_grid()
	grid_lines()
	pygame.display.flip()
	first = True

	time.sleep(2)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill(display_color)

		backup_grid = [row[:] for row in grid]
		update()
		grid = [row[:] for row in backup_grid]

		draw_grid()
		grid_lines()
		pygame.display.flip()
		time.sleep(0.1)

	pygame.quit()
