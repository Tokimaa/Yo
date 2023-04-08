#Створи власний Шутер!
from pygame import*
import pygame
from random import*
pygame.init()
mixer.init()
width, height = 800, 500
window = display.set_mode((width, height))
display.set_caption("Шутер")
background = transform.scale(image.load("background.jpg"), (width, height))
hp1 = transform.scale(image.load("heart.png"), (75, 13))
hp2 = transform.scale(image.load("heart.png"), (75, 13))
hp3 = transform.scale(image.load("heart.png"), (75, 13))
frame = transform.scale(image.load("frame.png"), (300,20))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w_sprite, h_sprite, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w_sprite, h_sprite))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 750:
            self.rect.x += self.speed
    def shot(self):
        bullet = Bullets("bullet.png", self.rect.centerx + 20, self.rect.y + 40, 5, 10, 10)
        bullet2 = Bullets("bullet.png", self.rect.centerx - 25, self.rect.y + 40, 5, 10, 10)
        bullets.add(bullet)
        bullets.add(bullet2)
        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        global lost
        if lost >= 14 and self.rect.y > 400:
            time.delay(25)
        if self.rect.y > height:
            self.rect.x = randint(0, width - 30)
            self.rect.y = -30
            lost += 1  

class Bullets(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill
        

font1 = pygame.font.Font("technofosiano.ttf", 20)
font2 = pygame.font.Font("technofosiano.ttf", 50) 
font3 = pygame.font.Font("technofosiano.ttf", 50) 

player = Player("rocket.png", 350, 425, 50, 50, 10)
monsters = sprite.Group()
random_enemy = ["ufo.png", "asteroid1.png", "asteroid2.png", "asteroid3.png"]
for i in range(6):  
    monster = Enemy(choice(random_enemy)  , randint(0, width - 80), -40, randint(30,50), 30, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
score = 0
clock = time.Clock()
FPS = 120
finish = True 
game = True
start = 1
play = 0
koniec = 0
print("5 losts == -1hp")

mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shot()
    #if lost >= 15:
    #   pass
    hits = pygame.sprite.spritecollide(player, monsters, False)
    if hits:
        koniec = 1
    collide = sprite.groupcollide(monsters, bullets, True, True)
    for c in collide:
        score += 1 
        monster = Enemy(choice(random_enemy)  , randint(0, width - 80), -40, randint(30,50), 30, randint(1, 5))
        monsters.add(monster)

    pattern_lost_scores = font1.render("Lost: " +  str(lost), 0, (255, 255, 255))
    player_scores = font1.render("Scores:" + str(score), 0, (255, 255, 255))
    
    clock.tick(FPS)
    window.blit(background,(0,0))
    if start == 1:
        test = 0
        window.fill((0,0,0))
        btns = pygame.Rect(300, 200, 175, 100)
        pygame.draw.rect(window,(255,255,255), btns)
        but_play = font3.render("Play", 1, (0, 0, 0))
        window.blit(but_play,(330, 225))
        for e in event.get():
            m_x, m_y = pygame.mouse.get_pos()
            if e.type == MOUSEBUTTONDOWN or btns.collidepoint(m_x, m_y):
                pygame.draw.rect(window,(200,200,200), btns)   
                but_play = font3.render("Play", 1, (100, 100, 100))
                window.blit(but_play,(330, 225))
                if e.type == MOUSEBUTTONDOWN:
                    play = 1
                    start = 0 
        
    elif play == 1:
        if lost > 15:
            koniec = 1
            play = 0
        window.blit(pattern_lost_scores,(10,10))
        window.blit(player_scores,(680,10))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        
        if lost < 5:
            window.blit(hp3,(435,484))
        if lost < 10:
            window.blit(hp2,(341,484))
        if lost < 15:
            window.blit(hp1,(247,484))
        window.blit(frame,(228, 480))
        
    if koniec == 1:
        window.fill((0,0,0))
        defeat = font2.render("Lose", 0, (255, 255, 255))
        window.blit(defeat,(width//2 - 50, height//2 - 50))
        
        m_x, m_y = pygame.mouse.get_pos()
        btn = pygame.Rect(250, 270, 50, 50)
        pygame.draw.rect(window,(255,255,255), btn)
        btn_e = pygame.Rect(500, 270, 50, 50)
        pygame.draw.rect(window,(255,0,0), btn_e)
        for e in event.get():
            if btn.collidepoint(m_x, m_y) and e.type == MOUSEBUTTONDOWN:
                for b in bullets:
                    b.kill()
                for m in monsters:
                    m.kill()
                    koniec = 0
                    play = 1
                for i in range(6):  
                    monster = Enemy(choice(random_enemy), randint(0, width - 80), -40, 30, 30, randint(1, 5))
                    monsters.add(monster)   
                lost = 0
                score = 0
                
        if btn_e.collidepoint(m_x, m_y) and e.type == MOUSEBUTTONDOWN:
            game = False
    display.update()
    clock.tick(FPS)
    