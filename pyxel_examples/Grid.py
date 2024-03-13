import pyxel
import World
class Grid:
    grid_size: int
    grid_count: int
    clr: int
    world: World
    def __init__(self, grid_size, grid_count, world: World,clr):
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.clr = clr
        self.world = world
    def secondborder(self, sx, sy, clr):
        sx = sx - self.world.offsetX
        sy = sy - self.world.offsetY
        pyxel.rectb(sx * self.grid_size + 2, sy * self.grid_size + 2, self.grid_size - 3, self.grid_size - 3, clr)

    def drawingridborder(self, sx, sy, clr):
        sx = sx - self.world.offsetX
        sy = sy - self.world.offsetY
        pyxel.rectb(sx * self.grid_size + 1, sy * self.grid_size + 1, self.grid_size - 1, self.grid_size - 1, clr)

    def drawingrid(self, sx, sy, clr):
        sx = sx - self.world.offsetX
        sy = sy - self.world.offsetY
        pyxel.rect(sx*self.grid_size+1,sy*self.grid_size+1,self.grid_size-1, self.grid_size-1, clr)
    def drawLetter(self, sx, sy, letter:str, clr):
        sx = sx - self.world.offsetX
        sy = sy - self.world.offsetY
        pyxel.text(sx*self.grid_size+4, sy*self.grid_size+3,letter, clr)
    def draw(self):
        for a in range(0, self.grid_count+2):
            pyxel.line(0, (self.grid_size * a), (self.grid_count* self.grid_size)+10, (self.grid_size * a), self.clr)
        for a in range(0, self.grid_count+2):
            pyxel.line((self.grid_size * a),0, (self.grid_size * a), (self.grid_count * self.grid_size)+10, self.clr)
