from math import sqrt

from Human import Human

ZONE_OF_REPULSION = 50
ZONE_OF_ALIGNMENT = 100
ZONE_OF_ATTRACTION = 400
ZONE_OF_WALL = 30
ZONE_OF_FEAR = 80

ATTRACTIVE_CONST = -11.0
REPULSIVE_CONST = 12.0
ALIGNMENT_CONST = 0.5
WALL_CONST = 2.0
FEAR_CONST = 4.0


class Alive(Human):
    """This is the human Sprite that will move around the area. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=None, deathSound=None):
        Human.__init__(self, rect, color, deathSound)
        Alive.count += 1
        self.aliveID = Alive.count
        self.MAX_SPEED_X = 9.0
        self.MAX_SPEED_Y = 9.0


    def calc_zombie_forces(self, zombieList):
        """Calculate the force of running away from zombies."""
        F_x, F_y = 0, 0
        if not zombieList:
            return F_x, F_y
        for zombie in zombieList:
            if self.behind_me(zombie):
                continue
            dx = self.rect[0] - zombie.rect[0]
            dy = self.rect[1] - zombie.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > ZONE_OF_FEAR or r == 0:
                continue
            F_x += FEAR_CONST * (dx / r)
            F_y += FEAR_CONST * (dy / r)
        return F_x, F_y


    def calc_attractive_forces(self, aliveList):
        """Calculate the attractive forces due to every other human.
        Return the force in the (x,y) directions."""
        F_x, F_y = 0, 0
        if not aliveList:
            return F_x, F_y
        for human in aliveList:
            if human.color != self.color:
                continue
            if self.behind_me(human):
                continue
            dx = self.rect[0] - human.rect[0]
            dy = self.rect[1] - human.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > ZONE_OF_ATTRACTION or r <= ZONE_OF_REPULSION:
                continue
            F_x += (ATTRACTIVE_CONST / r) * (dx / r)
            F_y += (ATTRACTIVE_CONST / r) * (dy / r)
        return F_x, F_y


    def calc_repulsive_forces(self, aliveList):
        """Calculate the repulsive force due to close by human.
        Return the force in (x,y) directions."""
        F_x, F_y = 0, 0
        if not aliveList:
            return F_x, F_y
        for human in aliveList:
            if self.behind_me(human):
                continue
            dx = self.rect[0] - human.rect[0]
            dy = self.rect[1] - human.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r == 0 or r > ZONE_OF_REPULSION:
                continue
            F_x += (REPULSIVE_CONST / r) * (dx / r)
            F_y += (REPULSIVE_CONST / r) * (dy / r)
        return F_x, F_y        


    def calc_alignment_forces(self, aliveList):
        """Calculate the alignment force due to other close human. human like to
        swim in the same direction as other human. Return the force in (x,y) directions."""
        F_x, F_y = 0, 0
        if not aliveList:
            return F_x, F_y
        for human in aliveList:
            if human.color != self.color:
                continue
            if self.behind_me(human):
                continue
            dx = self.rect[0] - human.rect[0]
            dy = self.rect[1] - human.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r < ZONE_OF_REPULSION or r > ZONE_OF_ALIGNMENT:
                continue
            F_x += human.xVel * (ALIGNMENT_CONST / r)
            F_y += human.yVel * (ALIGNMENT_CONST / r)
        return F_x, F_y                


    def calc_wall_forces(self, width, height):
        """Calculate the inward force of a wall, which is very short range. Either 0 or CONST."""
        F_x, F_y = 0, 0
        if self.rect[0] < ZONE_OF_WALL:
            F_x += WALL_CONST
        elif (self.rect[0]+self.rect[2]) > (width-ZONE_OF_WALL):
            F_x -= WALL_CONST
        if self.rect[1] < ZONE_OF_WALL:
            F_y += WALL_CONST
        elif (self.rect[1]+self.rect[3]) > (height-ZONE_OF_WALL):
            F_y -= WALL_CONST
        return F_x, F_y


    def update_velocity(self, area):
        """Update the humanes velocity based on forces from other human."""
        # Stay near other human, but not too close, and swim in same direction.
        aliveList = area.alive_group.sprites()
        aliveList.remove(self)
        attractiveForces = self.calc_attractive_forces(aliveList)
        repulsiveForces = self.calc_repulsive_forces(aliveList)
        alignmentForces = self.calc_alignment_forces(aliveList)

        # If a zombie is within 20 pixels, run away
        zombieList = area.zombie_group.sprites()
        zombieForces = self.calc_zombie_forces(zombieList)

        # Check the walls.
        wallForces = self.calc_wall_forces(area.width, area.height)

        # Calculate final speed for this step.
        allForces = [repulsiveForces, attractiveForces, alignmentForces, wallForces, zombieForces]
        for force in allForces:
            self.xVel += force[0]
            self.yVel += force[1]

        # Ensure human doesn't swim too fast.
        if self.xVel >= 0:
            self.xVel = min(self.MAX_SPEED_X, self.xVel)
        else:
            self.xVel = max(-self.MAX_SPEED_X, self.xVel)
        if self.yVel >= 0:
            self.yVel = min(self.MAX_SPEED_Y, self.yVel)
        else:
            self.yVel = max(-self.MAX_SPEED_Y, self.yVel)


    def swim(self, area):
        """Using my xVel and yVel values, take a step, so long as we don't swim out of bounds."""
        # Keep human in the window
        if self.rect[0]+self.xVel <= 0 or self.rect[0]+self.xVel >= area.width:
            dx = 0
        else:
            dx = self.xVel
        if self.rect[1]+self.yVel <= 0 or self.rect[1]+self.yVel >= area.height:
            dy = 0
        else:
            dy = self.yVel

        self.rect.move_ip(dx, dy)