from __future__ import print_function, division
import sys

import pygame as pg

WIDTH = 320
HEIGHT = 240


class Station(pg.sprite.Sprite):

    def __init__(self, label, url, *args, **kwargs):
        pg.sprite.Sprite.__init__(self, *args, **kwargs)
        self.font = pg.font.Font(None, 24)
        self.label = label
        self.url = url

        # The sprite content *must* be named "image"!
        self.image = self.font.render(self.label, 1, (0, 255, 255))
        self.rect = self.image.get_rect()

    def __repr__(self):
        return "<Station %s>" % self.label

    def collides(self, target):
        "returns true if the station collides with the target"
        hitbox = self.rect.inflate(-5, -5)
        return hitbox.collidepoint(target)

    def update(self):
        pass

    def clicked(self, event):
        print("clicked", self, event)  # XXX debug print


class ControlButton(pg.sprite.Sprite):

    def __init__(self, size, *args, **kwargs):
        pg.sprite.Sprite.__init__(self, *args, **kwargs)
        self.__size = size
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect()

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, id(self))

    def collides(self, target):
        "returns true if the station collides with the target"
        hitbox = self.rect.inflate(-5, -5)
        return hitbox.collidepoint(target)

    def update(self):
        pass

    def clicked(self, event):
        print("clicked", self, event)  # XXX debug print


class ArrowButton(ControlButton):

    def __init__(self, size, *args, **kwargs):
        ControlButton.__init__(self, size, *args, **kwargs)
        padding = size // 10
        pg.draw.polygon(self.image, (255, 0, 0), [
            (padding, size // 2),
            (size - padding, padding),
            (size - padding, size - padding)
        ])


class Pira(object):

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption('pira')

        self.__screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.__bg = pg.Surface(self.__screen.get_size())
        self.__bg = self.__bg.convert()
        self.__stations = []

    @property
    def stations(self):
        return self.__stations

    @stations.setter
    def stations(self, value):
        offset = 0
        for station in value:
            station.rect.top += offset
            offset += 20
            self.__stations.append(station)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit(0)
            elif event.type == pg.QUIT:
                sys.exit(0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                for station in self.__stations:
                    if station.collides(event.pos):
                        station.clicked(event)

    def main(self):
        self.__bg.fill((0, 0, 20))
        self.__screen.blit(self.__bg, (0, 0))
        pg.display.flip()

        if not self.__stations:
            print("No stations set!", file=sys.stderr)

        allstations = pg.sprite.Group()
        allstations.add(self.__stations)

        controls = pg.sprite.Group()
        controls.add(ArrowButton(100))

        rb = ArrowButton(100)
        rb.image = pg.transform.flip(rb.image, True, False)
        rb.rect.left = 150
        controls.add(rb)

        clock = pg.time.Clock()
        while True:
            clock.tick(60)
            self.handle_events()
            self.__screen.blit(self.__bg, (0, 0))
            controls.draw(self.__screen)
            controls.update()
            allstations.draw(self.__screen)
            allstations.update()
            pg.display.flip()


app = Pira()
app.stations = [
    Station('Chronix Aggression', 'http://chronixradio.com'),
    Station('SomaFM', 'http://somafm.com'),
]
app.main()
