import sys
import random
import math

class Cell(object):

  def __init__(self,resistance,moist,hunger,x,y,survive):
      #super(Cell,self(),__init__())
      self.resistance = resistance
      self.moist = moist
      self.hunger = hunger
      self.survivability = survive
      self.x = x
      self.y = y
      self.counter = 0
      self.time = 5


  def live(self, envR, envM, envH, rad): #based off of RGB
      R = self.resistance - envR
      H = envH - self.hunger
      M = abs(envM - self.moist)
      if R <= 0:
          cell.survivability = -1

      moisModif = 1
      hunModif = 1

      if H > 0:
          cell.survivability = -M*moisModif - rad*2 + self.survivability

      cell.survivability= -M*moisModif + H*hunModif - rad*2 + self.survivability

  def spread(self,envH):
      time = 5
      H = envH - self.hunger
      int(time - H*5)
      self.time = time

"CHANGE THESE"
width = 10
height = 10
radiation = 0
stMutation = random.normalvariate(0,.05)
radius = 10
"CHANGE THESE"

# Simulation settings
generations = 10
num_cells = 10

# Create the cells in the simulation
cells = [Cell(0,0.5,1,width//2,height//2,0.5)]

def get_cell_mutation():
    return (stMutation*2*radiation + stMutation,
            stMutation*2*radiation + stMutation,
            stMutation*2*radiation + stMutation)

def alterCells():
    mutated = []
    for cell in cells:
        mutated.append(Cell(get_cell_mutation,cell.x,cell.y,cell.survivability))

    for cell in mutated:
        R,G,B = 'GetRGB(image)'
        cell.live(R,G,B,radiation)
        if cell.survivability > 0:
            cell.spread()
            survived.append(cell)
    cells = survived

def movePossible(x,y):
    randomStart = random.randint(0,360)
    for i in range(randomStart,randomStart+360,10):
        radians = i*math.pi/180
        newX = radius*2*math.cos(radians) + x
        newY = radius*2*math.sin(radians) + y
        collide = False
        for cell in cells:
            if ((newX-cell.x)**2 + (newY - cell.y)**2)**0.5 < 2*radius:
                collide = True
                break
        if collide == False:
            return newX,newY

    return False

def newCells():
    for cell in cells:
        cell.counter += 1
        if cell.counter == cell.time:
            cell.counter = 0
            if movePossible(cell.x,cell.y) == False:
                continue
            else:
                newX, newY = movePossible(cell.x,cell.y)
            new = Cell(get_cell_mutation,newX,newY,cell.survivability)
            R,G,B = 'GetRGB(image)'
            new.live(R,G,B,radiation)
            if new.survivability > 0:
                new.spread()
                cells.append(new)
