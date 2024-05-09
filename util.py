import math 


def checkCollision(points: list[tuple], rect_center: tuple, rect_width: float, 
                   rect_height: float, rect_rotation: float):
    # points:           List of tupels of x,y coordinates [(x,y),(x,y)]
    #                   These are the points we want to check for collision
    # rect_center:      Center of the rectangle we want to check
    # rect_rotation:    Normal Angle of rect in degrees

    # Convert to radians
    rect_rotation = math.radians(-rect_rotation)

    # Translate the system
    points = [(point[0]-rect_center[0], point[1]-rect_center[1]) for point in points]

    # cancel out the rotation of the rect by rotation the points in the opposite direction
    points = [(
        point[0] * math.cos(-rect_rotation) + point[1] * math.sin(-rect_rotation),
        -point[0] * math.sin(-rect_rotation) + point[1] * math.cos(-rect_rotation)
    ) for point in points
    ]
    
    collisions = []
    # Check if any one of the points is in the rectangel
    for point in points:
        collisions.append(abs(point[0]) <= rect_width / 2 and abs(point[1]) <= rect_height / 2)
    
    if True in collisions: return True
    return False