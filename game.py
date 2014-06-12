import os, pygame
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#gravity is 10!!!!!!!!!!! ALWAYS!
GRAVITY = 10

SCREEN_SIZE = (800,400)

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

class Player(pygame.sprite.Sprite):
    """A guy who moves around the screen"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('person.png', -1)
        self.original_image = self.image
        self.pos = [200,0]
        screen = pygame.display.get_surface()
        self.screen_area = screen.get_rect()
        self.speed = 5
        self.direction = 1
        self.velocity = GRAVITY
        self.jumping = False
    def update(self):
        if pygame.key.get_pressed()[K_LEFT]:
            self.move(-1)
        if pygame.key.get_pressed()[K_RIGHT]:
            self.move(1)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.original_image, 1, 0)
        elif self.direction == 1:
            self.image = self.original_image
            
            
        if self.rect.bottom > self.screen_area.bottom:
            self.velocity = 0
            self.pos[1] = self.screen_area.bottom - 25
            self.jumping = False
        else:
            self.velocity += GRAVITY / 9

        if pygame.key.get_pressed()[K_UP]:
            self.jump()
            
        self.pos[1] += self.velocity
        
        self.rect.center = (self.pos[0],self.pos[1])
    def move(self, dx):
        if dx>0:
            self.direction = 1
        elif dx<0:
            self.direction = -1
        #move horizontaly
        self.pos[0]+= self.speed * dx
        if self.rect.right < self.screen_area.left:
            self.pos[0] = self.screen_area.right - 5
        if self.rect.left > self.screen_area.right:
            self.pos[0] = self.screen_area.left + 5

    def jump(self):
        """How high?"""
        #move verticaly
        if not self.jumping:
            self.velocity = -15
            self.jumping = True

    
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Fun Game')
    pygame.mouse.set_visible(1)
#create background    
    background_img = pygame.image.load(os.path.join(data_dir, "level.png")).convert()
    background = pygame.Surface(SCREEN_SIZE)
    background.blit(background_img, (0, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()


    clock = pygame.time.Clock()
    player = Player()
    allsprites = pygame.sprite.RenderPlain((player))

#Main Loop
    going = True
    while going:
        clock.tick(60)

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

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
