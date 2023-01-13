
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

Rshape = "./src/assets/Game_Assets/R.png"
Sshape = "./src/assets/Game_Assets/S.png"
S2shape = "./src/assets/Game_Assets/S_2.png"
Lshape = "./src/assets/Game_Assets/L.png"
L2shape = "./src/assets/Game_Assets/L_2.png"
Tshape = "./src/assets/Game_Assets/T.png"
Ishape = "./src/assets/Game_Assets/I.png"

IMGRshape = None
IMGSshape = None
IMGS2shape = None
IMGLshape = None
IMGL2shape = None
IMGTshape = None
IMGIshape = None
