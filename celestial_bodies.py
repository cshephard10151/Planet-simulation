from math import sqrt, atan2, cos, sin, degrees

G = 6.67e-11

class body:
    def __init__(self, name = 'planet X', coordinates = (0, 0), mass = 0, radius = 1):
        self.name = name
        self.position = [coordinates[0], coordinates[1]]
        self.mass = mass
        self.radius = radius
        self.velocity = [0, 0]

    def calculate_dist(self, other):
        dist = sqrt((other.position[1] - self.position[1]) ** 2 + (other.position[0] - self.position[0]) ** 2)
        if dist == 0:
            return 1
        return dist

    def calculate_pull(self, other):
        distance = self.calculate_dist(other)
        force = G * (self.mass * other.mass) / (distance ** 2)
        return force

    def get_dir(self, other):
        dir = atan2((other.position[1] - self.position[1]), (other.position[0] - self.position[0]))
        return dir

    def update_velocity(self, other, dt):
        other_dir = self.get_dir(other)
        force = self.calculate_pull(other)
        accel = force / self.mass
        self.velocity[0] += accel * cos(other_dir) * dt
        self.velocity[1] += accel * sin(other_dir) * dt

    def update_position(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def update(self, other, dt):
        self.update_velocity(other, dt)
        self.update_position(dt)
