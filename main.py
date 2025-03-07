import pygame
pygame.init()


def render_colorpicker():
    global z_choose, cpcx, cpcy

    pygame.draw.rect(screen, (0, 0, 0), (width // 2 + 40, 30, 295, 345), 0, 5)
    
    for x in range(255):
        for y in range(255):
            pygame.draw.rect(screen, (x, y, z_choose), (shiftx + x, shifty + y, 1, 1))
            if (x, y, z_choose) == cp_color:
                cpcx, cpcy = shiftx + x, shifty + y
    
    pygame.draw.rect(screen, (0, 0, 0), (cpcx - 5, cpcy - 5, 10, 10), 1)
    pygame.draw.rect(screen, (255, 255, 255), (cpcx - 4, cpcy - 4, 8, 8), 1)
    
    for z in range(255):
        pygame.draw.rect(screen, (cp_color[0], cp_color[1], z), (shiftx + z, 325, 1, 20))
    
    pygame.draw.rect(screen, (0, 0, 0), (shiftx + z_choose - 3, 315, 6, 40), 1)
    pygame.draw.rect(screen, (255, 255, 255), (shiftx + z_choose - 2, 316, 4, 38), 1)


import numpy, cv2, pyautogui, os
os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 0'
cv2.imwrite('screen.png', cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR))

width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
image = pygame.transform.scale(pygame.image.load('screen.png'), [width, height])
PI = 3.141592653589793238462643383279502884197169399375105

screen = pygame.display.set_mode((width, height), flags=pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption('Annotator+ Pro')

tools = list(range(width // 2 - 200, width // 2 - 124, 25)) + list(range(width // 2 + 75, width // 2 + 176, 25))
coordinates, mouse_x, mouse_y, origin, clicked = [], 0, 0, 0, 0
current, fill, color, colors = 1, 1, (63, 140, 255), (None, None, None, None, None, (63, 140, 255), (255, 66, 122), (44, 255, 102), None)
shiftx, shifty = width // 2 + 60, 50
can, cp_open, cp_color, draw, message, cpcx, cpcy, z_choose, cp_rect, cp_crect, cp_zrect = 1, 0, (255, 255, 255), 0, 'Text...', shiftx + 255, shifty + 255, 0, pygame.Rect(width // 2 + 40, 30, 295, 355), pygame.Rect(width // 2 + 60, 50, 255, 255), pygame.Rect(width // 2 + 60, 325, 255, 20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = draw = 0
            can = 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked, origin = 1, (mouse_x, mouse_y)
            if not mouse_y < 30 and cp_open == 0:
                if current == 4:
                    if message != 'Text...':
                        message = 'Text...'
                        continue
                draw = 1
                coordinates.append(
                    {'ox': origin[0], 'oy': origin[1], 'x': mouse_x, 'y': mouse_y, 'fill': fill, 'color': color,
                     'tool': current, 'message': message})
                if current == 4:
                    message = ''
            if cp_open == 1:
                cpmx, cpmy = event.pos[0], event.pos[1]
                if not cp_rect.collidepoint(cpmx, cpmy):
                    cp_open = 0
                else:
                    if cp_crect.collidepoint(cpmx, cpmy):
                        cp_color = color = (cpmx - (width // 2 + 60), cpmy - 50, z_choose)
                    elif cp_zrect.collidepoint(cpmx, cpmy):
                        z_choose = cpmx - (width // 2 + 60)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT or pygame.key.get_mods() & pygame.KMOD_CAPS:
                message += event.unicode
            elif pygame.key.name(event.key) in [chr(i) for i in range(33, 127)] and message != 'Text...':
                message += pygame.key.name(event.key)
            elif event.key == pygame.K_f:
                fill = 0 if fill == 1 else 1
            elif pygame.key.name(event.key) == 'space':
                message += ' '
            elif pygame.key.name(event.key) == 'backspace':
                message = message[:-1]

    screen.blit(image, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (width // 2 - 200, -10, 400, 40), 0, 5)

    for tool in tools:
        if tool < mouse_x < tool + 25 and mouse_y < 30:
            pygame.draw.rect(screen, (30, 30, 30), (tool, -10, 25, 40), 0, 5)
            if clicked:
                if tools.index(tool) < 4:
                    current = tools.index(tool) + 1
                elif tools.index(tool) == 4:
                    if can == 1 and len(coordinates) != 0:
                        del coordinates[-1]
                        can = 0
                elif tools.index(tool) == 8:
                    cp_open = 1
                else:
                    color = colors[tools.index(tool)]
        if tools.index(tool) == 4:
            pygame.draw.circle(screen, (255, 255, 255), (tool + 12, 15), 5, 1, False, True, True, True)
        elif tools.index(tool) == 8:
            pygame.draw.circle(screen, (255, 255, 255), (tool + 12, 15), 5)
            pygame.draw.circle(screen, cp_color, (tool + 12, 15), 4)
        elif tools.index(tool) > 4:
            pygame.draw.circle(screen, (255, 255, 255), (tool + 12, 15), 5)
            pygame.draw.circle(screen, colors[tools.index(tool)], (tool + 12, 15), 4)

    pygame.draw.line(screen, (255, 255, 255), (width // 2 - 190, 10), (width / 2 - 185, 20), 2)
    pygame.draw.rect(screen, (255, 255, 255), (width // 2 - 168, 10, 10, 10), 2)
    pygame.draw.circle(screen, (255, 255, 255), (width // 2 - 137, 16), 5, 2)
    screen.blit(pygame.font.Font('font.ttc', 16).render('T', False, (255, 255, 255)), (width // 2 - 117, 5))

    for item in coordinates:
        if item['tool'] == 1:
            pygame.draw.line(screen, item['color'], (item['ox'], item['oy']), (item['x'], item['y']))
        elif item['tool'] == 2:
            pygame.draw.polygon(screen, item['color'], ((item['ox'], item['oy']), (item['x'], item['oy']), (item['x'], item['y']), (item['ox'], item['y'])), item['fill'])
        elif item['tool'] == 3:
            pygame.draw.arc(screen, item['color'], (item['ox'] if item['ox'] < item['x'] and item['oy'] < item['y'] or item['ox'] < item['x'] and item['y'] < item['oy'] else item['x'], item['oy'] if item['oy'] < item['y'] else item['y'], abs(item['ox'] - item['x']), abs(item['oy'] - item['y'])), 0, 3 * PI, item['fill'])
        elif item['tool'] == 4:
            screen.blit(pygame.font.Font('font.ttc', 32).render(item['message'], False, item['color']), (item['ox'], item['oy']))
    if draw and not mouse_y < 30:
        coordinates[-1] = {'ox': origin[0], 'oy': origin[1], 'x': mouse_x, 'y': mouse_y, 'fill': fill, 'color': color,
                           'tool': current, 'message': message}
    if current == 4 and message != 'Text...':
        coordinates[-1]['message'] = message
        rect = pygame.font.Font('font.ttc', 32).render(item['message'], False, item['color']).get_rect()
        pygame.draw.rect(screen, (0, 0, 0), (coordinates[-1]['ox'] + rect.width, coordinates[-1]['oy'], 2, rect.height))
    if cp_open:
        render_colorpicker()
    pygame.display.update()
