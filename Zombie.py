from math import sqrt

from Human import Human


class Zombie(Human):
    """This is the Predator that will move around the area. y-axis points DOWN"""
    zombiePosX = 0
    zombiePosY = 0

    def __init__(self, rect=None, color=None, deathSound=None):
        Human.__init__(self, rect, color, deathSound)


    def swim(self, area, mousePos_x, mousePos_y):
        """Using my xVel and yVel values, take a step, so long as we don't swim out of bounds."""

        if mousePos_x <= 0: 
            zombiePosX = 0
        elif mousePos_x >= area.width:
            zombiePosX = area.width
        else:
            zombiePosX = mousePos_x

        if mousePos_y <= 0:
            zombiePosY = 0
        elif mousePos_y >= area.height:
            zombiePosY = area.height
        else:
            zombiePosY = mousePos_y

        #print("x: "+str(pozycja_ryby_x) + " y: "+str(pozycja_ryby_y))
        self.rect[0]=zombiePosX
        self.rect[1]=zombiePosY

        