import pyxel
from pyparsing import Word, alphas, nums

from Objects import *
from World import World


class CommandLine:
    commands: dict = {}
    world: World
    def ShowHiddenText(self, argc):
        self.world.show_hiddentext = True

    def HideHiddenText(self, argc):
        self.world.show_hiddentext = False
    def __init__(self, world: World):
        self.world = world
    def Parse(self, str) -> tuple:
        pp=str.split(" ")

        """pp = Word(alphas) + " " + Word(alphas)
        pp = pp.parseString(str)"""
        print(pp)
        return (pp[0], tuple(pp[1:]))
    def AddCommand(self, name, func):
        self.commands.update({name: func})
    def ExecCommand(self, name, argc):
        print(f"{name}: {argc}")
        try:
            self.commands[name.upper()](*argc)
        except KeyError:
            try:
                self.commands[name.lower()](*argc)
            except KeyError:
                self.world.queue.append(Action(self.ShowHiddenText, (0,)))
                self.world.queue.append(Action(self.ShowHiddenText, (0,)))
                self.world.hidden_text = "NOT FOUND"
                self.world.queue.append(Action(self.HideHiddenText, (0,)))




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


class Grid:
    grid_size: int
    grid_count: int
    clr: int
    def __init__(self, grid_size, grid_count, clr):
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.clr = clr
    def secondborder(self, sx, sy, clr):
        pyxel.rectb(sx * self.grid_size + 2, sy * self.grid_size + 2, self.grid_size - 3, self.grid_size - 3, clr)

    def drawingridborder(self, sx, sy, clr):
        pyxel.rectb(sx * self.grid_size + 1, sy * self.grid_size + 1, self.grid_size - 1, self.grid_size - 1, clr)

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
    ash = ">"
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
        self.cursorstats = ""
        for o in self.world.objects:
            #print(f"{o.name}: {o.__dict__}")

            if o.x == self.sx:
                if o.y == self.sy:
                    self.cursorstats = o.name+"\n"
                    for s,t in o.__dict__.items():
                        self.cursorstats += f"{s}: {t}\n"
                else:
                    pass
            else:
                pass
                #self.cursorstats = ""
                #self.cursorstats = ""
                    #p = Player(0,0,100)
                    #p.
    def halftick_func(self):
        if self.ash == ">":
            self.ash = ""
        else:
            self.ash = ">"
    def tick_func(self):
        try:
            args = self.world.queue[0].argc
            self.world.queue[0].func(*args)
            self.world.queue.pop(0)
        except:
            pass
            #print("not have in queue")
        self.world.tick = True
        self.cursor_changed()



        if self.cursorcol == 3:
            self.cursorcol = 5
        else:
            self.cursorcol = 3


    def worldinit(self):
        self.world = World(100, 100)
        self.world.addObject(Player(0,0, 100, self.world))
        self.world.addObject(Stone(4, 6, self.world))
        self.settings = Settings()
        self.cmdl = CommandLine(self.world)
        self.cmdl.AddCommand("down", self.world.GetPlayer().down)
        self.cmdl.AddCommand("moveto", self.world.GetPlayer().move_to)
        global alphaslower
        alphaslower = [char for char in alphas if char.isupper()]
        alphaslower = alphaslower
        print(alphaslower)
        self.frame = 0
        self.halfframe = 0
    def __init__(self):
        self.g = Grid(10, 10, 3)
        self.worldinit()
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)
        self.frame = pyxel.frame_count

    def update(self):
        self.world.sx = self.sx
        self.world.sy = self.sy
        if (self.frame - pyxel.frame_count) < -(self.settings.ticks):
            self.frame = pyxel.frame_count
            self.tick_func()
            self.tick += 1
        if (self.halfframe - pyxel.frame_count) < -int((self.settings.ticks * 0.5)):
            self.halfframe = pyxel.frame_count
            self.halftick_func()

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
            self.cmdl.ExecCommand(*self.cmdl.Parse(self.cml))
            self.cml = ""
        else:
            for a in alphaslower+list(str(nums)):
                try:  # used try so that if user pressed other than the given key error will not be shown
                    if pyxel.btnr(eval(f"pyxel.KEY_{str(a)}")):
                        #print('You Pressed ' + a + ' Key!')
                        self.cml += str(a)
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
        pyxel.text(0,105, self.ash, 3)

        if self.world.show_hiddentext:
            pyxel.text(5,105,self.world.hidden_text, 13)

        pyxel.text(5, 105, self.cml, 3)
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
