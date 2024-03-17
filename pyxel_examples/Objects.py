from threading import Thread
from abc import abstractmethod, ABC
class Action:
    func = None
    argc = tuple
    name = "Null"
    layer = 0
    def __init__(self, func, argc, name="Null"):
        self.func = func
        self.argc = argc
        self.name = name
class Object:
    letter: str = "o"
    letterColor: int = 0
    showLetter: bool = False
    name = "Object"
    world = None
    col: int = 5
    y: int
    x: int
    bordercol: int = 0
    border: bool = False
    secondBorder: bool = False
    @abstractmethod
    def onStart(self): #Start after spawning
        pass
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world

        self.onStart() # Start Abstract Mehthod onStart()
    def draw(self, grid):
        grid.drawingrid(self.x, self.y, self.col)
        if self.border == True:
            grid.drawingridborder(self.x, self.y, self.bordercol)
        if self.secondBorder == True:
            grid.secondborder(self.x, self.y, self.bordercol)
        if self.showLetter == True:
            grid.drawLetter(self.x, self.y, self.letter, self.letterColor)
    def down(self, argc):
        self.y += 1
class Entity(Object):
    name = "Entity"
    def down(self, argc):
        self.y += 1
    def up(self, argc):
        self.y -= 1
    def right(self, argc):
        self.x += 1
    def left(self, argc):
        self.x -= 1

    def _move_to(self, x ,y, layer: int = 0):
        offsetX = x - self.x + self.world.offsetX
        offsetY = y - self.y + self.world.offsetY
        print(offsetX)
        print(offsetY)

        if offsetX < 0:
            for a in range(0, -offsetX):
                self.world.queue[layer].append(Action(self.left, (0,), self.name))
        if offsetX > 0:
            for a in range(0, offsetX):
                self.world.queue[layer].append(Action(self.right, (0,), self.name))
        if offsetY < 0:
            for a in range(0, -offsetY):
                self.world.queue[layer].append(Action(self.up, (0,), self.name))
        if offsetY > 0:
            for a in range(0, offsetY):
                self.world.queue[layer].append(Action(self.down, (0,), self.name))
        for q in self.world.queue[layer]:
            print(q.func)
    def move_to(self, *argc):
        print(argc)
        try:
            if argc[0].lower() == "cursor":
                self._move_to(self.world.sx, self.world.sy, layer=0)
            else:
                rx=int(argc[0])
                ry=int(argc[1])
                print (f"moveto : {rx}, {ry}")
                self._move_to(rx, ry, layer=0)
        except:
            self._move_to(self.world.sx, self.world.sy, layer=0)
            """if argc[0].lower() == "cursor":
            def moveFunc(r, d, world):
                si = 0
                for i in range(0,r):
                    if world.tick:
                        if i!=0 and si==0:
                            si = i
                        self.x += si
                        world.tick = False
                sl = 0

                for l in range(0,d):
                    if world.tick:
                        if l!=0 and sl==0:
                            sl = l
                        self.y += sl
                        world.tick = False
            self.world.threads.append(Thread(moveFunc, (self.world.sx - self.x, self.world.sy - self.y, self.world)).run())
"""
class Player(Entity):
    name = "Player"
    showLetter = True
    letter = "P"
    col: int = 8
    def __init__(self, x, y, hp, world):
        self.x = x
        self.y = y
        self.hp = hp
        self.border = True
        self.secondBorder = True
        self.world = world

class Stone(Object):
    name = "Stone"
    col = 13

class Tree(Object):
    name = "Tree"
    col = 11
    border = True

class Zombie(Entity):

    name = "Zombie"
    col=11
    border = True
    secondBorder = True
    letter = "Z"
    showLetter = True
    def doActionUntilPlayerTouch(self):
        print("duActionUntilPlayerTouch" + str(self))
        self.world.DeleteAllActionByName("Zombie", 1)
        if self.world.GetPlayerPosition() == (self.x, self.y):
            self.world.DeleteAllInfinityActionByName("UntilZombieTouchPlayer")
        else:
            print("Uahh..Behh...")
            self._move_to(*self.world.GetPlayerPosition(), layer=1)
    def onStart(self):
        print("Zombie Has Spawned")
        #self._move_to(*self.world.GetPlayerPosition(), layer=1)
        self.world.queue[1].append(Action(self.doActionUntilPlayerTouch, ()))

