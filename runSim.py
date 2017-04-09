import sys
import random
import math
import pygame
from PIL import Image
from cell import Cell

def dist2(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)

def get_cell_mutation(data):
    Res = random.normalvariate(0,.1)
    Moi = random.normalvariate(0,.1)
    Hung = random.normalvariate(0,.1)
    return (Res*2*data.radiation + Res,
            Moi*2*data.radiation + Moi,
            Hung*2*data.radiation + Hung)

def alterCells(data):
    survived = []
    for cell in data.cells:
        res,moi,hunger = get_cell_mutation(data)
        res += cell.resistance
        if res < 0: res = 0
        if res > 1: res = 1
        moi += cell.moist
        if moi < 0: moi = 0
        if moi > 1: moi = 1
        hunger += cell.hunger
        if hunger < 0.25: hunger = 0.25
        if hunger > 1: hunger = 1
        (cell.res, cell.moi, cell.hunger) = (res, moi, hunger)
        R,G,B = data.rgbImage.getpixel((cell.x,cell.y))
        envAntibio,envFood,envMoist = R/255,1-G/255,B/255
        if (dist2(cell.x, cell.y, data.width//2,
                    data.height//2) < data.buffer**2):
            envAntiBio, envMoist, envFood = 0, 0.5, 1
        cell.updateSurvive(envAntibio,envMoist,envFood,data.radiation)
        if cell.survivability > 0 and random.random()<=cell.survivability:
            survived.append(cell)
        else:
            del data.dict[(cell.gridRow, cell.gridCol)]
    data.cells = survived

def movePossible(data, x,y):
    randomStart = random.randint(0,360)
    for i in range(randomStart,randomStart+360,10):
        radians = i*math.pi/180
        newX = data.radius*2*math.cos(radians) + x
        newY = data.radius*2*math.sin(radians) + y
        row,col = newY//data.cellSize,newX//data.cellSize
        for dR,dC in data.directions:
            if data.dict.get((row+dR,col+dC),0) != 0:
                cellX, cellY = data.dict.get((row+dR, col+dC))
                if (dist2(newX, newY, cellX, cellY) <(2*data.radius)**2 or
                            newX < 1 or newX > data.width-1 or newY < 1 or
                            newY >data.height-1):
                            return -1,-1
        return round(newX),round(newY)

def newCells(data):
    for cell in data.cells:
        cell.counter += 1
        if cell.counter >= cell.time:
            cell.counter = 0
            x,y = movePossible(data, cell.x,cell.y)
            if x == -1:
                continue
            else:
                (newX, newY) = x,y
                Res,Moi,Foo = get_cell_mutation(data)
                Res += cell.resistance
                if Res < 0: Res = 0
                if Res > 1: Res = 1
                Moi += cell.moist
                if Moi < 0: Moi = 0
                if Moi > 1: Moi = 1
                Foo += cell.hunger
                if Foo < 0.25: Foo = 0.25
                if Foo > 1: Foo = 1
                new = Cell(data, Res,Moi,Foo,newX,newY)
                R,G,B = data.rgbImage.getpixel((cell.x,cell.y))
                R,G,B = R/256,1-G/256,B/256
                if (dist2(cell.x, cell.y, data.width//2,
                         data.height//2) < data.buffer**2):
                    R, B, G = 0, 0.5, 1
                new.updateSurvive(R,B,G,data.radiation)
                if new.survivability > 0:
                    new.spread(B)
                    data.cells.append(new)
                    data.dict[(new.gridRow,new.gridCol)]=(new.x,new.y)


############# pygame stuff
##(structure derived from eventsexample.py and Lukas Perana's pygame structure)

def init(data):
    data.splash = True
    data.gameStart = False
    data.playing = True
    data.isPaused = False
    data.fps = 10
    initGameStart(data)

def initGameStart(data):
    data.radiation = 0
    data.radCount = 0
    data.radiationUpdate = data.fps
    data.dRadiation = 0.0001
    data.radius = min(data.width,data.height)//40
    data.buffer = min(data.width, data.height)//15
    data.cellSize = (2*data.radius//math.sqrt(2))
    data.directions = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                       (-1, -2), (-1,-1), (-1, 0), (-1, 1), (-1, 2),
                       (0, -2), (0, -1), (0, 0), (0, 1), (0, 2),
                       (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                       (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
    data.cells = [Cell(data, 0,0.5,1,data.width//2,data.height//2)]
    data.dict = {(data.cells[0].gridRow, data.cells[0].gridCol):(data.width/2,
                                                             data.height//2)}


def redrawAll(data, screen):
    if data.splash: redrawAllSplash(data, screen)
    elif data.gameStart:
        for cell in data.cells:
            color = (cell.resistance*255, cell.moist*255, cell.hunger*255)
            pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), data.radius)
            pygame.draw.circle(screen, (0, 0, 0), (int(cell.x), int(cell.y)),
                            data.radius, 2)

        font = pygame.font.Font(None, 25)
        text = font.render("REMs delivered: %f"% (data.radiation*100), True, (0,0,0))
        text_rect = text.get_rect(center=(data.width/2, 50/2))
        screen.blit(text, text_rect)
        if data.isPaused:
            text = font.render("PAUSED", True, (0,0,0))
            text_rect = text.get_rect(center=(data.width/2, 100/2))
            screen.blit(text, text_rect)

def timerFired(data):
    if data.splash: return
    elif data.isPaused: return
    elif data.gameStart:
        data.radCount+=1
        if data.radiation > 0 and data.radCount>=data.radiationUpdate:
            alterCells(data)
            data.radCount = 0
        newCells(data)
        liveCells = []
        for cell in range(len(data.cells)):
            if random.random()<=data.cells[cell].survivability*3/2:
                liveCells.append(data.cells[cell])
            else:
                del data.dict[(data.cells[cell].gridRow,
                               data.cells[cell].gridCol)]
        data.cells = liveCells

def mousePressed(data, x, y):
    if data.splash: return
    elif data.gameStart:
        collision = False
        for cell in data.cells:
            if (dist2(x, y, cell.x, cell.y) < (2*data.radius)**2 or
                x < 0 or x > data.width or y < 0 or y >data.height):
                collision = True
                break
        if not collision:
            newResist = random.normalvariate(0.1, 0.03)
            if newResist<0 or newResist>1: newResist = 0
            newMoisture = random.normalvariate(0.5,0.2)
            if newMoisture<0 or newMoisture>1: newMoisture = 0
            newHunger = random.normalvariate(0.9, 0.2)
            if newHunger<0.25 or newHunger>1: newHunger = 1
            newCell = Cell(data, newResist, newMoisture, newHunger,x, y)
            R,G,B = data.rgbImage.getpixel((newCell.x,newCell.y))
            R,G,B = R/256,1-G/256, B/256
            newCell.updateSurvive(R, B, G, data.radiation)
            data.cells.append(newCell)
            data.dict[newCell.gridRow, newCell.gridCol]=(x, y)

def keyPressed(data, key):
    if data.splash: keyPressedSplash(data, key)
    elif data.gameStart:
        if key == pygame.K_r:
            initGameStart(data)
        if key == pygame.K_p:
            data.isPaused = not data.isPaused
        if key == pygame.K_n:
            newCells(data)
        if key == pygame.K_UP:
            data.radiation+=data.dRadiation
        if key == pygame.K_DOWN and data.radiation>0.00000005:
            data.radiation-=data.dRadiation

##########
def initSplash(data):
    pass

def redrawAllSplash(data, screen):
    #sorry about this part; we're running out of time
    font1 = pygame.font.Font('freesansbold.ttf', 20)
    font2 = pygame.font.Font('freesansbold.ttf', 13)
    text1 = font1.render("Hello!", 1, (0,0,0))
    text1_rect = text1.get_rect(center = (data.width/2, 40))
    text2 = font2.render("This is a simulation of bacteria living on an image.",
                         1, (0, 0, 0))
    text2_rect = text2.get_rect(center = (data.width/2, 90))
    text3text = "The colors of the image represent different environments"
    text3 = font2.render(text3text, 1, (0, 0, 0))
    text3_rect = text3.get_rect(center = (data.width/2, 140))
    text4text = "Press the up and down arrow keys to change radiaton exposure"
    text4 = font2.render(text4text, 1, (0, 0, 0))
    text4_rect = text4.get_rect(center = (data.width/2, 190))
    text5text = "Press 'p' at any time to pause"
    text5 = font2.render(text5text, 1, (0,0,0))
    text5_rect = text5.get_rect(center = (data.width/2, 240))
    text6text = "Click anywhere to drop a colony!"
    text6 = font2.render(text6text, 1, (0,0,0))
    text6_rect = text6.get_rect(center = (data.width/2, 290))
    text7text = "(No guarantees it will live, though)"
    text7 = font2.render(text7text, 1, (0,0,0))
    text7_rect = text7.get_rect(center = (data.width/2, 310))
    text8 = font2.render("Press 'r' to reset the growth", 1, (0, 0, 0))
    text8_rect = text8.get_rect(center = (data.width/2, 350))
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    screen.blit(text3, text3_rect)
    screen.blit(text4, text4_rect)
    screen.blit(text5, text5_rect)
    screen.blit(text6, text6_rect)
    screen.blit(text7, text7_rect)
    screen.blit(text8, text8_rect)

def keyPressedSplash(data, key):
    if key == pygame.K_RETURN:
        data.splash = False
        data.gameStart = True

def run(imagePath):
    class Struct(object): pass
    data = Struct()
    #creates image for background)
    image = Image.open(imagePath)
    data.image = pygame.image.load(imagePath)
    data.rgbImage = image.convert('RGB')
    data.width, data.height = image.size
    init(data)
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((data.width, data.height))
    while data.playing:
        time = clock.tick(data.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data.playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePressed(data, *event.pos)
            elif event.type == pygame.KEYDOWN:
                keyPressed(data, event.key)
        screen.fill((255, 255, 255))
        if data.gameStart:
            screen.blit(data.image, (0, 0))
        timerFired(data)
        redrawAll(data, screen)
        pygame.display.flip()
    pygame.quit()

run("default.png")
