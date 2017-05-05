#!/usr/bin/env python3
# Listener
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor

import os, sys, math
import pygame
from pygame.locals import *

from connections import *

class GameSpace:
        def __init__(self):
            pygame.init()
	    pygame.key.set_repeat(1,50)
            self.connFact = HostConnFactory(self)
            reactor.listenTCP(40127, self.connFact)
            reactor.run()

	def main(self):

		self.size = self.width, self.height = 640, 480 
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size) 

		self.background = Background(self)
		#self.score = Score(self)
		#self.player1 = Player(self)
		#self.player2 = Player(self)
		#self.ball = Ball(self)
		
		self.clock = pygame.time.Clock()

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				#elif event.type == pygame.KEYDOWN:
					#key = pygame.key.get_pressed()
					#if key[pygame.K_SPACE]:
					#	pygame.display.update()
					#else:
					#	self.player.tick()
				#elif event.type == pygame.MOUSEMOTION:
					#self.player.tick()
			
			self.screen.blit(self.background.image, self.background.rect)
			#self.screen.blit(self.score.image, self.score.rect)
			#self.screen.blit(self.player1.image, self.player1.rect)
			#self.screen.blit(self.player2.image, self.player2.rect)
			#self.screen.blit(self.ball.image, self.ball.rect)

			pygame.display.update()
			self.clock.tick(60)
        #call to integrate data received
        #called from the connections protocol
        def addingData(self, data):
            #look up pickle
            pass

        def sendData(self, data):
            #send data before each tick 
            #call this from tick()
            #self.connFact.conn.send(_)
            pass


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
		#self.image = pygame.image.load("deathstar.png")
		#self.original_image = pygame.image.load("deathstar.png")
		#self.rect = self.image.get_rect()

	def move(self):
		key = pygame.key.get_pressed()
		step = 2

		#if key[pygame.K_UP]:
		#	self.rect.centery -= step
		#if key[pygame.K_DOWN]:
		#	self.rect.centery += step

	def tick(self):
		self.move()
		pass


class Ball(pygame.sprite.Sprite):
	def __init__(self, gs):
		self.GS = gs
		#self.image = pygame.image.load("laser2.png")
		#self.original_image = pygame.image.load("laser2.png")
		#self.rect = self.image.get_rect()
		#self.rect.centerx = self.GS.player.rect.centerx
		#self.rect.centery = self.GS.player.rect.centery

	def move(self):
		print("move ball")

	def tick(self):
		self.move()
		pass


class Score(pygame.sprite.Sprite):
	def __init__(self, gs):
		self.GS = gs
		#self.image = pygame.image.load("laser2.png")
		#self.original_image = pygame.image.load("laser2.png")
		#self.rect = self.image.get_rect()
		#self.rect.centerx = self.GS.player.rect.centerx
		#self.rect.centery = self.GS.player.rect.centery

	def update(self):
		print("change score")

	def tick(self):
		self.move()
		pass


if __name__ == '__main__':
	gs = GameSpace()
#	gs.main()
