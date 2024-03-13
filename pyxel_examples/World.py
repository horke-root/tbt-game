from Objects import Object, Player, Stone
class World:
    queue: list = []
    objects: list = []
    threads: list = []

    hidden_text = "NOT FOUND"
    show_hiddentext = False

    w: int
    sx = 0
    sy = 0
    h: int
    tick = False
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
