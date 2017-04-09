import pygame

class Cell(pygame.sprite.Sprite):

    def __init__(self,data,resistance,moist,hunger,x,y):
        super(Cell,self).__init__()
        self.resistance = resistance
        self.moist = moist
        self.hunger = hunger
        self.x = round(x)
        self.y = round(y)
        self.counter = 0
        self.time = 5
        self.survivability = 1
        self.gridCol = self.x//data.cellSize
        self.gridRow = self.y//data.cellSize

    def updateSurvive(self, envAntibio, envMoist, envFood, rad): #based off RGB
        foodLeft = envFood - self.hunger
        M = abs(envMoist - self.moist)
        if self.resistance - envAntibio < 0:
            #more antibiotics than cell can resist
            self.survivability = -1
        moistModif = 1
        hungerModif = 2
        if foodLeft > 0:
            self.survivability = 1-M*moistModif - rad
        else:
            self.survivability = 1-M*moistModif + foodLeft*hungerModif - rad

    def spread(self, envH):
        time = 5
        H = envH - self.hunger
        if H<0: H == 1
        self.time = int(time - H*5)
