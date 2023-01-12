
# connection
gameEngine = None

tcpConn = None
connector = None

gameState = 0

Blocks = []
NewBlock = []

# input
inpDIR_UP = False
inpDIR_DOWN = False
inpDIR_LEFT = False
inpDIR_RIGHT = False
inpSHIFT = False
inpCTRL = False

# pygame
height = 1600
width = 900
background_menu = "./src/assets/background_menu.png"
background_game = "./src/assets/background_game.png"
square = "./src/assets/Game_Assets/R/R.png"
Sshape = "./src/assets/Game_Assets/S/S.png"
Lshape = "./src/assets/Game_Assets/L/L.png"
Tshape = "./src/assets/Game_Assets/T/T_2.png"
IShape = "./src/assets/Game_Assets/I/1.png"
