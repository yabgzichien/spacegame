import pygame
import os
import random
import sys
import json
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 750, 750
pW,pH = 80,80

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Game')
ICON = pygame.image.load(os.path.join('images','icon.png')).convert_alpha()
pygame.display.set_icon(ICON)

# UFOS
UFO_WHITE = pygame.image.load(os.path.join('images','ufo.png')).convert_alpha()
UFO_RED = pygame.image.load(os.path.join('images','ufo_red.png')).convert_alpha()
UFO_ORANGE = pygame.image.load(os.path.join('images','ufo_orange.png')).convert_alpha()

#laser
ORANGE_LASER = pygame.image.load(os.path.join('images','orange_laser.png')).convert_alpha()
PLAYER_LASER = pygame.image.load(os.path.join('images','player_laser.png')).convert_alpha()
WHITE_LASER = pygame.image.load(os.path.join('images','white_laser.png')).convert_alpha()
RED_LASER = pygame.image.load(os.path.join('images','red_laser.png')).convert_alpha()


# Player and Background images
spaceship = ['spaceship0.png']
PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images',spaceship[0])),(pW,pH)).convert_alpha()
BG = pygame.transform.scale(pygame.image.load(os.path.join('images','bg.png')), (WIDTH,HEIGHT)).convert_alpha()


# Explosion Images 
EXPLODE_IMG = []
for i in range(8):
    explode_pic = pygame.image.load(os.path.join('images', f'player_expl{i}.png')).convert_alpha()
    EXPLODE_IMG.append(pygame.transform.scale(explode_pic, (85, 85)))

# Explosion Laser
EXPLODE_LASER = []
for i in range(9):
    explode_pic = pygame.image.load(os.path.join('images', f'expl{i}.png')).convert_alpha()
    EXPLODE_LASER.append(pygame.transform.scale(explode_pic, (50, 50)))


# Rock Images
ROCK_IMGS = []
for i in range(5):
    ROCK_IMGS.append(pygame.image.load(os.path.join('images', f'rock{i}.png')).convert_alpha())

all_sprites = pygame.sprite.Group()

# Power Ups
heart = pygame.image.load(os.path.join('images', 'heart.png')).convert_alpha()
power = pygame.image.load(os.path.join('images', 'powerups.png')).convert_alpha()
power = [heart,power]
heart_power = []
powerup = []

# Sounds
shoot_sound = pygame.mixer.Sound('ora.wav')
shoot_sound.set_volume(0.02)
# bg_music = pygame.mixer.music.load("aot.wav")

rock_sound = pygame.mixer.Sound('expl0.wav')
rock_sound.set_volume(0.04)

enemy_sound = pygame.mixer.Sound('enemy_expl.wav')
enemy_sound.set_volume(0.05)


pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1)

enemy_damage = 10
score = 0

data = {}

class Explosions_Laser(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = EXPLODE_LASER[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(EXPLODE_LASER):
                self.kill()
            else:
                self.image = EXPLODE_LASER[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Explosions(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = EXPLODE_IMG[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 7:
                self.kill()
            else:
                self.image = EXPLODE_IMG[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# create a rock class

class Rock:
    def __init__(self):
        self.x = random.randrange(0, WIDTH-50)
        self.y = random.randrange(-1500, -50)
        self.img_ori = ROCK_IMGS[random.randrange(0,len(ROCK_IMGS))]
        self.img = self.img_ori.copy()
        self.mask = pygame.mask.from_surface(self.img)
        self.y_speed = random.randrange(4,8)
        self.x_speed = random.randrange(-2,2)
        self.deg = random.randrange(-3,3)
        self.total_deg = 0

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def rotate(self):
        self.total_deg += self.deg
        self.total_deg %= 360
        self.img = pygame.transform.rotate(self.img_ori, self.total_deg)

    def move(self):
        self.rotate()
        self.x += self.x_speed
        self.y += self.y_speed
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT:
            self.x = random.randrange(0, WIDTH-50)
            self.y = random.randrange(-1500, -50)


class Power_Up(pygame.sprite.Sprite):
    rand = 0
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = power[self.rand]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = random.randrange(1,2)
        self.x_speed = random.randrange(-1,1)
        self.x = self.rect.x
        self.y = self.rect.y 


    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.x = self.rect.x
        self.y = self.rect.y 
        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT:
            self.kill()

class Power_Up_Po(pygame.sprite.Sprite):
    rand = 1
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = power[self.rand]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = random.randrange(1,2)
        self.x_speed = random.randrange(-1,1)
        self.x = self.rect.x
        self.y = self.rect.y 


    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.x = self.rect.x
        self.y = self.rect.y 
        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT:
            self.kill()
    


class Laser:
    def __init__(self,x,y,img,health=100):
        self.x = x +43
        self.y = y 
        self.img = img 
        self.mask = pygame.mask.from_surface(self.img)
        self.health = health

    def draw(self,window):
        window.blit(self.img, (self.x, self.y))

    def move(self,vel):
        self.y += vel

    def offscreen(self, height):
        return not(self.y >= height and self.y <= 0)

    def collision(self,obj):
        return collide(self,obj)


class Ship:
    COOL_DOWN_COUNT = 15

    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y 
        self.health = health
        self.ship_img = None
        self.ship_laser = None
        self.lasers = []
        self.cool_down_time = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)


    def cool_down(self):
        if self.cool_down_time > self.COOL_DOWN_COUNT:
            self.cool_down_time = 0
        elif self.cool_down_time > 0:
            self.cool_down_time += 1

    def shoot(self):
        if self.cool_down_time == 0:
            laser = Laser(self.x ,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_time = 1


    def move_laser(self, vel, obj):
        self.cool_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.y > HEIGHT:
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= enemy_damage
                expl = Explosions((obj.x+30,obj.y+30))
                all_sprites.add(expl)
                enemy_sound.play()

                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    s = 0
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = PLAYER_IMG
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.mode = 0
        self.mode_timer = 0

    def shoot(self):
        if self.mode == 0:
            if self.cool_down_time == 0:
                laser = Laser(self.x-10, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_time = 1
        elif self.mode >= 1:
            if self.cool_down_time == 0:
                laser1 = Laser(self.x-42, self.y, self.laser_img)
                laser2 = Laser(self.x+25 , self.y, self.laser_img)
                self.lasers.append(laser1)
                self.lasers.append(laser2)
                self.cool_down_time = 1


    def move_laser(self, vel, objs):
        print("Mode: " + str(self.mode))
        if self.mode_timer >= 1:
            self.mode_timer += 1

        if self.mode >= 1 and self.mode_timer >= 60*5:
            self.mode = 0
            self.mode_timer = 0

        self.cool_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.y < 0:
                self.lasers.remove(laser)
                print('Laser removed')
            else:
                for obj in objs:
                    if laser.collision(obj):
                        for laser in self.lasers:
                            laser.health -= 100
                            obj.health -= 100
                            self.s += 42
                            expl = Explosions((obj.x+30,obj.y+30))
                            all_sprites.add(expl)
                            enemy_sound.play()
                            print('Hit an enemy')
                            if random.random() > 0.95:
                                p = Power_Up(obj.x+30,obj.y+30)
                                heart_power.append(p)
                                all_sprites.add(p)
                            if random.randint(1,100) > 95:
                                p2 = Power_Up_Po(obj.x+30,obj.y+30)
                                powerup.append(p2)
                                all_sprites.add(p2)

    def up_shoot(self):
        self.mode += 1
        self.mode_timer += 1


    def draw_health(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y+self.ship_img.get_height()+10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y+self.ship_img.get_height()+10, self.ship_img.get_width()*self.health/100, 10))


                        


class Enemy(Ship):
    ENEMY_VARIANT = {
            "red" :(UFO_RED,RED_LASER),
            "orange":(UFO_ORANGE,ORANGE_LASER),
            "white": (UFO_WHITE,WHITE_LASER)
    }

    def __init__(self,x,y,variant,health=100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img = self.ENEMY_VARIANT[variant]
        self.max_health = health 
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


    def shoot(self):
        if self.cool_down_time == 0:
            laser = Laser(self.x-18, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_time = 1


def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None



def main():
    global enemy_damage, score

    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 0

    lost = False
    lost_count = 0

    #vel
    player_vel = 7.5
    enemy_vel = 3
    enemy_laser_vel = 5.5
    player_laser_vel = 8
    bullet_count = 4

    #fonts
    main_font = pygame.font.SysFont("cosmicsans", 50)
    lost_font = pygame.font.SysFont("cosmicsans", 70)

    player = Player((WIDTH-pW)/2,600)

    rock_list = []
    for i in range(20):
        r = Rock()
        rock_list.append(r)

    enemies = []
    wave_length = 3

    enemy_bullet = 10

    test = 0

    auto = False


    def draw_obj():

        screen.blit(BG,(0,0))

        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = main_font.render(f"Score: {score}", 1, (255,255,255))
        lost_label = lost_font.render("You Ded Lol", 1, (255,255,255))

        # text
        screen.blit(level_label, (10,10))
        screen.blit(score_label, (((WIDTH-score_label.get_width())/2), 10))


        # enemies
        for enemy in enemies:
            enemy.draw(screen)

        # rocks
        for r in rock_list:
            r.draw()
            r.move()

        
        # draw player
        player.draw(screen)
        player.draw_health(screen)

        if lost:
            screen.blit(lost_label, ((WIDTH-lost_label.get_width())/2, HEIGHT/2))




    while run:
        clock.tick(FPS)

        draw_obj()
        score = player.s

        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count >= FPS*3:
                data = {
                    "Score": player.s
                }
                with open('score.json','w') as score_file:
                    json.dump(data, score_file)
                main_menu()
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 1
            enemy_vel += 0.1
            enemy_laser_vel += 0.1
            enemy_bullet *= 0.95
            print(player.COOL_DOWN_COUNT)
            for i in range(wave_length):
                enemy = Enemy(random.randrange(0,WIDTH-64),random.randrange(-2000*level*0.25, -64),random.choice(["red", "orange", "white"]))
                enemies.append(enemy)
        player.cool_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data = {
                    "Score": player.s
                }
                with open('score.json','w') as score_file:
                    json.dump(data, score_file)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    shoot_sound.play()


        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel < HEIGHT - player.get_height() - 20:
            player.y += player_vel
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel < WIDTH - player.get_width():
            player.x += player_vel

        if keys[pygame.K_o]:
            if not auto:
                auto = True
            elif auto:
                auto = False

        if auto:
            player.shoot()


        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_laser(enemy_laser_vel, player)
            if round(random.uniform(0, FPS*enemy_bullet)) == 1:
                enemy.shoot()
            if enemy.health <= 0:
                enemies.remove(enemy)

            if collide(player, enemy): 
                enemy.health -= 100
                expl = Explosions((player.x+40,player.y+50))
                all_sprites.add(expl)
                enemy_sound.play()
                player.health -= 10
            elif enemy.y > HEIGHT - enemy.get_height():
                enemies.remove(enemy)
                player.health -= 10
                print(player.health)
            for laser_p in player.lasers:
                for laser_e in enemy.lasers:
                    if collide(laser_p, laser_e):
                        expl_l = Explosions_Laser((laser_p.x+30, laser_p.y+30 ))
                        all_sprites.add(expl_l)

                        laser_p.health -= 50
                        laser_e.health -= 100
        # Rock Collision
        for laser_p in player.lasers:
                for rock in rock_list:
                    if collide(rock, laser_p):
                        expl_l = Explosions_Laser((laser_p.x+30, laser_p.y+30 ))
                        all_sprites.add(expl_l)

                        rock_sound.play()

                        rock_list.remove(rock)
                        r = Rock()
                        rock_list.append(r)

                        laser_p.health -= 50
                        player.s += 17
                        print(laser_p.health)


        for rock in rock_list:
            if collide(rock,player):
                expl_l = Explosions_Laser((player.x+30, player.y+30 ))
                all_sprites.add(expl_l)

                rock_list.remove(rock)
                r = Rock()
                rock_list.append(r )
                player.health -= 2

        # Actually Working but the collision detection is not good
        # Implement another check collision method
        for laser_e in enemy.lasers:
            for rock in rock_list:
                if collide(rock, laser_e):
                    expl_l = Explosions_Laser((laser_e.x+30, laser_e.y+30 ))
                    all_sprites.add(expl_l)

                    rock_list.remove(rock)
                    laser_e.health -= 100


        # Check Laser HP
        for laser in player.lasers:
            if laser.health <= 0:
                player.lasers.remove(laser)

        for laser in enemy.lasers:
            if laser.health <= 0:
                enemy.lasers.remove(laser)

        # Check Enemy HP
        for enemy in enemies:
            if enemy.health <= 0:
                enemies.remove(enemy)

        #Check if player collide with the powerups
        for p in heart_power:
            if collide(player, p):
                heart_power.remove(p)
                p.kill()
                if p.rand == 0:
                    player.health += 20

        if player.health > 100:
            player.health = 100

        for p in powerup:
            if collide(player, p):
                powerup.remove(p)
                p.kill()
                if p.rand == 1:
                    player.up_shoot()

                    

        
        player.move_laser(-player_laser_vel,enemies)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()


def main_menu():
    run = True
    global PLAYER_IMG,spaceship

    i = 0

    with open('score.json') as score_file:
        data = json.load(score_file)

    font = pygame.font.SysFont("cosmicsans", 70)
    font2 = pygame.font.SysFont("cosmicsans", 50)
    main_menu_text = font.render("Press P to begins :)", 1, (255,255,255))
    change_player = font2.render("Use Arrow Keys to change Spaceship", 1, (255,255,255))
    score_label = font2.render(f'Score: {data["Score"]}',1,(255,255,255))

    def draw_obj():
        screen.blit(BG, (0,0))

        screen.blit(main_menu_text, ((WIDTH-main_menu_text.get_width())/2, (HEIGHT/2) - 200))
        screen.blit(change_player, ((WIDTH-change_player.get_width())/2, (HEIGHT/2)-75))
        screen.blit(PLAYER_IMG, (WIDTH/2-PLAYER_IMG.get_width()/2, HEIGHT/2))
        screen.blit(score_label, (WIDTH/2-score_label.get_width()/2, (HEIGHT/2)+80))


    while run:
        draw_obj()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    main()
                    run = False
                if event.key == pygame.K_RIGHT:
                    spaceship = ['spaceship0.png', 'spaceship1.png', 'spaceship2.png']

                    i += 1
                    if i >= len(spaceship):
                        i = 0

                    PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images',spaceship[i])),(pW,pH)).convert_alpha()

                if event.key == pygame.K_LEFT:
                    spaceship = ['spaceship0.png', 'spaceship1.png', 'spaceship2.png']

                    i -= 1
                    if i <= 0:
                        i = len(spaceship) - 1

                    PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images',spaceship[i])),(pW,pH)).convert_alpha()

        all_sprites.draw(screen)
        all_sprites.update() 
        pygame.display.update()
main_menu()