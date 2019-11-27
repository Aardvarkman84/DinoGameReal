import pygame
import memeTest
import sys
import random

numDino = 3

dinolist = []
for i in range(3):
    dinolist.append(memeTest.Dino())

def main(dList):
    pygame.init()
    screen = pygame.display.set_mode((500,300))

    font = pygame.font.Font("slkscre.ttf", 20)
    fontImg = font.render("0", 1, (0,0,0))
    fontRect = fontImg.get_rect(center = (400, 50))
    
    deadCount = 0
    period = 90
    switchImg = 0
    timer = pygame.time.Clock()
    obsGroup = pygame.sprite.Group()
    count = 0
    speed = 4.0
    while True:
        period -= 1
        screen.fill((0,0,255))
        
        fontImg = font.render(str(int(count)), 1, (0,0,0))
        fontRect = fontImg.get_rect(center = (400, 50))
        screen.blit(fontImg, fontRect)           
        count += 1.0
        if period == 0:
            rand = random.randint(1,4)
            period = random.randint(50, 120)
            if rand == 1:
                obsGroup.add(memeTest.Obstacle("cactusBig0000.png", 500, 240, 30, 60, False, False))
            elif rand == 2:
                obsGroup.add(memeTest.Obstacle("cactusSmall0000.png", 500, 260, 20, 40, False, False))
            elif rand == 3:
                obsGroup.add(memeTest.Obstacle("cactusSmallMany0000.png", 500, 260, 60, 40, False, False))
            elif rand == 4:
                randbird = random.randint(1,3)
                if randbird == 1:
                    obsGroup.add(memeTest.Obstacle("berd.png", 500, random.randint(120,250), 69, 60, True, True))
                if randbird == 2:
                    obsGroup.add(memeTest.Obstacle("berd.png", 500, random.randint(160,250), 69, 60, True, True))
                if randbird == 3:
                    obsGroup.add(memeTest.Obstacle("berd.png", 500, random.randint(200,250), 69, 60, True, True))
        if deadCount == numDino:
            fontD = pygame.font.Font("slkscre.ttf", 50)
            fontDead = fontD.render("Game Over", 1, (0,0,0))
            fontDRect = fontDead.get_rect(center = (250, 150))
            fontS = pygame.font.Font("slkscre.ttf", 25)
            fontScore = fontS.render("Your Score: " + str(int(count)), 1, (0,0,0))
            fontSRect = fontScore.get_rect(center = (250, 200))
            screen.blit(fontDead, fontDRect)
            screen.blit(fontScore, fontSRect)

        for dino in dList:
            if not dino.dead:
                dino.rect.top += dino.vel
                dino.hitbox.top += dino.vel
                dino.vel += .7
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
                if not dino.hitbox.collidelist(obsGroup.sprites()) == -1:
                    dino.die(count)
                    deadCount += 1

        for obs in obsGroup:
            obs.rect.left -= (speed + count/200)
            if(obs.rect.right <= 0):
                obsGroup.remove(obs)
            if count % 30 == 0:
                if obs.pter:
                    if obs.pos:
                        obs.image = pygame.image.load("berd2.png")
                        obs.image = pygame.transform.scale(obs.image, (69, 60))
                        obs.pos = False
                    else:
                        obs.image = pygame.image.load("berd.png")
                        obs.image = pygame.transform.scale(obs.image, (69, 60)) 
                        obs.pos = True
        
        for dino in dList:
            if not dino.dead:
                screen.blit(dino.image, dino.rect)
        obsGroup.draw(screen)
        pygame.display.flip()
        timer.tick(60)

if __name__ == "__main__":
    main(dinolist)

