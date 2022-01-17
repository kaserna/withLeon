import pygame, time, random

pygame.mixer.init()
pygame.init()
pygame.mixer.music.load("Music.mp3")
notrectlaser = pygame.image.load("Laser.png")
notrectlaser2 = pygame.image.load("Laser.png")
arrow = pygame.image.load("downarrow.png")
notrectarrow = pygame.transform.scale(arrow, (200, 200))
notrectlaser = pygame.transform.scale(notrectlaser, (1920, 10))
notrectlaser2 = pygame.transform.scale(notrectlaser2, (1920, 10))
laser = notrectlaser.get_rect()
laser2 = notrectlaser.get_rect()
arrow = notrectarrow.get_rect()
laser.x, laser.y = 0, 200
laser2.x, laser2.y = 0, 600
starttime = time.time()
showtime = time.time()


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pygame.init()
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Start')
back = pygame.image.load('osnPfut.jpg')
back = pygame.transform.scale(back, (800, 500))
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

is_start = False
is_finish = False

start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)


def menu():
    global is_start
    run = True
    font = pygame.freetype.Font("Ore_Crusher/orecrusherrotal.ttf", 50)
    text1 = font.render('SEASON RIDER', 500, (192, 255, 192))
    while run:
        screen.fill((202, 0, 100))
        screen.blit(back, (0, 0))
        if start_button.draw(screen):
            is_start = True
            return is_start
        if exit_button.draw(screen):
            pygame.quit()
            exit(0)
            return None

        for event in pygame.event.get():
            if event.type == pygame.K_1:
                run = False
                exit(0)
                return

        screen.blit(text1[0], (200, 100))

        pygame.display.update()


menu()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
level = 1


class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self):
        super().__init__()
        self.level = None
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .50
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -16

    # Передвижение игрока
    def go_left(self):
        self.change_x = -9
        if self.right:
            self.flip()
            self.right = False
            return None

    def go_right(self):
        self.change_x = 9
        if not self.right:
            self.flip()
            self.right = True
            return None

    def stop(self):
        self.change_x = 0

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        if level == 1:
            self.image = pygame.image.load('platform2.png')
        elif level == 2:
            self.image = pygame.image.load('platform3.png')
        elif level == 3:
            self.image = pygame.image.load('platform4.png')
        self.image = pygame.transform.scale(self.image, (377, 56))
        self.rect = self.image.get_rect()


class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        global arrow
        if level == 1:
            bg = pygame.image.load('fon.jpg')
            bg = pygame.transform.scale(bg, (1920, 1080))
        elif level == 2:
            bg = pygame.image.load('fon2.jpg')
            bg = pygame.transform.scale(bg, (1920, 1080))
        elif level == 3:
            bg = pygame.image.load('fon3.jpg')
            bg = pygame.transform.scale(bg, (1920, 1080))
        screen.blit(bg, (0, 0))
        self.platform_list.draw(screen)


class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level = [
            [210, 100, 100, 900],
            [210, 32, 1500, 700],
            [210, 32, 400, 300],
            [210, 32, 200, 700],
            [210, 32, 800, 500]
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


score = 5
mas = [0.5, 1]


def main_Level1():
    global score, screen, notrectlaser, level, notrectarrow, arrow, starttime, showtime, mas, gifimage
    timer = 0
    arrow.x, arrow.y = 480, 100
    font = pygame.freetype.Font("Ore_Crusher/orecrusherrotal.ttf", 75)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption("Платформер")
    player = Player()
    level_list = [Level_01(player)]

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    done = False
    hidingPos = (-100, -100)

    clock = pygame.time.Clock()
    while not done:
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    done = True

            if score <= 1:
                konec()
                exit(0)
                return

            if arrow.colliderect(player):
                if score >= 1:
                    main_Level2()
                    return None
                else:
                    konec()
                    return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    break

                if event.key == pygame.K_d:
                    player.go_right()
                    break

                if event.key == pygame.K_w:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()
        current_level.update()
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        a = random.randint(0, 1)
        q = random.randint(5, 10) - ((time.time() - starttime) % 60.0)
        qq = mas[a] - ((time.time() - showtime) % 60.0)
        if q <= 0:
            screen.blit(notrectlaser, (0, 200))
            starttime = time.time()
            showtime = time.time()
            if laser.colliderect(player):
                score -= 1
                if score == 0:
                    konec()
                    return None
        elif qq >= 0:
            screen.blit(notrectlaser, (0, 200))

        clock.tick(30)
        text1 = font.render("Lives: " + str(score), 1000, (255, 0, 0))
        screen.blit(text1[0], (100, 50))
        screen.blit(notrectarrow, (480, 100))
        pygame.display.flip()
    pygame.quit()


class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level2 = [
            [210, 100, 100, 900],
            [210, 32, 1500, 250],
            [210, 32, 400, 300],
            [210, 32, 200, 700],
            [210, 32, 800, 500]
        ]

        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main_Level2():
    global score, screen, notrectlaser, level, notrectarrow, arrow, starttime, showtime, mas
    arrow = pygame.Rect(0, 0, 1600, 300)
    level += 1
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption("Платформер")
    player = Player()
    level_list = [Level_02(player)]
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    timer02 = 0
    hidingPos02 = (-100, -100)
    font02 = pygame.freetype.Font("Ore_Crusher/orecrusherrotal.ttf", 75)
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    while not done:
        timer02 += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    done = True

            if arrow.colliderect(player):
                if score >= 1:
                    main_Level3()
                    return None
                else:
                    konec()
                    return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    break
                if event.key == pygame.K_d:
                    player.go_right()
                    break
                if event.key == pygame.K_w:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()

        current_level.update()

        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        a = random.randint(0, 1)
        q = random.randint(5, 10) - ((time.time() - starttime) % 60.0)
        qq = mas[a] - ((time.time() - showtime) % 60.0)
        if q <= 0:
            screen.blit(notrectlaser, (0, 200))
            starttime = time.time()
            showtime = time.time()
            if laser.colliderect(player):
                score -= 1
                if score == 0:
                    konec()
                    return None
        elif qq >= 0:
            screen.blit(notrectlaser, (0, 200))

        if q <= 0:
            screen.blit(notrectlaser, (0, 600))
            starttime = time.time()
            showtime = time.time()
            if laser.colliderect(player):
                score -= 1
                if score == 0:
                    konec()
                    return None
        elif qq >= 0:
            screen.blit(notrectlaser, (0, 600))
        text1 = font02.render("Lives: " + str(score), 1000, (255, 0, 0))
        screen.blit(text1[0], (100, 50))
        screen.blit(notrectarrow, (1600, 30))
        clock.tick(30)

        pygame.display.flip()
    pygame.quit()


class Level_03(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level2 = [
            [210, 100, 300, 900],
            [210, 32, 1500, 300],
            [210, 32, 600, 400],
            [210, 32, 400, 800],
            [210, 32, 800, 500]
        ]

        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


score03 = 0


def main_Level3():
    global score, screen, notrectlaser, level, notrectarrow, arrow, starttime, showtime, mas
    level += 1
    arrow = pygame.Rect(0, 0, 1600, 300)
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption("Платформер")
    player = Player()
    level_list = [Level_02(player)]
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    timer03 = 0
    hidingPos03 = (-100, -100)
    font03 = pygame.freetype.Font("Ore_Crusher/orecrusherrotal.ttf", 75)
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    while not done:
        timer03 += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    done = True

            if arrow.colliderect(player):
                if score >= 1:
                    Win()
                    return None
                else:
                    konec()
                    return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    break
                if event.key == pygame.K_d:
                    player.go_right()
                    break
                if event.key == pygame.K_w:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()

        current_level.update()

        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        a = random.randint(0, 1)
        q = random.randint(3, 7) - ((time.time() - starttime) % 60.0)
        qq = mas[a] - ((time.time() - showtime) % 60.0)
        if q <= 0:
            screen.blit(notrectlaser, (0, 200))
            starttime = time.time()
            showtime = time.time()
            if laser.colliderect(player):
                score -= 1
                if score == 0:
                    konec()
                    return None
        elif qq >= 0:
            screen.blit(notrectlaser, (0, 200))

        if q <= 0:
            screen.blit(notrectlaser, (0, 600))
            starttime = time.time()
            showtime = time.time()
            if laser.colliderect(player):
                score -= 1
                if score == 0:
                    konec()
                    return None
        elif qq >= 0:
            screen.blit(notrectlaser, (0, 600))
        text1 = font03.render("Lives: " + str(score), 1000, (255, 0, 0))
        screen.blit(text1[0], (100, 50))
        screen.blit(notrectarrow, (1600, 30))
        clock.tick(30)

        pygame.display.flip()
    pygame.quit()


class ButtonsEnd:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pygame.init()
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


SCREEN_WIDTH1, SCREEN_HEIGHT1 = 800, 500

screen1 = pygame.display.set_mode((SCREEN_WIDTH1, SCREEN_HEIGHT1), pygame.FULLSCREEN)
pygame.display.set_caption('Button Demo')
backgr = pygame.image.load('osnPfut.jpg')
backgr = pygame.transform.scale(backgr, (800, 500))

exit_img = pygame.image.load('exit_btn.png').convert_alpha()

pygame.font.init()

GAME_OVER_FONT = pygame.freetype.Font("Ore_Crusher/orecrusherrotal.ttf", 75)
textsurface = GAME_OVER_FONT.render('Some Text', False, (100, 100, 100))
exit_button1 = Button(300, 300, exit_img, 0.8)
is_finish1 = True


def konec():
    global is_finish1
    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(backgr, (0, 0))
        if exit_button1.draw(screen):
            is_finish1 = True
            return is_finish1
        text_surface, rect = GAME_OVER_FONT.render("GAME OVER!", (255, 0, 0))
        screen.blit(text_surface, (150, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


class ButtonsWin:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pygame.init()
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


pygame.display.set_caption('Win Window')

exit_img = pygame.image.load('exit_btn.png').convert_alpha()

pygame.font.init()

WIN_FONT = pygame.freetype.Font("Ore_Crusher/orecrusherrotal.ttf", 75)
textsurface1 = GAME_OVER_FONT.render('Some Text', False, (100, 100, 100))
exit_button2 = Button(300, 300, exit_img, 0.8)
backgro = pygame.image.load('osnPfut.jpg')
backgro = pygame.transform.scale(backgro, (800, 500))


def Win():
    global is_finish2
    SCREEN_WIDTH2, SCREEN_HEIGHT2 = 800, 500

    screenWin = pygame.display.set_mode((SCREEN_WIDTH2, SCREEN_HEIGHT2))
    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(backgro, (0, 0))
        if exit_button2.draw(screen):
            return None
        text_surface, rect = GAME_OVER_FONT.render("YOU WIN!", (0, 255, 0))
        screen.blit(text_surface, (200, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


if is_start:
    is_start = False
    pygame.mixer.music.play(1)
    main_Level1()
elif is_finish1:
    Win()

pygame.quit()
