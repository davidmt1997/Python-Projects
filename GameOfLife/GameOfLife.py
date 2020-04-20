import pygame
import numpy as np
import time


pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

# Number of cells
nxC, nyC = 50, 50

# Dimension of the cells
dimCW = width / nxC
dimCH = height / nyC

#State of the cells, 1 = alive, 0 = dead
gameState = np.zeros((nxC, nyC))

gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Controlling the execution of the game
pauseExect = False

# Execution loop
while True:

    new_game_state = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    ev = pygame.event.get()

    for event in ev:
        # Pause the game when pressing any key
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        # Make a cell "alive" by clicking right in your mouse
        # Make a cell "die" by left clicking your mouse
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            new_game_state[celX, celY] = not mouseClick[2]


    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
                # Calculating the state of neighbors
                # % operators to wrap around the edges
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x)  % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x) % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule 1: a dead cell qith 3 neighbors alive, revives
                if gameState[x, y] == 0 and n_neigh == 3:
                    new_game_state[x, y] = 1
                # Rule 2: an alive cell with less than 2 or more than 3 alive cells, dies
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_game_state[x, y] = 0
            # Creating the polygon to draw
            poly = [(x * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    (x * dimCW, (y+1) * dimCH)]

            # Draw the cell for each x and y
            if new_game_state[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Update state of the game
    gameState = np.copy(new_game_state)
    pygame.display.flip()