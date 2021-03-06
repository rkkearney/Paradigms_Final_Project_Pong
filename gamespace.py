#!/usr/bin/env python3

import os, sys, math, time
import pygame
from pygame.locals import *
from random import randint

class GameSpace:
	def __init__(self):
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

		#self.clock = pygame.time.Clock()

	def main(self):
		#while 1:
		self.ball.move()
		
		# Print Score
		self.score1 = self.ourfont.render(str(self.player.points), False, (255, 255, 255))
		self.score2 = self.ourfont.render(str(self.opponent.points), False, (255, 255, 255))
		
		# Handle Moving 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self.player.tick()

		#self.opponent.rect.centery -= y
		#self.ball.xstep = xstep
		#self.ball.ystep = ystep
		
		# Blit to Screen
		self.screen.blit(self.background.image, self.background.rect)
		self.screen.blit(self.player.image, self.player.rect)
		self.screen.blit(self.opponent.image, self.opponent.rect)
		self.screen.blit(self.score1, (275, 30))
		self.screen.blit(self.score2, (340, 30))
		self.screen.blit(self.ball.image, self.ball.rect)

		# Check for and Handle Winner
		if self.player.points == 5:
			self.winner = self.ourfont.render("You Win!", False, (255, 255, 255))
			self.screen.fill(self.black)
			self.screen.blit(self.winner, (220, 150))
			pygame.display.update()
			time.sleep(3)
			break
		elif self.opponent.points == 5:
			self.winner = self.ourfont.render("Opponent Wins!", False, (255, 255, 255))
			self.screen.fill(self.black)
			self.screen.blit(self.winner, (150, 150))
			pygame.display.update()
			time.sleep(3)
			break

		pygame.display.update()
			#self.clock.tick(60)



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
		self.xstep = randint(10,15)
		self.ystep = randint(5,15)
		self.direction = randint(-1,1)
		if self.direction < 0:
			self.xstep *= self.direction
			self.ystep *= self.direction

	def move(self):
		if self.GS.player.rect.colliderect(self.rect) or self.GS.opponent.rect.colliderect(self.rect):
			#print("collision detected")
			self.xstep *= -1
			#self.ystep *= -1
		elif self.rect.centerx < 0:
			# give point to player 2
			self.GS.opponent.points += 1
			self.miss()
		elif self.rect.centerx > 640:
			# give point to player 1
			self.GS.player.points += 1
			self.miss()
		elif self.rect.centery < 20 or self.rect.centery > 460:
			self.ystep *= -1

		self.rect.centerx += self.xstep
		self.rect.centery += self.ystep

	def miss(self):
		time.sleep(1)
		self.rect.centerx = 320
		self.rect.centery = 240
		self.xstep = randint(10,15)
		self.ystep = randint(5,15)
		self.direction = randint(-1,1)
		if self.direction < 0:
			self.xstep *= self.direction
			self.ystep *= self.direction

	def tick(self):
		self.move()
		pass


if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
