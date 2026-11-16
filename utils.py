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

def get_time_passed(seconds):
    years = int(seconds // 3.154e7)
    seconds %= 3.154e7
    months = int(seconds // 2.628e6)
    seconds %= 2.628e6
    days = int(seconds // 86400)
    seconds %= 86400
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = round(seconds / 60, 1)
    seconds %= 60
 #   seconds = seconds // 1

    final_str = f"{years} years {months} months {days} days {hours} hours {minutes} minutes passed"
    return final_str