from music import Music
import sqlite3

WIDTH, HEIGHT = SIZE = 600, 600
FPS = 60
TILE = 50
LOSE = False
PANEL_IMAGE_SIZE = (30, 30)
INVENTORY_IMAGE_SIZE = (50, 50)
INVENTORY_INDENT = 25
PANEL_HEIGHT = 50
DESCRIPTION_POSITION = (
    100 + INVENTORY_INDENT, 100 + 2 * INVENTORY_INDENT + 4 * (
            INVENTORY_INDENT + INVENTORY_IMAGE_SIZE[0]))

# colors
BLACK = (0, 0, 0)
HP_COLOR = (32, 192, 32)
DAMAGE_COLOR = (192, 32, 32)
ACTION_POINTS_COLOR = (32, 32, 192)
PANEL_COLOR = (64, 64, 64)
DESCRIPTION_COLOR = (192, 192, 192)

music = Music()


def users():
    con = sqlite3.connect('dungeonBase.db')
    cur = con.cursor()
    users_ = list(map(lambda x: x[0], cur.execute(
        """SELECT user_name FROM users""").fetchall()))
    con.close()
    return users_


N, MAX_N = 0, len(users())
USER_NAME = users()[N] if users() else None
INPUT_USER = ''
