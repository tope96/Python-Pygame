#!/usr/bin/env python
import sys
from random import random

import pygame
from pygame.locals import *

import Alive, Zombie
import physics

redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)

NUMBER_OF_alive = 13
NUMBER_OF_zombieS = 1

class Area:
    x = 0
    y = 0

    def __init__(self, width=800, height =600):
        """Initialize pygame."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Area')
        self.chewSound = pygame.mixer.Sound('./chew.wav')

    def draw_direction_line(self, human):
        """Given a human sprite, draw a line of motion using xVel and yVel."""
        startX = human.rect[0]
        startY = human.rect[1]
        endX = (human.rect[0] + 2*human.xVel)
        endY = (human.rect[1] + 2*human.yVel)
        pygame.draw.line(self.screen, blackColor, (startX, startY), (endX, endY), 3)


    def load_sprites(self):
        """Load all of the human sprites."""
        self.zombie_group = pygame.sprite.Group()
        for i in range(NUMBER_OF_zombieS):
            self.zombie_group.add(Zombie.Zombie(rect=pygame.Rect(random()*self.width, random()*self.height, 30, 30), color='zombie2.png'))
        
        self.alive_group = pygame.sprite.Group()
        for i in range(NUMBER_OF_alive):
            self.alive_group.add(Alive.Alive(rect=pygame.Rect(random()*self.width, random()*self.height, 10, 10), deathSound=self.chewSound, color='brain4.png'))
        #for i in range(NUMBER_OF_alive):
        #    self.alive_group.add(alive.alive(rect=pygame.Rect(random()*self.width, random()*self.height, 10, 10), deathSound=self.chewSound, color=redColor))

    def main_loop(self):
        """The main loop for drawing into the area."""
        fpsClock = pygame.time.Clock()
        self.load_sprites()

        while True:
            #self.screen.fill(blueColor)
            charRect = pygame.Rect((0,0),(800, 600))
            
            charImage = pygame.image.load("rsz_background.jpg")
            charImage = pygame.transform.scale(charImage, charRect.size)
            charImage = charImage.convert()
            self.screen.blit(charImage, charRect)
            self.zombie_group.draw(self.screen)
            self.alive_group.draw(self.screen)

            # Go through a list of all Event objects that happened since the last get()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT)) # Create an event
                elif event.type == pygame.MOUSEMOTION:
                        # gets the mouse position
                        self.x, self.y = pygame.mouse.get_pos()
            # Update the human velocities
           
            for alive in self.alive_group.sprites():
                alive.update_velocity(area=self)

            # Move human                
            for zombie in self.zombie_group.sprites():
                zombie.swim(area=self,mousePos_x=self.x,mousePos_y=self.y)                
            for alive in self.alive_group.sprites():
                alive.swim(area=self)

            # Draw direction arrows
            #for zombie in self.zombie_group.sprites():
            #    self.draw_direction_line(zombie)
            #for human in self.alive_group.sprites():
            #    self.draw_direction_line(human)

            # Check for all colisions among zombies and human
            spriteHitList = pygame.sprite.groupcollide(self.zombie_group, self.alive_group, False, False, collided=physics.human_collision)

            


                

            # Draw new window to the screen.
            pygame.display.update()
            fpsClock.tick(30)   # Wait long enough so fps <= 30.


def main():
    area = Area()
    area.main_loop()

if __name__ == "__main__":
    main()