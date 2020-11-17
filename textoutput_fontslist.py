import pygame
from pygame.constants import (
    QUIT, K_ESCAPE, KEYDOWN, KEYUP, K_f, K_UP, K_DOWN
)
import os


class Settings:
    """Project global informations.

    This static class contains project global informations 
    like window size and file directories.
    """
    window_width = 1000
    window_height = 600

    @staticmethod
    def get_dim():
        return (Settings.window_width, Settings.window_height)


class TextSprite(pygame.sprite.Sprite):
    """Manager of one font example.
    """

    def __init__(self, fontname, fontsize=24, fontcolor=(255, 255, 255), text="abcdefghijklmnopqrstxyzßöäü0123456789"):
        """Constructor.

        Args:
            fontname (string): name of the font
            fontsize (int, optional): size of the font. Defaults to 24.
            fontcolor (tuple, optional): Color of the font. Defaults to (255, 255, 255).
            text (str, optional): Example text. Defaults to "abcdefghijklmnopqrstxyzßöäü0123456789".
        """
        super().__init__()
        self.text = text
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fontname = fontname
        self.font = pygame.font.Font(
            pygame.font.match_font(fontname), fontsize)
        self.create_image()

    def create_image(self):
        """Renders the text.

        Creates a bitmap by rendering the text according to
        the given parameter like size and color.
        """
        self.image = self.font.render(
            self.fontname+": "+self.text, True, self.fontcolor)
        self.rect = self.image.get_rect()


class FontList(pygame.sprite.Sprite):
    """One big bitmap with all font examples.
    """

    def __init__(self):
        """Constructor
        """
        super().__init__()
        self.offset = pygame.Rect((0, 0), Settings.get_dim())

    def create_image(self, width, height):
        """Creates the bis image.

        Args:
            width (int): width of the bitmap
            height (int): height of the bitmap
        """
        self.image_total = pygame.Surface((width, height))
        self.update(0)

    def update(self, delta):
        """Extracts the subimage.

        According to the offset only the visible part
        of the bitmap is created as the image attribute of the sprite.

        Args:
            delta (int): a positiv or negative number of pixel to move down or up.
        """
        if self.offset.top + delta >= 0:
            if self.offset.bottom + delta <= self.image_total.get_rect().height:
                self.offset.move_ip(0, delta)
            else:
                self.offset.bottom = self.image_total.get_rect().height
        else:
            self.offset.top = 0
        self.image = self.image_total.subsurface(self.offset)
        self.rect = self.image.get_rect()


if __name__ == '__main__':

    # Preparation
    os.environ['SDL_VIDEO_WINDOW_POS'] = "650, 40"

    #pylint: disable=no-member
    pygame.init()
    #pylint: enable=no-member
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(Settings.get_dim())

    fonts = pygame.font.get_fonts()
#    print(font)

    ts = []
    height = 0
    width = 0
    for name in fonts:
        try:
            t = TextSprite(name)
            height += t.rect.height
            width = t.rect.width if t.rect.width > width else width
            ts.append(t)
        except OSError as err:
            print(f"OS error {err}")
        except pygame.error as perr:
            print(f"Pygame error: {perr} with font {name}")

    l = FontList()
    l.create_image(width, height)
    vpos = 0
    for t in ts:
        l.image_total.blit(t.image, (0, vpos))
        vpos += t.rect.height

    # main loop
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_UP:
                    l.update(-Settings.window_height//3)
                if event.key == K_DOWN:
                    l.update(Settings.window_height//3)

        screen.fill((0, 0, 0))
        screen.blit(l.image, l.rect)
        pygame.display.flip()

    # bye bye
    #pylint: disable=no-member
    pygame.quit()
    #pylint: enable=no-member
