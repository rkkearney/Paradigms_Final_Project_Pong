#!/usr/bin/env python
import os, sys, math, time
import pygame
import pickle
from pygame.locals import *
from random import randint
from Queue import Queue

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
#from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class ClientConnFactory(ClientFactory):        
    def buildProtocol(self, addr):
        self.addr = addr
        self.conn = GameSpace(addr)
        return self.conn

class GameSpace(Protocol):
    def __init__(self, addr):
        self.addr = addr
        self.queue = Queue()

        pygame.init()
        pygame.font.init()
        pygame.key.set_repeat(1,50)

        self.size = self.width, self.height = 640, 480 
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size) 

        self.background = Background(self)
        self.player = Player(self)
        self.opponent = Opponent(self)
        self.ball = Ball(self)
        
        self.ourfont = pygame.font.SysFont('Comic Sans MS', 70)

    def main(self):
        if not self.queue.empty():
            data = self.queue.get()
            self.opponent.rect.centery = data['centery']
            self.ball.xstep = (-1) * data['xstep']
            self.ball.ystep = data['ystep']

        self.ball.tick()
        
        # Print Score
        self.score1 = self.ourfont.render(str(self.player.points), False, (255, 255, 255))
        self.score2 = self.ourfont.render(str(self.opponent.points), False, (255, 255, 255))
        
        # Handle Moving 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.player.tick()
                self.sendData()

        # Blit to Screen
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.opponent.image, self.opponent.rect)
        self.screen.blit(self.score1, (275, 30))
        self.screen.blit(self.score2, (340, 30))
        self.screen.blit(self.ball.image, self.ball.rect)

        # Check for and Handle Winner
        if self.player.points == 2:
            self.winner = self.ourfont.render("You Win!", False, (255, 255, 255))
            self.screen.fill(self.black)
            self.screen.blit(self.winner, (220, 150))
            pygame.display.update()
            time.sleep(3)
            sys.exit()
        elif self.opponent.points == 2:
            self.winner = self.ourfont.render("Opponent Wins!", False, (255, 255, 255))
            self.screen.fill(self.black)
            self.screen.blit(self.winner, (150, 150))
            pygame.display.update()
            time.sleep(3)
            sys.exit()

        pygame.display.update()

    def connectionMade(self):
        print "connection 2 made"
        # run the game til events end it
        #self.main()
        looping = LoopingCall(self.main) #makes all the ticks?
        looping.start(1/60)

    def dataReceived(self, data):
        #add data to some function in gamspace
        #function called addingData
        data = pickle.loads(data)
        self.queue.put(data)
        pass

    def sendData(self):
        data = {}
        data['centery'] = self.player.rect.centery
        data = pickle.dumps(data)
        self.transport.write(data)

    def connectionLost(self, args):
        print "connection 2 lost"


class Background(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.GS = gs
        self.image = pygame.image.load("background.png")
        self.original_image = pygame.image.load("background.png")
        self.rect = self.image.get_rect()

    def tick(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.GS = gs
        self.image = pygame.Surface((20, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 25
        self.rect.centery = 240
        self.points = 0

    def move(self):
        key = pygame.key.get_pressed()
        step = 10

        if key[pygame.K_UP]:
            self.rect.centery -= step
            self.check()
        if key[pygame.K_DOWN]:
            self.rect.centery += step
            self.check()

    def check(self):
        if self.rect.centery > 430:
            self.rect.centery = 430
        elif self.rect.centery < 50:
            self.rect.centery = 50

    def tick(self):
        self.move()
        pass


class Opponent(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.GS = gs
        self.image = pygame.Surface((20, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 615
        self.rect.centery = 240
        self.points = 0

    def move(self, y):
        self.rect.centery -= y

    def tick(self, y):
        pass


class Ball(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.GS = gs
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 240
        self.xstep = 0
        self.ystep = 0


    def move(self):
        if self.rect.centerx < 25:
            # give point to player 2
            self.GS.opponent.points += 1
            self.miss()
        elif self.rect.centerx > 615:
            # give point to player 1
            self.GS.player.points += 1
            self.miss()

        self.rect.centerx += self.xstep
        self.rect.centery += self.ystep

        print str(self.rect.centerx) + "\t" + str(self.rect.centery)

    def miss(self):
        time.sleep(1)
        self.rect.centerx = 320
        self.rect.centery = 240
        self.xstep = randint(10,15)
        self.ystep = randint(5,15)
        self.direction = randint(-1,1)


    def tick(self):
        self.move()
        pass


if __name__ == '__main__':
    connFact = ClientConnFactory()
    reactor.connectTCP("ash.campus.nd.edu", 40127, connFact)
    reactor.run()
