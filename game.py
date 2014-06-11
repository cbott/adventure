import os, pygame
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

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
        self.pos = [10,10]
        screen = pygame.display.get_surface()
        self.screen_area = screen.get_rect()
        self.speed = 3
    def update(self):
        if pygame.key.get_pressed()[K_UP]:
            self.move(0,-1)
        if pygame.key.get_pressed()[K_DOWN]:
            self.move(0,1)
        if pygame.key.get_pressed()[K_LEFT]:
            self.move(-1,0)
        if pygame.key.get_pressed()[K_RIGHT]:
            self.move(1,0)

        self.rect.center = (self.pos[0],self.pos[1])
    def move(self, dx, dy):
        self.pos[0]+= self.speed * dx
        self.pos[1]+= self.speed * dy
        if self.rect.right < self.screen_area.left:
            self.pos[0] = self.screen_area.right - 5
        if self.rect.left > self.screen_area.right:
            self.pos[0] = self.screen_area.left + 5
        if self.rect.bottom < self.screen_area.top:
            self.pos[1] = self.screen_area.bottom - 5
        if self.rect.top > self.screen_area.bottom:
            self.pos[0] = self.screen_area.top + 5
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    pygame.display.set_caption('Fun Game')
    pygame.mouse.set_visible(0)
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((12, 55, 210))

#Display The Background
    screen.blit(background, (0, 0))
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
