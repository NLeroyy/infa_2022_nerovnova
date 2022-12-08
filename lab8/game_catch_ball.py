import pygame as pg
from random import randint
import math

pg.init()
width = 1100
height = 650
FPS = 30
screen = pg.display.set_mode((width, height))

sea = (32, 178, 170)
spring = (0, 255, 127)
aqua = (127, 255, 212)
cyan = (0, 255, 255)
pink = (255, 20, 147)
purple = (128, 0, 128)
lime = (0, 255, 0)
black = (0, 0, 0)
colors = [
            sea, spring,
            aqua, pink,
            purple, lime,
            cyan
        ]

def characteristics(x_range, y_range, vx_range,
                    vy_range, r_range, colors):
    ''' Задает случайные характеристики шара,
    возвращая их в виде массива.
    x_range - диапазон х-координат центра шара.
    y_range - диапазон у-координат центра шара.
    vx_range - диапазон скоростей шара по оси x.
    vy_range - диапазон скоростей шара по оси y.
    r_range - диапазон возможных радиусов шара.
    colors - массив возможных цветов в формате,
    подходящем для pygame.Color.

    '''
    col = colors[randint(0, len(colors) - 1)]
    r = randint(r_range[0], r_range[1])
    v_x = randint(vx_range[0], vx_range[1])
    v_y = randint(vy_range[0], vy_range[1])
    x = randint(x_range[0], x_range[1])
    y = randint(y_range[0], y_range[1])
    return [x, y, v_x, v_y, r, col]

def new_ball(surface, x_range, y_range,
             vx_range, vy_range, r_range, colors):
    '''Создает и рисует новый шар.
    surface - объект pygame.Surface.
    x_range - диапазон х-координат центра шара.
    y_range - диапазон у-координат центра шара.
    vx_range - диапазон скоростей шара по оси x.
    vy_range - диапазон скоростей шара по оси y.
    r_range - диапазон возможных радиусов шара.
    colors - массив возможных цветов в формате,
    подходящем для pygame.Color.

    '''
    global ball
    character = characteristics(x_range, y_range,
             vx_range, vy_range, r_range, colors)
    x = character[0]
    y = character[1]
    v_x = character[2]
    v_y = character[3]
    r = character[4]
    col = character[5]
    ball = {'x': x, 'y': y, 'v_x': v_x, 'v_y': v_y, 'r': r, 'col': col}
    arr_balls.append(ball)
    pg.draw.circle(surface, col, (x, y), r)

def first_one(surface, x_range, y_range, vx_range,
               vy_range, r_range, colors):
    '''Создаёт первый шар.
    surface - объект pygame.Surface.
    x_range - диапазон х-координат центра шара.
    y_range - диапазон у-координат центра шара.
    vx_range - диапазон скоростей шара по оси x.
    vy_range - диапазон скоростей шара по оси y.
    r_range - диапазон возможных радиусов шара.
    colors - массив возможных цветов в формате,
    подходящем для pygame.Color.

    '''
    global first
    if first:
        new_ball(
            surface, x_range, y_range, vx_range,
            vy_range, r_range, colors)
        first = False

def click(event, ball):
    '''Проверяет попадание по шару и обновляет количество очков.
    event - объект pygame.Event.
    ball - словарь с параметрами шара.

    '''
    global res, hit
    x, y = event.pos[0], event.pos[1]
    if (x - ball['x'])**2 + (y - ball['y'])**2 <= ball['r']**2:
        res += 1
        hit = True
    else:
        hit = False

def hit_one_ball(event, ball):
    '''Проверяет попадание хотя бы по одному щару,
       из находящихся на экране
       envent - объект pygame.Event.
       ball - словарь с параметрами шара.
       arr_balls - массив шаров, находящихся на экране.

       '''
    for ball in arr_balls:
        click(event, ball)
        if hit:
            arr_balls.pop(arr_balls.index(ball))
            break

def move(balls, width, height,
               vx_range, vy_range):
    '''Задаёт движение шаров.
    balls - словарь с парметрами шаров.
    width - ширина экрана.
    height - высота экрана.
    vx_range - диапазон скоростей шара по оси x.
    vy_range - диапазон скоростей шара по оси y.

    '''
    for ball in balls:
        reflection(ball, width, height,
                             vx_range, vy_range)
        ball['x'] += ball['v_x'] * dt
        ball['x'] = int(ball['x'])
        ball['y'] += ball['v_y'] * dt
        ball['y'] = int(ball['y'])
        pg.draw.circle(screen, ball['col'],
                      (ball['x'], ball['y']), ball['r'])

def reflection(ball, width, height,
                         vx_range, vy_range):
    '''Сменяет, если необходимо, скорость шара при отражении,
    на случайный вектор, направленный так, чтобы шар летел от стены.
    ball - словарь с параметрами шара.
    width - ширина экрана.
    height - высота экрана.
    vx_range - диапазон скоростей шара по оси x.
    vy_range - диапазон скоростей шара по оси y.

    '''
    if ball['x'] <= ball['r']:
        ball['v_x'] = randint(1, vx_range[1])
    elif ball['x'] >= width - ball['r']:
        ball['v_x'] = randint(vx_range[0], -1)
    if ball['y'] <= ball['r']:
        ball['v_y'] = randint(1, vx_range[1])
    elif ball['y'] >= height - ball['r']:
        ball['v_y'] = randint(vy_range[0], -1)

#добавим ещё один тип мишеней со своим характером движения
def new_target(surface, colors):
    """Создаёт новую мишень.
    surface - объект pygame.Surface.
    colors - массив возможных цветов в формате,
    подходящем для pygame.Color.
    """

    global targets
    target_surf = pg.Surface((40, 40))
    target_surf.fill((0, 0, 0))
    color = colors[randint(0, len(colors) - 1)]
    pg.draw.polygon(target_surf, color,
                        [[20, 0], [40, 10], [40, 30], [20, 40], [0, 30], [0, 10]])
    target = {"center_angle": 0, "OMEGA": 1, "omega": 4, "self_angle": 0,
              "x": 500, "y": 75,"color": color}
    targets.append(target)
    surface.blit(target_surf, (500, 75))

def move_targets(surface, targets):
    """Двигает цели по экрану.
    targets - массив с параметрами целей.
    surface - объект pygame.Surface.
    """

    for target in targets:
        target["center_angle"] += target["OMEGA"] * dt/2
        target["self_angle"] += target["omega"] * dt/2
        #target["center_angle"] %= 360
        #target["self_angle"] %= 360
        target_surf = pg.Surface((40, 40))
        target_surf.fill((0, 0, 0))
        pg.draw.polygon(target_surf, target["color"],
                        [[20, 0], [40, 10], [40, 30], [20, 40], [0, 30], [0, 10]])
        target_surf = pg.transform.rotate(target_surf, -math.degrees(target["self_angle"]))
        x = 500 + (300*math.sin(target["center_angle"]))
        y = 375 - (300*math.cos(target["center_angle"]))
        target["x"] = x
        target["y"] = y
        surface.blit(target_surf, (x, y))

def hit_one_target(event, targets):
    '''Проверяет попадание хотя бы в одну цель,
    event - объект pygame.Event.
    targets - Массив содержащий параметры шаров, нахлдящихся на экране.

    '''
    for target in targets:
        hit_target(event, target)
        if hit_t:
            targets.pop(targets.index(target))
            break

def hit_target(event, target):
    '''Проверяет попадание мыши по цели и засчитывает очки.
    event - объект pygame.Event.
    target - словарь с параметрами цели.

    '''
    global res, hit_t
    if (event.pos[0]-target["x"]-20)**2 + \
            (event.pos[1]-target["y"]-20)**2 <= 40**2:
        res += 3   # Засчитывает 3 очка за попадание
        hit_t = True
    else:
        hit_t = False

pg.display.update()
clock = pg.time.Clock()
finished = False
first = True
res = 0
arr_balls = []
targets = []

while not finished:
    dt = clock.tick(FPS) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            hit_one_ball(event, arr_balls)
            hit_one_target(event, targets)
            if len(arr_balls) == 0 or (not hit and not hit_t):
                new_ball(screen, (60, 900), (60, 550), (-150, 150),
                        (-150, 150), (10, 50), colors)
            if len(targets) == 0 or (not hit_t and not hit):
                new_target(screen, colors)
    move_targets(screen, targets)
    move(arr_balls, width, height, (-150, 150), (-150, 150))
    first_one(screen, (60, 900), (60, 550), (-150, 150),
              (-150, 150), (10, 50), colors)
    pg.display.update()
    screen.fill((0, 0, 0))

pg.quit()
print("Количество очков: ", res)
