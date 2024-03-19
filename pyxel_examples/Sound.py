import pyxel
#from World import World
class Sound:
    world = None
    notes = "d"
    tones = "n"
    volumes = "7"
    effects = "f"
    speed = 25
    snd : int
    do_loop = False
    def _sound_creator(self, snd=None):
        if snd == None:
            snd = len(self.world.sounds) + 1
        else:
            pass
        pyxel.sounds[snd].set(
            str(self.notes),
            str(self.tones),
            str(self.volumes),
            str(self.effects),
            self.speed
        )
        self.snd = snd
    def play(self, ch=0):
        pyxel.play(ch, self.snd, loop=self.do_loop)
    def __init__(self, world, snd = None):
        self.world = world
        self._sound_creator(snd)

class StepSound(Sound):
    notes = "f0"
    tones = "n"
    effects = "f"

