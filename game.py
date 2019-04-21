import pygame

import argparser

import lib
import ai.neatinterface.neatcore

pygame.init()

if __name__ == "__main__":
    args = argparser.get_args()

    # pygame initialization
    pygame.init()

    # initialize properly and make links make them as common resources
    # for other modules
    # I admit this looks pretty hideous but python has no good way of
    # handling singletons
    lib.common.settings = settings = lib.Settings(args)
    lib.common.display = display = lib.Display()
    lib.common.clock = clock = lib.Clock()
    lib.common.events = events = lib.Events()

    # setting game mode
    if args.ai == "neat":
        lib.common.core = core = ai.neatinterface.neatcore.NeatCore()
    else:
        lib.common.core = core = lib.Core()

    core.new_game()

    # main loop
    while True:
        clock.tick()
        core.update()

        if core.game_over():
            core.new_game()
            continue

        display.draw(core.get_surface())
