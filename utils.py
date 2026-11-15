WIDTH, HEIGHT = 1250, 900

def find_largest(bodies):
    largest = 1
    for b in bodies:
        if b.radius >= largest: largest = b.radius

    return largest

def world_to_screen(position, camera_pos, zoom):
    x = (position[0] - camera_pos[0]) * zoom
    y = (position[1] - camera_pos[1]) * zoom

    return (int(WIDTH / 2 + x), int(HEIGHT / 2 + y))