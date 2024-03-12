import pyxel
from pyparsing import Word, alphas
import keyboard
class CommandLine:
    commands: dict = {}
    def __init__(self):
        pass
    def Parse(self, str) -> tuple:
        pp=str
        try:
            pp = Word(alphas) + " " + Word(alphas+" ")
            pp = pp.parseString(str)
        except:
            pass
        return (pp[0], pp[1])
    def AddCommand(self, name, func):
        self.commands.update({name: func})
    def ExecCommand(self, name, argc):
        try:
            self.commands[name.upper()](argc)
        except KeyError:
            self.commands[name.lower()](argc)



class Block:
    x1: int = 0
    y1: int = 0
    x2: int = 10
    y2: int = 10
    clr: int = 3
    def __init__(self, x1, y1, x2, y2, clr):
        self.x1 = x1
        self.x2 = x2
        self.y2 = y2
        self.y1 = y1
        self.clr = clr
    def drawblock(self):
        pyxel.line(self.x1, self.y1, self.x2, self.y1, self.clr)
        pyxel.line(self.x1, self.y1, self.x1, self.y2, self.clr)
        pyxel.line(self.x1, self.y2, self.x2, self.y2, self.clr)
        pyxel.line(self.x2, self.y2, self.x2, self.y1, self.clr)

b1 = Block(0,0,10,10,3)
b2 = Block(0, 0 , 10 , 30 ,3)

class Object:
    name = "Object"
    col: int = 5
    y: int
    x: int
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, grid):
        grid.drawingrid(self.x, self.y, self.col)
    def down(self, argc):
        self.y += 1



class Player(Object):
    name = "Player"
    col: int = 8
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
class World:
    objects: list = []
    w: int
    h: int
    def __init__(self, width, height):
        self.w = width
        self.h = height
    def addObject(self, obj: Object):
        self.objects.append(obj)
    def GetPlayer(self) ->  Player:
        player_exist = False
        pobj: Player
        for obj in self.objects:
            if obj.name == "Player":
                player_exist = True
                pobj = obj
        if player_exist == False:
            print("Player not in the World")
        return pobj
    def GetPlayerPosition(self) -> (int , int):
        pobj = self.GetPlayer()
        return (pobj.x, pobj.y)
    def GetPlayerHealth(self)-> int:
        pobj = self.GetPlayer()
        return pobj.hp
    def drawAll(self, grid):
        for obj in self.objects:
            obj.draw(grid)



class Stone(Object):
    name = "Stone"
    col = 13



class Grid:
    grid_size: int
    grid_count: int
    clr: int
    def __init__(self, grid_size, grid_count, clr):
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.clr = clr
    def drawingrid(self, sx, sy, clr):
        pyxel.rect(sx*self.grid_size+1,sy*self.grid_size+1,self.grid_size-1, self.grid_size-1, clr)
    def draw(self):
        for a in range(0, self.grid_count+1):
            pyxel.line(0,0+(self.grid_size * a), (self.grid_count * self.grid_size),0+(self.grid_size * a), self.clr)
        for a in range(0, self.grid_count+1):
            pyxel.line((self.grid_size * a),0, 0+(self.grid_size * a) ,(self.grid_count * self.grid_size), self.clr)

class Settings:
    ticks: int = 30



class App:
    g: Grid
    world: World
    tick: int = 0
    settings: Settings
    sx = 0
    sy = 0
    cml: str = ""
    cursorcol : int = 5
    cursorstats: str = ""
    def cursor_changed(self):
        for o in self.world.objects:
            if o.x == self.sx:
                if o.y == self.sy:
                    self.cursorstats = o.name+"\n"
                    for x,y in o.__dict__.items():
                        self.cursorstats += f"{x}: {y}\n"
                else:
                    self.cursorstats = ""
            else:
                self.cursorstats = ""
                    #p = Player(0,0,100)
                    #p.

    def tick_func(self):

        self.cursor_changed()

        if self.cursorcol == 3:
            self.cursorcol = 5
        else:
            self.cursorcol = 3


    def worldinit(self):
        self.world = World(100, 100)
        self.world.addObject(Player(0,0, 100))
        self.world.addObject(Stone(4, 6))
        self.settings = Settings()
        self.cmdl = CommandLine()
        self.cmdl.AddCommand("down", self.world.GetPlayer().down)
        global alphaslower
        alphaslower = [char for char in alphas if char.isupper()]
        print(alphaslower)
        self.frame = 0
    def __init__(self):
        self.g = Grid(10, 10, 3)
        self.worldinit()
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)
        self.frame = pyxel.frame_count

    def update(self):

        if (self.frame - pyxel.frame_count) < -(self.settings.ticks):
            self.frame = pyxel.frame_count
            self.tick_func()
            self.tick += 1

        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.sx += 1
            self.cursor_changed()
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.sx -= 1
            self.cursor_changed()
        elif pyxel.btnp(pyxel.KEY_UP):
            self.sy -= 1
            self.cursor_changed()
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.sy += 1
            self.cursor_changed()
        elif pyxel.btnr(pyxel.KEY_BACKSPACE):
            self.cml = self.cml[:-1]
        elif pyxel.btnr(pyxel.KEY_SPACE):
            self.cml += " "
        elif pyxel.btnr(pyxel.KEY_RETURN):
            self.cmdl.ExecCommand(self.cml, ())
            self.cml = ""
        else:
            for a in alphaslower:
                try:  # used try so that if user pressed other than the given key error will not be shown
                    if pyxel.btnr(eval(f"pyxel.KEY_{a}")):
                        print('You Pressed ' + a + ' Key!')
                        self.cml += a
                except:
                    break



    def draw(self):
        pyxel.cls(0)
        pyxel.text(110, 0, f"x:{self.sx} y:{self.sy}", 3)
        pyxel.text(110, 5, f"tick: {self.tick}",3)
        def Ntext(x, y, text, col):
            ntext = text.split("\n")
            i=0
            print(ntext)
            for t in ntext:
                i += 1
                pyxel.text(x, y+(5*i), t, col)

        pyxel.text(110, 15, self.cursorstats, 3)

        pyxel.text(5,105, self.cml, 3)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)
        #pyxel.line(0, 0, 0, 120, 3)
        #pyxel.line(10, 0, 10, 120, 3)
        #b1.drawblock()
        #b2.drawblock()
        self.g.draw()

        #self.world.GetPlayer().draw(self.g)
        self.world.drawAll(self.g)
        self.g.drawingrid(self.sx, self.sy, self.cursorcol)



if __name__ == "__main__":
    App()
