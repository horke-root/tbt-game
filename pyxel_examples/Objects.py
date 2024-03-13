from threading import Thread
class Action:
    func = None
    argc = tuple
    def __init__(self, func, argc):
        self.func = func
        self.argc = argc

class Object:
    name = "Object"
    world = None
    col: int = 5
    y: int
    x: int
    bordercol: int = 0
    border: bool = False
    secondBorder: bool = False
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
    def draw(self, grid):
        grid.drawingrid(self.x, self.y, self.col)
        if self.border == True:
            grid.drawingridborder(self.x, self.y, self.bordercol)
        if self.secondBorder == True:
            grid.secondborder(self.x, self.y, self.bordercol)
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
    def _move_to(self, x ,y):
        offsetX = x - self.x
        offsetY = y - self.y
        print(offsetX)
        print(offsetY)
        if offsetX < 0:
            for a in range(0, -offsetX):
                self.world.queue.append(Action(self.left, (0,)))
        if offsetX > 0:
            for a in range(0, offsetX):
                self.world.queue.append(Action(self.right, (0,)))
        if offsetY < 0:
            for a in range(0, -offsetY):
                self.world.queue.append(Action(self.up, (0,)))
        if offsetY > 0:
            for a in range(0, offsetY):
                self.world.queue.append(Action(self.down, (0,)))
        for q in self.world.queue:
            print(q.func)
    def move_to(self, *argc):
        print(argc)
        if argc[0].lower() == "cursor":
            self._move_to(self.world.sx, self.world.sy)
        else:
            rx=int(argc[0])
            ry=int(argc[1])
            print (f"moveto : {rx}, {ry}")
            self._move_to(rx, ry)

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
