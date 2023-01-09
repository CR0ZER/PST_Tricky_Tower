
# version constants
CLIENT_MAJOR = 0
CLIENT_MINOR = 0
CLIENT_REVISION = 0


GAME_NAME = "Template"  # the game name
GAME_PORT = 2727      # the game port

# the maximum amount of (online) players allowed in the game
MAX_PLAYERS = 4


class textColor():
    BLACK = (0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE = (0,   0, 255)
    GREEN = (0, 255,   0)
    RED = (255,   0,   0)
    CYAN = (0, 255, 255)
    YELLOW = (255, 255,   0)
    GREY = (128, 128, 128)
    PINK = (255,   0, 255)
    BROWN = (153,  76,   0)

    BRIGHT_RED = (255,  51,  51)
    BRIGHT_GREEN = (128, 255,   0)
    BRIGHT_BLUE = (0, 128, 255)
    BRIGHT_CYAN = (0, 255, 128)

    DARK_GREY = (96,  96,  96)
    DARK_CYAN = (0, 204, 204)


sayColor = textColor.GREY
globalColor = textColor.BRIGHT_BLUE
broadcastColor = textColor.PINK
tellColor = textColor.BRIGHT_GREEN
emoteColor = textColor.BRIGHT_CYAN
adminColor = textColor.BRIGHT_CYAN
helpColor = textColor.PINK
whoColor = textColor.PINK
joinLeftColor = textColor.DARK_GREY
npcColor = textColor.BROWN
alertColor = textColor.RED
newMapColor = textColor.PINK

# direction constants
DIR_UP = 0
DIR_LEFT = 1
DIR_DOWN = 2
DIR_RIGHT = 3
