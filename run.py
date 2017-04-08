import sys
import random

class Cell(pygame.sprite.Sprite):

  def __init__(self,resistance,moist,hunger,x,y):
      super(Cell,self(),__init__())
      self.resistance = resistance
      self.moist = moist
      self.hunger = hunger
      self.survivability = 0.5
      self.x = x
      self.y = y


  def live(self, envR, envM, envH, rad):
      R = self.resistance - envR
      H = envH - self.hunger
      M = abs(envM - self.moist)
      if R <= 0:
          return -1

      moisModif = 1
      hunModif = 1

      if H > 0:
          return -M*moisModif - rad*2 + self.survivability

      return -M*moisModif + H*hunModif - rad*2 + self.survivability

  def spread(self,envH):
      time = 5
      H = envH - self.hunger
      int(time - H*5)

"CHANGE THESE"
width = 10
height = 10
radiation = 0
stMutation = random.normalvariate(0,.05)
"CHANGE THESE"

# Simulation settings
generations = 10
num_cells = 10

# Create the cells in the simulation
cells = [Cell(0,0.5,1,width//2,height//2)]


def get_cell_mutation():
  return (stMutation*2*radiation + stMutation,
          stMutation*2*radiation + stMutation,
          stMutation*2*radiation + stMutation)


  # Life!
  for cell in cells:
    cell.live(environment_modifier)

  # Death!
  # Survivability < 0 will die
  survived_cells = []
  for cell in cells:
    if cell.survivability > 0:
      survived_cells.append(cell)

  if len(survived_cells) == 0:
    print("\n\033[91mAll cells died in generation " + str(i) + "\033[0m")
    sys.exit()

  # Intermediate results
  cells = sorted(cells, key=lambda cell: cell.survivability)
  print("Cells that survived this gen: " + str(len(survived_cells)) + "\n")

  # Reproduction: each surviving cell will split into two new cells,
  # each with the parent's fitness + a random mutation value
  cells = []
  for survived in survived_cells:
    cells.append(Cell(cell.fitness + get_cell_mutation()))
    cells.append(Cell(cell.fitness + get_cell_mutation()))

print("\033[92mSuccess\033[0m")
