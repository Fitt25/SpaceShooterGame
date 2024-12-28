import pygame
from os.path import join 
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, dt):
         # input
        #pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt   

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot: 
            laser = Laser(all_sprites, player, laser_surf)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            
        self.laser_timer()
        

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))
        
class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH), 0))
        self.creation_time = pygame.time.get_ticks()
        self.duration_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400, 700)

    def update(self, dt):
        self.rect.center +=  self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.creation_time >= self.duration_time:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, player, surf):
        super().__init__(groups)
        self.player = player
        player_x, player_y = self.player.rect.center
        self.image = surf
        self.rect = self.image.get_frect(midbottom = (player_x , player_y - 50))
    

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

# setting up our basics
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1240,620
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# import
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()

# sprites
all_sprites = pygame.sprite.Group()

for i in range(20):
    stars = Star(all_sprites, star_surf)
   
player = Player(all_sprites)

# custom events 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)


while running:
    dt = clock.tick() / 1000
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor = Meteor(all_sprites, meteor_surf) 

    #update
    all_sprites.update(dt)

    # draw the game
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)
    
    pygame.display.update()
pygame.quit()
