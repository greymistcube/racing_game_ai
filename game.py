import pygame

import argparser

import lib
import neatinterface

pygame.init()

if __name__ == "__main__":
    args = argparser.get_args()

    # pygame initialization
    pygame.init()

    settings = lib.Settings(args)
    display = lib.Display(args)
    clock = lib.Clock()

    if args.ai == "neat":
        core = neatinterface.NeatCore()
    else:
        core = lib.Core()
    core.new_game()

    # main loop
    while True:
        clock.tick()
        core.update()

        if core.game_over():
            core.new_game()
            continue

        display.draw(core.get_surface())
