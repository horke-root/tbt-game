import pyxel
from pyparsing import Word, alphas, nums
#from Sound import *
from Objects import *
from World import World
from Grid import Grid

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
                try:
                    self.world.queue[2] = []
                except KeyError:
                    self.world.queue.update({2: []})
                self.world.queue[2].append(Action(self.ShowHiddenText, (0,)))
                self.world.queue[2].append(Action(self.ShowHiddenText, (0,)))
                self.world.hidden_text = "NOT FOUND"
                self.world.queue[2].append(Action(self.HideHiddenText, (0,)))


class Settings:
    ticks: int = 30



class App:

    ash = ">"
    g: Grid
    world: World
    tick: int = 0
    settings: Settings
    sx = 1
    sy = 1
    cml: str = ""
    cursorcol : int = 5
    cursorstats: str = ""



    def cursor_changed(self):
        self.cursorstats = ""

        if self.world.sx > 10:
            self.world.offsetX += 1
            self.sx -= 1
        if self.world.sx < 0:
            self.world.offsetX -= 1
            self.sx += 1
        if self.world.sy > 10:
            self.world.offsetY += 1
            self.sy -= 1
        if self.world.sy < 0:
            self.world.offsetY -= 1
            self.sy += 1

        for o in self.world.objects:
            #print(f"{o.name}: {o.__dict__}")

            if o.x == self.sx+self.world.offsetX:
                if o.y == self.sy+self.world.offsetY:
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
        print(self.world.queue)
        for k, m in self.world.queue.items():
            print(m)
            try:
                args = m[0].argc
                m[0].func(*args)
                m.pop(0)
            except IndexError:
                pass
        try:
            for iQ in self.world.infinityQueue:
                args = iQ.argc
                iQ.func(*args)
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
        self.world.addObject(Tree(3,8, self.world))
        self.world.addObject(Zombie(2, 11, self.world))
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

        pyxel.init(int(160*1.2), int(120*1.2), title="Hello Pyxel")
        self.worldinit()
        self.g = Grid(10, 10, self.world, 3)
        pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.sounds[0].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "t",
            "6",
            "vffn fnff vffs vfnn",
            100,
        )
        pyxel.sounds[1].set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
            "p",
            "6",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            80,
        )

        self.sS = StepSound(self.world, 2)
        print(self.sS.snd)

        pyxel.play(0, [0, 1], loop=True)
        pyxel.run(self.update, self.draw)
        self.frame = pyxel.frame_count


    def update(self):
        self.world.sx = self.sx
        self.world.sy = self.sy
        if (self.frame - pyxel.frame_count) < -(self.settings.ticks):
            self.frame = pyxel.frame_count
            Thread(target=self.tick_func).run()
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
        pyxel.text(115, 0, f"x:{self.sx+self.world.offsetX} y:{self.sy+self.world.offsetY}", 3)
        pyxel.text(115, 5, f"tick: {self.tick}",3)
        def Ntext(x, y, text, col):
            ntext = text.split("\n")
            i=0
            print(ntext)
            for t in ntext:
                i += 1
                pyxel.text(x, y+(5*i), t, col)

        pyxel.text(115, 15, self.cursorstats, 3)
        pyxel.text(0,135, self.ash, 3)

        if self.world.show_hiddentext:
            pyxel.text(5,135,self.world.hidden_text, 13)

        pyxel.text(5, 135, self.cml, 3)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)
        #pyxel.line(0, 0, 0, 120, 3)
        #pyxel.line(10, 0, 10, 120, 3)
        #b1.drawblock()
        #b2.drawblock()
        self.g.draw()

        #self.world.GetPlayer().draw(self.g)
        self.world.drawAll(self.g)
        self.g.drawingrid(self.sx+self.world.offsetX, self.sy+self.world.offsetY, self.cursorcol)



if __name__ == "__main__":
    App()
