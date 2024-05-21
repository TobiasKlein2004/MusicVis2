import math
import pygame


class Ball():
    def __init__(self, surface, position=(200, 50), radius=10, world=[]) -> None:
        self.surface = surface
        self.windowWidth, self.windowHeight = surface.get_width(), surface.get_height()
        self.x_pos, self.y_pos = position
        self.worldOffset = position
        self.x_velocity = 0
        self.y_velocity = 0
        self.gravity = 4
        self.radius = radius
        # world is a list of all boxes
        self.world = world
        # after a collsion the ball cant register another for n frames
        self.collisionTimeout = 10
        self.framesSinceCollsion = self.collisionTimeout + 1
        # Debug - - - - - - - 
        self.LifeTime = 0 # Frames since start
        self.pastPositions = []

    def calcAngle(self) -> float:
        Vx, Vy = self.x_velocity, self.y_velocity*-1  # *-1 because growing y means down not up
        return math.degrees(math.atan2(Vx,Vy))


    def samplePoints(self) -> list[tuple]:
        #   resolution: number of points to ssample on the edge
        resolution = 12
        degree_per_point = 360 // resolution

        points = [(
            self.x_pos + self.radius * math.cos(math.radians(i)), 
            self.y_pos - self.radius * math.sin(math.radians(i))
            ) for i in range(0, 360, degree_per_point)]
        
        # draw points
        # for point in points:
        #     pygame.draw.circle(self.surface, (255,0,0), (point[0], point[1]), 1)

        return points


    def checkCollision(self):
        for box in self.world:
            if box.checkCollision(self.samplePoints()) == True: return box
        return False
    

    def bounce(self, e, theta):
        v_normal = self.x_velocity * math.sin(theta) + self.y_velocity * math.cos(theta)
        v_parallel = self.x_velocity * math.cos(theta) - self.y_velocity * math.sin(theta)
        v_normal = -e * v_normal

        self.x_velocity = v_parallel * math.cos(theta) + v_normal * math.sin(theta)
        self.y_velocity = -v_parallel * math.sin(theta) + v_normal * math.cos(theta)


    def updatePhysics(self, deltaTime) -> None:
        self.y_velocity += self.gravity * deltaTime

        # Handle Collision
        box = self.checkCollision()
        if box and self.framesSinceCollsion > self.collisionTimeout:
            print(box.rotation)
            self.framesSinceCollsion = 0
            bouncePower = 7
            theta = math.radians(box.rotation - 90)
            self.y_velocity += math.sin(theta) * bouncePower
            self.x_velocity += math.cos(theta) * bouncePower

        self.framesSinceCollsion += 1
        self.y_pos += self.y_velocity
        self.x_pos += self.x_velocity
        self.worldOffset = (self.x_pos - self.windowWidth//2, 
                            self.y_pos - self.windowHeight//2)


    def draw(self) -> None:
        # Make true for player centric
        if True:
            pygame.draw.circle(self.surface, (255,255,255), (self.windowWidth//2, self.windowHeight//2), self.radius)
        else:
            pygame.draw.circle(self.surface, (255,255,255), (self.x_pos, self.y_pos), self.radius)
        self.samplePoints()
        self.debugDraw()
    

    def debugDraw(self) -> None:
        self.LifeTime += 1
        if self.LifeTime % 5 == 0:
            self.pastPositions.append((self.x_pos, self.y_pos))
        for point in self.pastPositions:
            # Make true for player centric
            if True:
                point = (point[0]-self.worldOffset[0], point[1]-self.worldOffset[1])
            pygame.draw.circle(self.surface, (0,255,0), (point[0], point[1]), 1)


#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Box():
    def __init__(self, x, y, width, height, rotation, surface, color=(255,0,255)) -> None:
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.rotationRadians = math.radians(-rotation)

        # Rotation is direction of normal

        self.points = []
        # r = Distance from center to one of the corners 
        radius = math.sqrt((width/2)**2 + (height/2)**2)
        # a = angle to the bottom left corner with respect to the x axis
        angle = math.atan2(height/2, width/2)
        # Transform that angle to reach each corner of the rectangle.
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        # Calculate the coordinates of each point.
        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + self.rotationRadians)
            x_offset = radius * math.cos(angle + self.rotationRadians)
            self.points.append((x + x_offset, y + y_offset))


    def checkCollision(self, points: list[tuple]) -> bool:
        # points:           List of tupels of x,y coordinates [(x,y),(x,y)]
        #                   These are the points we want to check for collision
        # rect_center:      Center of the rectangle we want to check
        # rect_rotation:    Normal Angle of rect in degrees

        center = (self.x, self.y)

        # Translate the system
        points = [(point[0]-center[0], point[1]-center[1]) for point in points]

        # cancel out the rotation of the rect by rotation the points in the opposite direction
        points = [(
            point[0] * math.cos(-self.rotationRadians) + point[1] * math.sin(-self.rotationRadians),
            -point[0] * math.sin(-self.rotationRadians) + point[1] * math.cos(-self.rotationRadians)
        ) for point in points
        ]

        collisions = []
        # Check if any one of the points is in the rectangel
        for point in points:
            collisions.append(abs(point[0]) <= self.width / 2 and abs(point[1]) <= self.height / 2)

        if True in collisions: return True
        return False


    def draw(self, worldOffset) -> None:
        points = self.points
        # Make true for player centric
        if True:
            points = [(point[0]-worldOffset[0], point[1]-worldOffset[1]) for point in self.points]
        pygame.draw.polygon(self.surface, self.color, points)


#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Line():
    def __init__(self, surface, function) -> None:
        self.surface = surface
        self.function = function
    
    def draw(self, worldOffset, sampleRate=1, sampleRange=50):
        points = []
        for x in range(-sampleRange, sampleRange, sampleRate):
            points.append((x + self.surface.get_width()//2, 
                           self.function(x) + self.surface.get_height()//2))
        # for point in points:
        #     pygame.draw.circle(self.surface, (0,255,0), (point[0], point[1]), 1)
        for i in range(len(points)-1):
            pygame.draw.line(self.surface, (0, 255, 0), points[i], points[i+1])