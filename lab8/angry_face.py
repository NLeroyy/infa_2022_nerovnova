import pygame as pg

pg.init()

FPS = 30
screen = pg.display.set_mode((400, 400))
black = (0,0,0)
red = (255,0,0)
yellow = (253,253,0)
grey = (165,165,165)

screen.fill(grey)

def draw_emoji():
    ''' Рисует смайлик на экране. '''
    draw_head()
    draw_eyes()
    draw_eyebrows()
    draw_mouth()

def draw_head():
    ''' Рисует голову. '''
    pg.draw.circle(screen, yellow, (200,200), 100)
    pg.draw.circle(screen, black, (200, 200), 100, 2)

def draw_eyes():
    ''' Рисует глаза смайлика. '''
    pg.draw.circle(screen, red, (160,180),25)
    pg.draw.circle(screen, black, (160,180), 25, 1)     # Левый глаз
    pg.draw.circle(screen, black, (155,180), 10)

    pg.draw.circle(screen, red, (240,175), 15)
    pg.draw.circle(screen, black, (240,175), 15, 1)          # Правый глаз
    pg.draw.circle(screen, black, (240,175), 5)
def draw_eyebrows():
    ''' Рисует брови смайлика. '''
    pg.draw.polygon(screen, black, [[107,133], [187,158],
                                    [187,167],[107,142]])
    pg.draw.polygon(screen, black, [[217,164], [303,143],
                                    [304,151],[220,170]])
def draw_mouth():
    ''' Рисует рот. '''
    pg.draw.rect(screen, black, (150,240,100,15))


pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

    draw_emoji()
    pg.display.update()

pg.quit()