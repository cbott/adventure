#!/usr/bin/env python2

import os, pygame
from pygame.locals import *
from pygame.compat import geterror

#######Starting Level#########
START_LEVEL = 1
##############################

gravity = 0.02

SCREEN_SIZE = (800,400) # width, height
IMAGE_FOLDER = "data"

####colors####
BLACK = (0,0,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)
GREEN = (0, 255, 0, 255)
CYAN = (0, 255, 255, 255)
MAGENTA = (255, 0, 255, 255)
NEAR_BLACK = (1,1,1,255)

def write(words, surf, x, y, color = (0,0,0), size = 36):
        font = pygame.font.Font(None, size)
        text = font.render(words, 1, color)
        textpos = text.get_rect(center = (x,y))
        surf.blit(text, textpos)
        pygame.display.flip()
        
def load_image(name, colorkey=None):
    fullname = os.path.join(IMAGE_FOLDER, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def draw_bg(surf, screen, img):
    background_img = pygame.image.load(os.path.join(IMAGE_FOLDER, img)).convert()
    surf.blit(background_img, (0, 0))
    screen.blit(surf, (0,0))
    pygame.display.flip()

class Player(pygame.sprite.Sprite):
    """A guy who moves around the screen"""
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('person.png', -1)
        self.original_image = self.image
        self.level = level
        self.pos = [10,350]
        screen = pygame.display.get_surface()
        self.screen_area = screen.get_rect()
        self.speed = 0.5
        self.direction = 1
        self.velocity = gravity
        self.gravity = gravity
        self.horiz = 0
        self.jumping = False
        self.flipped = 0
        #direction of self.gravity: +/- 1
        self.gforce = lambda:abs(self.gravity)/self.gravity
    def update(self):
        #move side-to-side
        if pygame.key.get_pressed()[K_LEFT]:
            self.move(-1)
        elif pygame.key.get_pressed()[K_RIGHT]:
            self.move(1)
        #slide on cyan
        elif self.is_on(CYAN):
                self.move(self.direction)
        #face direction of travel
        self.image = pygame.transform.flip(self.original_image,int(-(self.direction-1)/2), int(self.flipped))

        #bounce on green
        if self.is_on(GREEN):
                self.velocity = -1.2 * self.velocity
        # otherwise fall downward if you are on white pixels
        # or traveling opposite of gravity (i.e. decrease vertical velocity)
        elif self.is_on(WHITE) or self.is_on(NEAR_BLACK)\
            or self.velocity * self.gforce() < 0:
            self.velocity += self.gravity
        #or stop falling when you land, while traveling in the direction of gravity
        else:
            self.jumping = False
            self.velocity = 0

        #flip gravity on magenta
        if self.is_on(MAGENTA):
            self.gravity = -self.gravity
            self.flipped = -(self.flipped-1)

        #jump           
        if pygame.key.get_pressed()[K_UP] and not self.is_on(WHITE):
            self.jump()
        #drop
        if pygame.key.get_pressed()[K_DOWN]:
                if self.is_on(BLUE):
                        self.pos[1]+=1

        #hit your head
        if self.px_to_top(BLACK):
            if self.velocity * self.gforce() < 0:
                self.velocity = 0    
        #move
        self.pos[1] += self.velocity
        self.rect.midbottom = (self.pos[0],self.pos[1])

    def move(self, dx):
        # Prevent movement through black pixels
        if dx>0:
            self.direction = 1
            if self.px_to_right(BLACK): return
        elif dx<0:
            self.direction = -1
            if self.px_to_left(BLACK): return

        #move horizontaly
        self.pos[0] += self.speed * dx
        #Wrap between sides of the screen
        if self.rect.left < self.screen_area.left:
            self.pos[0] = self.screen_area.right - 10
        if self.rect.right > self.screen_area.right:
            self.pos[0] = self.screen_area.left + 10

    def jump(self):
        """How high?"""
        #move verticaly
        if not self.jumping:
            self.velocity = - self.gforce() * 1.5
            self.jumping = True

    def is_on(self, color):
        """tells whether the player is standing on a certain colored pixel"""
        value = False
        try:
            if self.gforce() == 1:
                bottom_px = (self.rect.centerx,self.rect.bottom+1)
            else:
                bottom_px = (self.rect.centerx,self.rect.top-1)
            value = self.level.get_at(bottom_px) == color
        except IndexError:
            if color == WHITE:
                value = True
            else:
                value = False
        finally:
            return value

    def px_to_right(self, color):
        """tells whether the player is bumping into a pixel on the right"""
        value = False
        try:
            if self.gforce == 1:
                px = (self.rect.right+1,self.rect.bottom-4)
            else:
                px = (self.rect.right+1,self.rect.top+4)
            value = self.level.get_at(px) == color
        except IndexError:
            if color == WHITE:
                value = True
            else:
                value = False
        finally:
            return value
    def px_to_left(self, color):
        """tells whether the player is bumping into a pixel on the left"""
        value = False
        try:
            if self.gforce == 1:
                px = (self.rect.left-1,self.rect.bottom-4)
            else:
                px = (self.rect.left-1,self.rect.top+4)
            value = self.level.get_at(px) == color
        except IndexError:
            if color == WHITE:
                value = True
            else:
                value = False
        finally:
            return value
    def px_to_top(self, color):
        """tells whether the player is bumping into a pixel his head"""
        value = False
        try:
            if self.gforce() == 1:
                l_px = (self.rect.left,self.rect.top - 1)
                r_px = (self.rect.right,self.rect.top - 1)
            else:
                l_px = (self.rect.left,self.rect.bottom + 1)
                r_px = (self.rect.right,self.rect.bottom + 1)
            if self.level.get_at(l_px) == color or \
               self.level.get_at(r_px) == color:
                value = True
        except IndexError:
            if color == WHITE:
                value = True
            else:
                value = False
        finally:
            return value   
    def die(self):
        self.kill()

def pause():
    pausing = True
    while pausing:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                pausing = False
            elif event.type == QUIT:
                pausing = False
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pausing = False
                pygame.quit()
        
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Colors')
    pygame.mouse.set_visible(1)

    background = pygame.Surface(SCREEN_SIZE)
    level = START_LEVEL
#create background
    draw_bg(background, screen, "level"+str(level)+".png")

    clock = pygame.time.Clock()
    player = Player(background)
    allsprites = pygame.sprite.RenderPlain((player))

#Main Loop
    going = True
    while going:
        clock.tick(300)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

        #restarting
        if pygame.key.get_pressed()[K_r]:
            player.die()
            player = Player(background)
            allsprites = pygame.sprite.RenderPlain((player))
        
        #dying
        if player.is_on(RED):
            player.die()
            write("You Died",screen,400,200,color=RED,size=250)
            write("Press Enter To Retry", screen, 400,
                  300, size = 30, color=(255,128,0))
            pause()
            player = Player(background)
            allsprites = pygame.sprite.RenderPlain((player))
        
        #winning
        if player.is_on(YELLOW):
            write("Good Job!", screen, 400, 100, color=(0,255,0))
            write("Level "+str(level)+" completed", screen,
                  400, 130, color=(0,255,0))
            write("Press Enter To Continue", screen, 400,
                  160, size = 20, color=(0,255,0))
            player.die()
            pause()
            level+=1
            try:
                draw_bg(background, screen, "level"+str(level)+".png")
                player = Player(background)
                allsprites = pygame.sprite.RenderPlain((player))
            except:
                write("You Win!!!!!!!!!!!!!!", screen, 400, 200,
                        (255,91,231),50)
                pause()
                going = False
                

    pygame.quit()


#Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
