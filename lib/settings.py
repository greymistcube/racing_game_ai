import lib.constants as const
import lib.common as common

class Settings:
    __instance = None

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            raise Exception("only single instance is allowed")

    def __init__(self, args=None):
        self.info = True
        self.debug = False
        if args is not None:
            self.tickrate = const.TICKRATE
            self.num_cars = args.n
            self.display_size = (
                const.WIDTH * args.z, const.HEIGHT * args.z
            )
        return

    def update(self):
        self.tickrate = const.TICKRATE * common.events.multiplier
        if common.events.info:
            self.info = not self.info
        if common.events.debug:
            self.debug = not self.debug
        return
