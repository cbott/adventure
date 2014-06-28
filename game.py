import os, pygame
from pygame.locals import *
from pygame.compat import geterror


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#gravity is 10!!!!!!!!!!! ALWAYS!
GRAVITY = 0.1

SCREEN_SIZE = (800,400)

####colors####
BLACK = (0,0,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)

def write(words, surf, x, y, color = (0,0,0), size = 36):
        font = pygame.font.Font(None, size)
        text = font.render(words, 1, color)
        textpos = text.get_rect(center = (x,y))
        surf.blit(text, textpos)
        pygame.display.flip()
        
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
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
    background_img = pygame.image.load(os.path.join(data_dir, img)).convert()
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
        self.pos = [10,200]
        screen = pygame.display.get_surface()
        self.screen_area = screen.get_rect()
        self.speed = 5
        self.direction = 1
        self.velocity = GRAVITY
        self.jumping = False
    def update(self):
        if pygame.key.get_pressed()[K_LEFT]:
            self.move(-0.2)
        if pygame.key.get_pressed()[K_RIGHT]:
            self.move(0.2)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.original_image, 1, 0)
        elif self.direction == 1:
            self.image = self.original_image
            
            
        #stop if you land on a non-white pixel
        try:
            if not self.is_on(WHITE):
                self.jumping = False
                self.velocity = 0
            else:
                self.velocity += GRAVITY

        except IndexError:
                self.velocity += GRAVITY
        #jump           
        if pygame.key.get_pressed()[K_UP] and not self.is_on(WHITE):
            self.jump()

        #die
        if self.is_on(RED):
            self.die()
        
        #move
        self.pos[1] += self.velocity
        self.rect.midbottom = (self.pos[0],self.pos[1])

    def move(self, dx):
        if dx>0:
            self.direction = 1
        elif dx<0:
            self.direction = -1
        #move horizontaly
        self.pos[0]+= self.speed * dx
        if self.rect.left < self.screen_area.left:
            self.pos[0] = self.screen_area.right - 10
        if self.rect.right > self.screen_area.right:
            self.pos[0] = self.screen_area.left + 10

    def jump(self):
        """How high?"""
        #move verticaly
        if not self.jumping:
            self.velocity = -3
            self.jumping = True

    def is_on(self, color):
        """tells whether the player is standing on a certain colored pixel"""
        value = False
        try:
            bottom_px = (self.rect.centerx,self.rect.bottom+1)
            value = self.level.get_at(bottom_px) == color
        except IndexError:
            if color == WHITE:
                value = True
            else:
                value = False
        finally:
            return value
            
    def die(self):
        self.kill()
        font = pygame.font.Font(None, 36)
        text = font.render("YOU DIED!!!", 1, (10, 10, 10))
        textpos = text.get_rect()
        self.level.blit(text, textpos)

def pause():
    pausing = True
    while pausing:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                pausing = False
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Fun Game')
    pygame.mouse.set_visible(1)

    background = pygame.Surface(SCREEN_SIZE)
    level = 1
#create background
    draw_bg(background, screen, "level"+str(level)+".png")

    clock = pygame.time.Clock()
    player = Player(background)
    allsprites = pygame.sprite.RenderPlain((player))

#Main Loop
    going = True
    while going:
        clock.tick(200)

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

        if player.is_on(YELLOW):
            write("Good Job!", screen, 400, 100, color=(0,255,0))
            write("Level "+str(level)+" completed", screen,
                  400, 130, color=(0,255,0))
            write("Press Enter To Continue", screen, 400,
                  160, size = 20, color=(0,255,0))
            pause()
            player.kill()
            pause()
            level+=1
            draw_bg(background, screen, "level"+str(level)+".png")
            player = Player(background)
            allsprites = pygame.sprite.RenderPlain((player))

    pygame.quit()


#Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
