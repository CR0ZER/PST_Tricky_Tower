from pickle import TRUE
import time
import math
import pygame
import pygame_menu
from pygame.locals import *

from twisted.internet import reactor

from network import *
from constants import *
import global_vars as g


class Engine:
    def __init__(self):
        self.FRAMES_PER_SECOND = 50

        # menus

        self.tmr25 = 0
        self.tmr1000 = 0
        self.walkTimer = 0
        self.clockTick = 0

        self.draw_options = None
        self.screen = None
        self.clock = None
        self.space = None
        self.shape = None
        self.menu = None
        self.background = None

        self.sprite_group = pygame.sprite.Group()

    def changeState(self):
        reactor.callLater(1, self.sendPlayerPacket)
        log("boom2")
        g.gameState = 1

    def init(self):

        # self.initConfig(g.dataPath + '/config.cfg')

        # pygame init
        pygame.init()
        self.screen = pygame.display.set_mode((g.height, g.width))
        self.clock = pygame.time.Clock()
        self.size = (50, 50)
        self.background = pygame.Surface((g.width, g.height))

        # pygame menu
        theme_background_image = pygame_menu.themes.THEME_DARK.copy()
        theme_background_image.background_color = pygame_menu.BaseImage(
            image_path=g.background_menu)

        g.IMGTshape = pygame.image.load(g.Tshape).convert_alpha()
        g.IMGTshape = pygame.transform.scale(g.IMGTshape, (60, 60))
        g.IMGLshape = pygame.image.load(g.Lshape).convert_alpha()
        g.IMGLshape = pygame.transform.scale(g.IMGLshape, (60, 60))
        g.IMGL2shape = pygame.image.load(g.L2shape).convert_alpha()
        g.IMGL2shape = pygame.transform.scale(g.IMGL2shape, (60, 60))
        g.IMGRshape = pygame.image.load(g.Rshape).convert_alpha()
        g.IMGRshape = pygame.transform.scale(g.IMGRshape, (60, 60))
        g.IMGSshape = pygame.image.load(g.Sshape).convert_alpha()
        g.IMGSshape = pygame.transform.scale(g.IMGSshape, (60, 60))
        g.IMGS2shape = pygame.image.load(g.S2shape).convert_alpha()
        g.IMGS2shape = pygame.transform.scale(g.IMGS2shape, (60, 60))
        g.IMGIshape = pygame.image.load(g.Ishape).convert_alpha()
        g.IMGIshape = pygame.transform.scale(g.IMGIshape, (60, 60))
        g.IMGPlatform = pygame.image.load(g.Platform).convert_alpha()
        g.IMGPlatform = pygame.transform.scale(g.IMGPlatform, (75, 100))
        g.IMGflag = pygame.image.load(g.flag).convert_alpha()
        g.IMGflag = pygame.transform.scale(g.IMGflag, (1600, 20))

        menu2 = pygame_menu.Menu(
            'Tricky Tower', g.height, g.width, theme=theme_background_image)
        menu2.add.vertical_margin(200)
        menu2.add.label(title=f'Nombre de joueurs : {g.nbPlayers}', font_color=(
            255, 255, 255), font_name=g.font, font_size=50)
        menu2.add.vertical_margin(50)
        menu2.add.button('Prêt', self.changeState, font_color=(
            255, 255, 255), font_name=g.font, font_size=50)
        menu2.add.button('Retour', action=pygame_menu.events.BACK, font_color=(
            255, 255, 255), font_name=g.font, font_size=50)

        def connectAndUpdate():
                g.gameEngine.initConnection()
                link = menu1.add.menu_link(menu2)
                link.open()

        menu1 = pygame_menu.Menu(
            'Tricky Tower', g.height, g.width, theme=theme_background_image)
        menu1.add.vertical_margin(200)
        menu1.add.button('Jouer', action=connectAndUpdate, font_color=(
            255, 255, 255), font_name=g.font, font_size=50)
        menu1.add.button('The useless button', action=None, font_color=(
            255, 255, 255), font_name=g.font, font_size=50)
        menu1.add.button('Quitter', pygame_menu.events.EXIT, font_color=(
            255, 255, 255), font_name=g.font, font_size=50)
        self.menu = menu1

        self.gameLoop()
        reactor.run()

    def initConnection(self):
        """starts the connection to the server"""
        connectionProtocol = startConnection()
        g.tcpConn = TCPConnection(connectionProtocol)

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

    class TShape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGTshape.copy()
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class LShape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGLshape
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class L2Shape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGL2shape
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class RShape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGRshape
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class SShape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGSshape
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class S2Shape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGS2shape
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class IShape(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGIshape
            self.rect = self.image.get_rect()
            self.rect.center = (x-35, y-45)

    class Rectangle(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = g.IMGPlatform
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    def gameLoop(self, FPS=50):
        global clockTick
        clockTick = time.time()
        """the main loop of the game"""
        # TODO: DIRTY AREAS

        self.sprite_group.empty()
        posX = 0
        posY = 0
        for b in g.Blocks:
            # log("position : " + str(b[0].x) + " ; " + str(b[0].y) +
            #    "rotation : " + str(b[1].x) + " ; " + str(b[1].y))
            posX = b[0].x + 300
            posY = b[0].y + 125
            rotX = b[1].x
            rotY = b[1].y
            type = b[2]

            angle_rad = math.atan2(rotY, rotX)
            angle_deg = math.degrees(angle_rad)

            if type == 0:
                plateform = self.Rectangle(posX, posY)
                self.sprite_group.add(plateform)

            elif type == 1:
                shape = self.IShape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

            elif type == 2:
                shape = self.RShape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

            elif type == 3:
                shape = self.S2Shape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

            elif type == 4:
                shape = self.SShape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

            elif type == 5:
                shape = self.L2Shape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

            elif type == 6:
                shape = self.LShape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

            elif type == 7:
                shape = self.TShape(posX, posY)
                shape.image = pygame.transform.rotate(shape.image, -angle_deg)
                self.sprite_group.add(shape)

        if g.gameState == MENU_LOGIN:
            self.menu.mainloop(self.screen, disable_loop=True)

        elif g.gameState == MENU_REGISTER:
            self.screen.blit(pygame.image.load(g.background_game), (0, 0))
            self.screen.blit(g.IMGflag, (0, 400))
            self.sprite_group.draw(self.screen)

        elif g.gameState == MENU_CHAR:
            pygame.font.init()
            my_font = pygame.font.Font(g.font, 100)
            text_surface = my_font.render(f"Joueur {g.winner} a gagné !", True, pygame.color.Color("white"))
            text_rect = text_surface.get_rect()
            text_rect.center = (800, 450)
            self.screen.blit(pygame.image.load(g.background_game), (0, 0))
            self.screen.blit(text_surface, text_rect)
            pygame.display.update()
            self.disconnect()
            time.sleep(10)
            g.gameState = 0

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
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g.gameState = 0
                elif event.key == pygame.K_z or event.key == K_UP:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 1, "actived": True}])
                    g.tcpConn.sendData(packet)
                elif event.key == pygame.K_q or event.key == K_LEFT:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 2, "actived": True}])
                    g.tcpConn.sendData(packet)
                elif event.key == pygame.K_s or event.key == K_DOWN:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 3, "actived": True}])
                    g.tcpConn.sendData(packet)
                elif event.key == pygame.K_d or event.key == K_RIGHT:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 4, "actived": True}])
                    g.tcpConn.sendData(packet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z or event.key == K_UP:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 1, "actived": False}])
                    g.tcpConn.sendData(packet)
                elif event.key == pygame.K_q or event.key == K_LEFT:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 2, "actived": False}])
                    g.tcpConn.sendData(packet)
                elif event.key == pygame.K_s or event.key == K_DOWN:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 3, "actived": False}])
                    g.tcpConn.sendData(packet)
                elif event.key == pygame.K_d or event.key == K_RIGHT:
                    packet = json.dumps(
                        [{"packet": ClientPackets.CArrowKey, "key": 4, "actived": False}])
                    g.tcpConn.sendData(packet)

        # pygame.draw.rect(self.screen, (0, 0, 0), (1, 1))

        pygame.display.flip()
        # self.clock.tick(self.FRAMES_PER_SECOND)

        # make it loop
        t = time.time() - clockTick
        # log("tts :" + str(t))
        if (t > 0.02):
            reactor.callLater(0.001, self.gameLoop)
        else:
            reactor.callLater(0.02 - t, self.gameLoop)

    def sendPlayerPacket(self):
        packet = json.dumps(
            [{"packet": ClientPackets.CNewPlayer}]
        )
        g.tcpConn.sendData(packet)

    def quitGame(self):
        """called when quitting the game"""
        if g.tcpConn != None:
            # if connected to server, send quit msg
            g.tcpConn.sendQuit()

        reactor.stop()
        pygame.quit()
