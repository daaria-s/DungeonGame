import pygame
from config import *
import config
from drawing import Drawing
from dungeon import Dungeon

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Magic Dungeon')
    screen = pygame.display.set_mode(SIZE)

    drawing = Drawing(screen)
    dungeon = Dungeon()
    clock = pygame.time.Clock()

    drawing.dungeon(dungeon)
    drawing.bottom_panel(dungeon, (0, 0))

    running = True
    while running:
        if not config.LOSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if config.TURN == 1:
                        dungeon.player_move(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        drawing.bottom_panel(dungeon, event.pos)

            if config.TURN == 2:
                dungeon.enemies_move()

            drawing.top_panel(dungeon)
            drawing.entities(dungeon)
            drawing.fps(clock)

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
