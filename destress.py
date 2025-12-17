import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Destresser")

KEYS = {pygame.K_1:(0/11,1),pygame.K_2:(1/11,1),pygame.K_3:(2/11,1),pygame.K_4:(3/11,1),
        pygame.K_5:(4/11,1),pygame.K_6:(5/11,1),pygame.K_7:(6/11,1),pygame.K_8:(7/11,1),
        pygame.K_9:(8/11,1),pygame.K_0:(9/11,1),pygame.K_MINUS:(10/11,1),pygame.K_EQUALS:(1,1),
        pygame.K_q:(0/11,0.75),pygame.K_w:(1/11,0.75),pygame.K_e:(2/11,0.75),pygame.K_r:(3/11,0.75),
        pygame.K_t:(4/11,0.75),pygame.K_y:(5/11,0.75),pygame.K_u:(6/11,0.75),pygame.K_i:(7/11,0.75),
        pygame.K_o:(8/11,0.75),pygame.K_p:(9/11,0.75),pygame.K_LEFTBRACKET:(10/11,0.75),pygame.K_RIGHTBRACKET:(1,0.75),
        pygame.K_a:(0/10,0.5),pygame.K_s:(1/10,0.5),pygame.K_d:(2/10,0.5),pygame.K_f:(3/10,0.5),
        pygame.K_g:(4/10,0.5),pygame.K_h:(5/10,0.5),pygame.K_j:(6/10,0.5),pygame.K_k:(7/10,0.5),
        pygame.K_l:(8/10,0.5),pygame.K_SEMICOLON:(9/10,0.5),pygame.K_QUOTE:(1,0.5),
        pygame.K_z:(0/9,0.25),pygame.K_x:(1/9,0.25),pygame.K_c:(2/9,0.25),pygame.K_v:(3/9,0.25),
        pygame.K_b:(4/9,0.25),pygame.K_n:(5/9,0.25),pygame.K_m:(6/9,0.25),pygame.K_COMMA:(7/9,0.25),
        pygame.K_PERIOD:(8/9,0.25),pygame.K_SLASH:(1,0.25),
        pygame.K_SPACE:(0.5,0.5)}

class Firework:
    def __init__(self, x, y,lifetime):
        self.x = x
        self.y = y
        self.speed = 5  
        self.exploded = False
        self.particles = []
        self.lifetime=lifetime
    def update(self):
        if not self.exploded:
                self.explode()
        else:
            for particle in self.particles[:]:
                particle.move()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)
    def explode(self):
        self.exploded = True
        for _ in range(100):
            self.particles.append(Particle(self.x, self.y,self.lifetime))
    
    def draw(self, screen):
            for particle in self.particles:
                particle.draw(screen)


class Particle:
    def __init__(self, x, y, lifetime=100):
        self.x = x
        self.y = y
        if lifetime <= 100:
            self.speed = random.uniform(2, 6)
        else:
            self.speed = random.uniform(6, 10)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = lifetime
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed - 0.1
        self.lifetime -= 1
        
    def draw(self, screen):
        if self.lifetime > 0:
            if self.lifetime<=100:
                alpha = int((self.lifetime / 100) * 255)
            else:
                alpha = 255
            color = (*self.color, alpha)
            surf = pygame.Surface((5, 5), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (2, 2), 2)
            screen.blit(surf, (int(self.x), int(self.y)))

fireworks = []
running = True
freeze=False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            freeze = not freeze

        if not freeze:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for _ in range(3):
                    fireworks.append(Firework(x, y,100))
                    
            elif event.type == pygame.KEYDOWN and event.key in KEYS:
                x=KEYS[event.key][0]*(WIDTH)*0.9+0.05*WIDTH
                y=(1-KEYS[event.key][1])*(HEIGHT)*0.9+0.05*HEIGHT
                lifetime=100
                if event.key == pygame.K_SPACE:
                    lifetime*=2
                for _ in range(3):
                    fireworks.append(Firework(x, y,lifetime))
                    
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    if not freeze:
        screen.fill((0, 0, 0))
        
        for firework in fireworks[:]:
            firework.update()
            firework.draw(screen)
            if firework.exploded and len(firework.particles) == 0:
                fireworks.remove(firework)
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
