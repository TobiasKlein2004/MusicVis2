import math
import pygame


class Box():
    def __init__(self, x, y, width, height, rotation, surface, color=(255,0,255)) -> None:
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = math.radians(-rotation)

        # Rotation is direction of normal

        self.points = []
        # r = Distance from center to one of the corners 
        radius = math.sqrt((width/2)**2 + (height/2)**2)
        # a = angle to the bottom left corner with respect to the x axis
        angle = math.atan2(height/2, width/2)
        # Transform that angle to reach each corner of the rectangle.
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        # Convert rotation from degrees to radians.
        rot_radians = (math.pi / 180) * -1 * rotation
        # Calculate the coordinates of each point.
        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + rot_radians)
            x_offset = radius * math.cos(angle + rot_radians)
            self.points.append((x + x_offset, y + y_offset))


    def checkCollision(self, points: list[tuple]):
        # points:           List of tupels of x,y coordinates [(x,y),(x,y)]
        #                   These are the points we want to check for collision
        # rect_center:      Center of the rectangle we want to check
        # rect_rotation:    Normal Angle of rect in degrees

        center = (self.x, self.y)

        # Translate the system
        points = [(point[0]-center[0], point[1]-center[1]) for point in points]

        # cancel out the rotation of the rect by rotation the points in the opposite direction
        points = [(
            point[0] * math.cos(-self.rotation) + point[1] * math.sin(-self.rotation),
            -point[0] * math.sin(-self.rotation) + point[1] * math.cos(-self.rotation)
        ) for point in points
        ]

        collisions = []
        # Check if any one of the points is in the rectangel
        for point in points:
            collisions.append(abs(point[0]) <= self.width / 2 and abs(point[1]) <= self.height / 2)

        if True in collisions: return True
        return False

    def draw(self):
        pygame.draw.polygon(self.surface, self.color, self.points)