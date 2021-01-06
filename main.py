import pygame
from config import *
import config
from drawing import Drawing
from dungeon import Dungeon
from music import Music
import sys

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Magic Dungeon')
    screen = pygame.display.set_mode(SIZE)

    drawing = Drawing(screen)
    dungeon = Dungeon()
    clock = pygame.time.Clock()
    music = Music()

    drawing.bottom_panel(dungeon, (0, 0))

    running = True
    in_inventory = False
    while running:
        if not config.LOSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if config.TURN == 1 and not in_inventory:
                        dungeon.player_move(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not in_inventory:
                        drawing.bottom_panel(dungeon, event.pos)

                        # top panel buttons pressed
                        if 10 <= event.pos[1] <= 10 + PANEL_IMAGE_SIZE[1]:
                            if 450 <= event.pos[0] <= 450 + PANEL_IMAGE_SIZE[0]:  # inventory
                                drawing.inventory(dungeon)
                                in_inventory = True
                            if 500 <= event.pos[0] <= 500 + PANEL_IMAGE_SIZE[0]:  # save
                                print('SAVE')
                            if 550 <= event.pos[0] <= 550 + PANEL_IMAGE_SIZE[0]:  # exit
                                sys.exit(1)
                    elif event.button == 1 and in_inventory:
                        if event.pos[0] < 100 or event.pos[0] > 500 or event.pos[1] < 100 or event.pos[1] > 500:
                            in_inventory = False
                            screen.fill(BLACK)
                            drawing.dungeon(dungeon)
                            drawing.bottom_panel(dungeon, (0, 0))
            if in_inventory:
                pass
            else:
                if config.TURN == 2:
                    dungeon.enemies_move()

                drawing.top_panel(dungeon)
                drawing.dungeon(dungeon)

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
