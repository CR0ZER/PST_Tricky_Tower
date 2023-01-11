from pickle import TRUE
import time
import os.path as path
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.pygame_util import from_pygame, to_pygame
import pymunk.autogeometry
import pygame_menu
from pygame.locals import *

from twisted.internet import reactor

from network import *
from constants import *
import global_vars as g


class Engine:
    def __init__(self):
        self.FRAMES_PER_SECOND = 20

        # menus

        self.tmr25 = 0
        self.tmr1000 = 0
        self.walkTimer = 0
        self.clockTick = 0

        self.draw_options = None
        self.screen = None
        self.clock = None
        self.space = None
        self.nbPlayer = 1
        self.shape = None
        self.menu = None

    def changeState(self):
        g.gameState = 1
    
    def init(self):

        # self.initConfig(g.dataPath + '/config.cfg')
        g.gameEngine.initConnection()

        # pygame init
        pygame.init()
        self.screen = pygame.display.set_mode((g.height, g.width))
        self.clock = pygame.time.Clock()

        # pygame physics
        self.space = pymunk.Space()
        self.mass = 1
        self.size = (50, 50)
        self.moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.space.add(self.body, self.shape)
        self.force = pymunk.Vec2d(0, 30)

        # pygame plateforme
        def static_rect(space, x, y, r_width, r_height):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = x, y
            shape = pymunk.Poly.create_box(body, (r_width, r_height))
            space.add(body, shape)

        static_rect(self.space, 600, 900, 200, 400)
        static_rect(self.space, 1000, 900, 200, 400)

        # pygame menu
        theme_background_image = pygame_menu.themes.THEME_DARK.copy()
        #theme_background_image.background_color = pygame_menu.BaseImage(image_path="src/assets/background_menu.png")
        theme_background_image.background_color = pygame_menu.BaseImage(image_path="./assets/background_menu.png")

        menu1 = pygame_menu.Menu(
            'Tricky Tower', g.height, g.width, theme=theme_background_image)
        menu1.add.vertical_margin(200)
        menu1.add.button('Jouer', action=self.changeState, font_color=(255, 255, 255))
        menu1.add.button('Quitter', pygame_menu.events.EXIT, font_color=(255, 255, 255))
        self.menu = menu1

        self.gameLoop()
        reactor.run()

    def initConnection(self):
        """starts the connection to the server"""
        connectionProtocol = startConnection()
        g.tcpConn = TCPConnection(connectionProtocol)

    def initConfig(self, configFile):
        """reads the configuration file"""
        log("can read config.cfg file here")

    def disconnect(self):
        g.connector.disconnect()

    def setState(self, state):
        """sets the game state"""
        if state == MENU_LOGIN:
            g.gameState = MENU_LOGIN

        elif state == MENU_REGISTER:
            g.gameState = MENU_REGISTER

        elif state == MENU_CHAR:
            g.gameState = MENU_CHAR

        elif state == MENU_NEWCHAR:
            g.gameState = MENU_NEWCHAR

        elif state == MENU_INGAME:
            g.gameState = MENU_INGAME


    class Sprite(pygame.sprite.Sprite):
        def __init__(self, x, y, size):
            super().__init__()

            self.image = pygame.Surface([size, size])
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


    def gameLoop(self, FPS=60):
        """the main loop of the game"""
        # TODO: DIRTY AREAS

        for b in g.Blocks:
            log(f"position : " + str(b[1].x) + " ; " + str(b[1].y))
            self.posX = b[0].x
            self.posY = b[0].y - 1000
            log(f"position : " + str(self.posX) + " ; " + str(self.posY))
            # TODO cr�er uns structure pour les rectangles re�u
            #  b[0].x et b[0].y position physique du carr�
            #  b[1].x et b[1].y vecteur rotation du carr�
        
        if g.gameState == MENU_LOGIN:
            self.menu.mainloop(self.screen, disable_loop=True)

        elif g.gameState == MENU_REGISTER:
            self.screen.fill(pygame.Color("white"))
            self.sprite = self.Sprite(self.posX, self.posY, 50)
            self.sprite_group = pygame.sprite.Group()
            self.sprite_group.add(self.sprite)
            self.sprite_group.draw(self.screen)
            pygame.display.update()

        elif g.gameState == MENU_CHAR:
            pass

        elif g.gameState == MENU_NEWCHAR:
            pass

        elif g.gameState == MENU_INGAME:
            # todo: dirty areas

            # self.graphicsEngine.renderGraphics()

            # flip graphics
            pygame.display.update()
            # pygame.display.update(self.graphicsEngine.dirtyRects)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quitGame()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.quitGame()

        self.space.step(1/50.0)
        
        # pygame.draw.rect(self.screen, (0, 0, 0), (1, 1))

        pygame.display.flip()
        self.clock.tick(self.FRAMES_PER_SECOND)

        # pygame.event.pump()
        # for event in pygame.event.get():
        #    # todo: organize this better...
        #    if g.gameState == MENU_LOGIN:
        #        pass
        #
        #    elif g.gameState == MENU_REGISTER:
        #        pass
        #
        #    elif g.gameState == MENU_CHAR:
        #        pass
        #
        #    elif g.gameState == MENU_NEWCHAR:
        #        pass
        #    elif g.gameState == MENU_INGAME:
        #        pass
        #
        #    if event.type == pygame.QUIT:
        #        reactor.stop()
        #        pygame.quit()
        #
        #    elif event.type == pygame.MOUSEMOTION:
        #        self.handleMouse(event)

        # make it loop
        reactor.callLater(1.0 / FPS, self.gameLoop)

    def quitGame(self):
        """called when quitting the game"""
        if g.tcpConn != None:
            # if connected to server, send quit msg
            g.tcpConn.sendQuit()

        reactor.stop()
        pygame.quit()

    ##################
    # INPUT SPECIFIC #
    #################

    def checkInputKeys(self):
        """checks for input events"""

        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_UP) or pressed(pygame.K_z):
            g.inpDIR_UP = True
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_DOWN) or pressed(pygame.K_s):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = True
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_LEFT) or pressed(pygame.K_q):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = True
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = True

        else:
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False
            g.inpSHIFT = False
            g.inpCTRL = False

    def handleMouse(self, event):
        g.cursorX = event.pos[0]
        g.cursorY = event.pos[1]

        # only set mouse tile position within game screen boundaries
        # if g.cursorX > 16 and g.cursorX < (16 + 15 * PIC_X):
        # g.cursorXTile = (g.cursorX - 16) // PIC_X
        ##
        # if g.cursorY > 16 and g.cursorY < (16 + 11 * PIC_Y):
        # g.cursorYTile = (g.cursorY - 16) // PIC_Y
