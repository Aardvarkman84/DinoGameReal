import pygame
import sys
import random

class Dino(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.dead = False
        self.jump = False
        self.duck = False
        self.rect = pygame.Rect(0, 216, 72, 84)
        self.image = pygame.image.load("dinorun0000.png")
        self.image = pygame.transform.scale(self.image, (72, 84))
        self.hitbox = pygame.Rect(10, 216, 52, 84)
        self.score = 0
        self.dat = 2
        self.vel = 0

    def jumpDino(self):
        self.vel -= self.dat
        self.dat *= .75
        self.jump = True
        self.image = pygame.image.load("dino0000.png")
        self.image = pygame.transform.scale(self.image, (72, 84)) 

    def duckDino(self, toDuck):
        if(toDuck):
            self.image = pygame.image.load("dinoduck0000.png")
            self.image = pygame.transform.scale(self.image, (72, 42))
            self.rect = pygame.Rect(0, 258, 72, 42)
            self.hitbox = pygame.Rect(30, 258, 52, 42)
            self.duck = True
        if(not toDuck):
            self.image = pygame.image.load("dinorun0000.png")
            self.image = pygame.transform.scale(self.image, (72, 84))
            self.rect = pygame.Rect(0, 216, 72, 84)
            self.hitbox = pygame.Rect(10, 216, 52, 84)
            self.duck = False

    def die(self, con):
        self.image = None
        self.rect = None
        self.hitbox = None
        self.dead = True
        self.score = con
       




def main():
    pygame.init()
    dino = Dino()
    screen = pygame.display.set_mode((500,300))

    font = pygame.font.Font("slkscre.ttf", 20)
    fontImg = font.render("0", 1, (0,0,0))
    fontRect = fontImg.get_rect(center = (400, 50))
    
    period = 90
    switchImg = 0
    timer = pygame.time.Clock()
    obsGroup = pygame.sprite.Group()
    count = 0
    speed = 4.0
    while True:
        period -= 1
        screen.fill((255,255,255)) 
        if not dino.dead:
            fontImg = font.render(str(int(count)), 1, (0,0,0))
            fontRect = fontImg.get_rect(center = (400, 50))
            screen.blit(fontImg, fontRect)
            dino.rect.top += dino.vel
            dino.hitbox.top += dino.vel
            dino.vel += .7
            count += 1.0
            if period == 0:
                rand = random.randint(1,4)
                period = random.randint(50, 120)
                if rand == 1:
                    obsGroup.add(Obstacle("cactusBig0000.png", 500, 240, 30, 60, False, False))
                elif rand == 2:
                    obsGroup.add(Obstacle("cactusSmall0000.png", 500, 260, 20, 40, False, False))
                elif rand == 3:
                    obsGroup.add(Obstacle("cactusSmallMany0000.png", 500, 260, 60, 40, False, False))
                elif rand == 4:
                    randbird = random.randint(1,3)
                    if randbird == 1:
                        obsGroup.add(Obstacle("berd.png", 500, random.randint(120,250), 69, 60, True, True))
                    if randbird == 2:
                        obsGroup.add(Obstacle("berd.png", 500, random.randint(160,250), 69, 60, True, True))
                    if randbird == 3:
                        obsGroup.add(Obstacle("berd.png", 500, random.randint(200,250), 69, 60, True, True))
        else:
            fontD = pygame.font.Font("slkscre.ttf", 50)
            fontDead = fontD.render("Game Over", 1, (0,0,0))
            fontDRect = fontDead.get_rect(center = (250, 150))
            fontS = pygame.font.Font("slkscre.ttf", 25)
            fontScore = fontS.render("Your Score: " + str(int(count)), 1, (0,0,0))
            fontSRect = fontScore.get_rect(center = (250, 200))
            screen.blit(fontDead, fontDRect)
            screen.blit(fontScore, fontSRect)
        if dino.rect.bottom >= 300:
            dino.vel = 0
            dino.dat = 4
            dino.rect.bottom = 300
            dino.hitbox.bottom = 300
            dino.jump = False
        if count % 5 == 0 and not dino.jump and not dino.duck:
            if switchImg % 2 == 0:
                dino.image = pygame.image.load("dinorun0001.png")
                dino.image = pygame.transform.scale(dino.image, (72, 84))
            if not switchImg % 2 == 0:
                dino.image = pygame.image.load("dinorun0000.png")
                dino.image = pygame.transform.scale(dino.image, (72, 84))
            switchImg += 1
        if count % 5 == 0 and not dino.jump and dino.duck:
            if switchImg % 2 == 0:
                dino.image = pygame.image.load("dinoduck0000.png")
                dino.image = pygame.transform.scale(dino.image, (72, 42))
            if not switchImg % 2 == 0:
                dino.image = pygame.image.load("dinoduck0001.png")
                dino.image = pygame.transform.scale(dino.image, (72, 42))
            switchImg += 1    

        for obs in obsGroup:
            if not dino.dead:
                obs.rect.left -= (speed + count/200)
            if(obs.rect.right <= 0):
                obsGroup.remove(obs)
            if count % 30 == 0:
                if obs.pter and not dino.dead:
                    if obs.pos:
                        obs.image = pygame.image.load("berd2.png")
                        obs.image = pygame.transform.scale(obs.image, (69, 60))
                        obs.pos = False
                    else:
                        obs.image = pygame.image.load("berd.png")
                        obs.image = pygame.transform.scale(obs.image, (69, 60)) 
                        obs.pos = True
        if not dino.hitbox.collidelist(obsGroup.sprites()) == -1:
            dino.dead = True
            dino.image = pygame.image.load("dinoDead0000.png")
            dino.image = pygame.transform.scale(dino.image, (72, 84))
            dino.rect = pygame.Rect(0, dino.rect.bottom - 84, 72, 84)
        screen.blit(dino.image, dino.rect)
        obsGroup.draw(screen)
        pygame.display.flip()
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_RSHIFT and not dino.dead and not dino.jump:
                    dino.duckDino(True)
            if e.type == pygame.KEYUP:   
                if e.key == pygame.K_RSHIFT and not dino.dead and not dino.jump:
                    dino.duckDino(False)
        if pygame.key.get_pressed()[pygame.K_SPACE] and not dino.dead and not dino.duck:
            dino.jumpDino()


class Obstacle(pygame.sprite.Sprite):
       
    def __init__(self, image, top, left, width, height, ptera, posit):
        super().__init__()
        self.rect = pygame.Rect(top, left, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.vel = -3
        self.pter = ptera
        self.pos = posit

if __name__ == "__main__":
    main()