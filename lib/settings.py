from lib.constants import TICKRATE

class Settings:
    __instance = None

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    # this should be called at least once with args in main.py
    def __init__(self, args=None):
        self.info = True
        self.debug = False
        if args is not None:
            self.tickrate = TICKRATE
            self.num_cars = args.n
        return

    def update(self, events):
        self.tickrate = TICKRATE * events.multiplier
        if events.info:
            self.info = not self.info
        if events.debug:
            self.debug = not self.debug
        return
