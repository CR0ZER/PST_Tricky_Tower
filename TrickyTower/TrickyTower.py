import pygame
import pygame_menu
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import random
import os.path as path

# Global
height = 1600
width = 900
NbPlayer = None
NamePlayer1 = "Player1"
NamePlayer2 = "Player2"
NamePlayer3 = "Player3"
NamePlayer4 = "Player4"


pygame.init()
screen = pygame.display.set_mode((height, width))


def main():
    print("NbPlayer = ", NbPlayer)
    print("NamePlayer = ", NamePlayer1, NamePlayer2, NamePlayer3, NamePlayer4)
    clock = pygame.time.Clock()
    running = True

    # Physics stuff
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Plateformes
    def static_rectangle(space, x, y, r_width, r_height):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (x, y)
        rectangle = pymunk.Poly.create_box(body, (r_width, r_height))
        space.add(body, rectangle)

    static_rectangle(space, 250, 900, 150, 400)
    static_rectangle(space, 600, 900, 150, 400)
    static_rectangle(space, 1000, 900, 150, 400)
    static_rectangle(space, 1350, 900, 150, 400)
    # End Plateformes

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(pygame.Color("white"))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)


# Menu functions
theme_background_image = pygame_menu.themes.THEME_DARK.copy()
theme_background_image.background_color = pygame_menu.BaseImage(image_path="addons/background_menu.png")

def set_nb_player(value, dhze):
    NbPlayer = int(value[1] + 1)
    print("NbPlayer = ", NbPlayer)

def set_name_player(value):
    NamePlayer1 = value
    print("NamePlayer = ", NamePlayer1)


menu2 = pygame_menu.Menu('Tricky Tower', height, width, theme=theme_background_image)
menu2.add.vertical_margin(200)
if NbPlayer == 1:
    menu2.add.text_input('Name : ', default='Player1', onchange=None)
elif NbPlayer == 2:
    menu2.add.text_input('Name : ', default='Player1', onchange=None)
    menu2.add.text_input('Name : ', default='Player2', onchange=None)
elif NbPlayer == 3:
    menu2.add.text_input('Name : ', default='Player1', onchange=None)
    menu2.add.text_input('Name : ', default='Player2', onchange=None)
    menu2.add.text_input('Name : ', default='Player3', onchange=None)
elif NbPlayer == 4:
    menu2.add.text_input('Name : ', default='Player1', onchange=None)
    menu2.add.text_input('Name : ', default='Player2', onchange=None)
    menu2.add.text_input('Name : ', default='Player3', onchange=None)
    menu2.add.text_input('Name : ', default='Player4', onchange=None)
menu2.add.button('Play', main, font_color=(255, 255, 255))
menu2.add.button('Retour', action=pygame_menu.events.BACK, font_color=(255, 255, 255))


# Menu
menu1 = pygame_menu.Menu('Tricky Tower', height, width, theme=theme_background_image)
menu1.add.vertical_margin(200)
menu1.add.button('Jouer', action=menu2, font_color=(255, 255, 255))
menu1.add.selector(title="Nb de joueurs  ", items=[("1", 1), ("2", 2), ("3", 3), ("4", 4)], onchange=set_nb_player, font_color=(255, 255, 255))
menu1.add.button('Quitter', pygame_menu.events.EXIT, font_color=(255, 255, 255))

if __name__ == '__main__':
    menu1.mainloop(screen)
