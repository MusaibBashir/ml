import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Set screen size
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up game grid
grid_size = 10
rows = int(screen_height / grid_size)
cols = int(screen_width / grid_size)
grid = np.zeros((rows, cols), dtype=int)
# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
green1 = (0, 255, 0)
green2= (0, 200, 0)
green3 = (0, 150, 0)
green4 = (0, 100, 0)
green5 = (0, 50, 0)
blue1 = (0, 0, 255)
blue2= (0, 0, 200)
blue3= (0, 0, 150)
blue4= (0, 0, 100)
blue5= (0, 0, 50)
color_code=[2,3,4,5,6,7,8,9,10,11]

# Initialize ant positions and directions
num_ants = 2
ant_positions = np.zeros((num_ants, 2), dtype=int)
ant_directions = np.zeros(num_ants, dtype=int)
# Set ant positions and directions randomly
for i in range(num_ants):
    ant_positions[i] = np.array([20+5*i, 30+5*i])
    ant_directions[i] = np.random.randint(4)

def phermone_decay(phermone_grid, ant_positions):
    x, y = ant_positions
    for i in range(phermone_grid.shape[0]):
        for j in range(phermone_grid.shape[1]):
            if phermone_grid[i, j] > 0:
                phermone_grid[i, j] -= 1
    phermone_grid[x, y] = 4

def prob_phermone(phermone_grid, direction, ant_positions, self_or_cross):
    if self_or_cross == 1:
        r = 0.8
    else:
        r = 0.2
    step_till_5 = phermone_grid[ant_positions[0], ant_positions[1]]
    
    if step_till_5 == 0:
        return 0  # Default direction if no pheromone is present
    
    probabilities = [r * step_till_5, (1 - r) * step_till_5]
    result = random.choices([-1, 1], weights=probabilities, k=1)[0]
    return result

def colour_update(phermone_grid, grid, ant):
    phermone_colors_green = [2,3,4,5,6]
    phermone_colors_blue = [7,8,9,10,11]
    
    for i in range(phermone_grid.shape[0]):
        for j in range(phermone_grid.shape[1]):
            if phermone_grid[i, j] > 0:
                if ant == 1:
                    grid[i, j] = phermone_colors_green[phermone_grid[i, j]]
                else:
                    grid[i, j] = phermone_colors_blue[phermone_grid[i, j]]

 
phermone_grid = np.zeros((rows,cols), dtype=int)
# Run simulation
steps = 30000
for step in range(steps):
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Update ant positions and directions
    for i in range(num_ants):
        if i==0:
            ant=1
        else:
            ant=2
        row, col = ant_positions[i][0],ant_positions[i][1]
        direction = ant_directions[i]
        
        phermone_decay(grid,ant_positions[i])
        # Update grid
        if grid[row, col] == 0:
            ant_directions[i] = (direction + 1) % 4
        elif grid[row, col] == 1:
            ant_directions[i] = (direction - 1) % 4
        elif grid[row, col] == color_code[i]:
            ant_directions[i] = (prob_phermone(phermone_grid,direction, ant_positions[i],1)+ direction) % 4
        else:
            ant_directions[i] = (prob_phermone(phermone_grid,direction, ant_positions[i],2) + direction) % 4 
        colour_update(phermone_grid, grid, ant)
        # Move ant
        if ant_directions[i] == 0:
            row -= 1
        elif ant_directions[i] == 1:
            col += 1
        elif ant_directions[i] == 2:
            row += 1
        else:
            col -= 1

        # Wrap ant around edges of screen
        row = row % rows
        col = col % cols
        ant_positions[i] = np.array([row, col])

    # Draw grid and ants
    screen.fill(black)
    for row in range(rows):
        for col in range(cols):
            x = col * grid_size
            y = row * grid_size
            if grid[row, col] == 1:
                pygame.draw.rect(screen, white, (x, y, grid_size, grid_size))
            elif grid[row, col] == 2:
                pygame.draw.rect(screen, green1, (x, y, grid_size, grid_size))
            elif grid[row, col] == 3:
                pygame.draw.rect(screen, green2, (x, y, grid_size, grid_size))
            elif grid[row,col]==4:
                pygame.draw.rect(screen, green3, (x, y, grid_size, grid_size))
            elif grid[row,col]==5:
                pygame.draw.rect(screen, green4, (x, y, grid_size, grid_size))
            elif grid[row,col]==6:
                pygame.draw.rect(screen, green5, (x, y, grid_size, grid_size))
            elif grid[row, col] == 7:
                pygame.draw.rect(screen, blue1, (x, y, grid_size, grid_size))
            elif grid[row, col] == 8:
                pygame.draw.rect(screen, blue2, (x, y, grid_size, grid_size))
            elif grid[row,col]==9:
                pygame.draw.rect(screen, blue3, (x, y, grid_size, grid_size))
            elif grid[row,col]==10:
                pygame.draw.rect(screen, blue4, (x, y, grid_size, grid_size))
            elif grid[row,col]==11:
                pygame.draw.rect(screen, blue5, (x, y, grid_size, grid_size))
    for i in range(num_ants):
        x = ant_positions[i, 1] * grid_size
        y = ant_positions[i, 0] * grid_size
        if ant_directions[i] == 0:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, grid_size, grid_size))
        elif ant_directions[i] == 1:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, grid_size, grid_size))
        elif ant_directions[i] == 2:
            pygame.draw.rect(screen, (0, 0, 255), (x, y, grid_size, grid_size))
        else:
            pygame.draw.rect(screen, (255, 255, 0), (x, y, grid_size, grid_size))

    # Update screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
