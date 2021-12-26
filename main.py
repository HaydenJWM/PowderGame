import pygame
import sys
import math

width = 1000
height = 1000
step = 20

gray = (100,100,100)
black = (0,0,0)
sand = (233,206,92)

#Sand Physics function
def sandPhys(cells,grid,screen):
    rows = int(height/step) - 1
    cols = int(width/step) - 1

    for x in range(len(cells)):
        if cells[x][1] < rows and not grid[cells[x][0]][cells[x][1]+1][0]: #Can the sand go down?
            grid[cells[x][0]][cells[x][1]][0] = False
            grid[cells[x][0]][cells[x][1]+1][0] = True
            
            cells[x][1] = cells[x][1] + 1
            updateScreen(screen,(cells[x][0]*step,(cells[x][1]-1)*step), black)
            updateScreen(screen,(cells[x][0]*step,cells[x][1]*step), sand)

        elif cells[x][0] < cols and cells[x][1] < rows and not grid[cells[x][0]+1][cells[x][1]][0] and not grid[cells[x][0]+1][cells[x][1]+1][0]: #Can the sand go right?
            grid[cells[x][0]][cells[x][1]][0] = False
            grid[cells[x][0]+1][cells[x][1]][0] = True
            
            cells[x][0] = cells[x][0] + 1
            updateScreen(screen,((cells[x][0]-1)*step,cells[x][1]*step), black)
            updateScreen(screen,(cells[x][0]*step,cells[x][1]*step), sand)

        elif cells[x][0] > 0 and cells[x][1] < rows and not grid[cells[x][0]-1][cells[x][1]][0] and not grid[cells[x][0]-1][cells[x][1]+1][0]: #Can the sand go left?
            grid[cells[x][0]][cells[x][1]][0] = False
            grid[cells[x][0]-1][cells[x][1]][0] = True
            
            cells[x][0] = cells[x][0] - 1
            updateScreen(screen,((cells[x][0]+1)*step,cells[x][1]*step), black)
            updateScreen(screen,(cells[x][0]*step,cells[x][1]*step), sand)

        

    return cells

#Draws the physical powder on the screen
def updateScreen(screen,pos,colour):
    x = math.floor(pos[1]/step)*step
    y = math.floor(pos[0]/step)*step
    pygame.draw.rect(screen,colour,(y+1,x+1,step-1,step-1))
    pygame.display.flip()

#Initializes the program
def main():
    #Initialize main grid
    activeCells = []
    gameBoard = [[[False,None] for x in range(int(width/step))] for y in range(int(height/step))] #Cells are (row,col,alive,species) (Species is 0 if not alive, 1 or 2 otherwise)
    #Initialize pygame window
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))

    #Draw initial lines on the screen (for testing)
    screen.fill(black)
    for x in range(0,height,step):
        pygame.draw.line(screen, gray, (0,x),(width,x))
    for x in range(0,width,step):
        pygame.draw.line(screen, gray, (x,0),(x,width))
    pygame.display.flip()   

    drawFlag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP: #Stop Drawing
                if(event.button == 1):
                    drawFlag = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #Start Drawing
                if (event.button == 1) and (gameBoard[math.floor(event.pos[0]/step)][math.floor(event.pos[1]/step)][0] == False):
                    colour = sand
                    gameBoard[math.floor(event.pos[0]/step)][math.floor(event.pos[1]/step)][0] = True
                    activeCells.append([math.floor(event.pos[0]/step),math.floor(event.pos[1]/step),colour,"SAND"]) 
                    updateScreen(screen,event.pos,colour)
                    drawFlag = True
            elif event.type == pygame.MOUSEMOTION and drawFlag and gameBoard[math.floor(event.pos[0]/step)][math.floor(event.pos[1]/step)][0] == False: #Keep Drawing
                    colour = sand
                    gameBoard[math.floor(event.pos[0]/step)][math.floor(event.pos[1]/step)][0] = True
                    activeCells.append([math.floor(event.pos[0]/step),math.floor(event.pos[1]/step),colour,"SAND"])
                    updateScreen(screen,event.pos,colour)
        activeCells = sandPhys(activeCells,gameBoard,screen)
if __name__ == "__main__":
    main()