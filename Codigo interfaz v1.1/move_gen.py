from random import uniform, randint, betavariate
import numpy as np

import parametros as p


class MoveGen:
    def __init__(self):
        self.move_dist: float
        self.dir = np.ones(2) / np.sqrt(2)
        self.pix_over_cm: float
        self.x_range: list
        self.y_range: list
        self.mode = "movie"
        self.mode_actions = {
            "movie": self.movie,
            "random": self.random,
            "fly": self.fly,
            "smart_fly": self.smart_fly
        }

        self.random_max_counter_limits: tuple
        self.fly_max_counter_limits: tuple
        self.fly_max_angle: int
        self.sfly_max_counter_limits: tuple
        self.sfly_max_beta_value: float
        self.sfly_max_angle: int

        self.random_counter = 0
        self.fly_counter = 0
        self.sfly_counter = 0

    def set_ranges(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range

    def set_vel_dist(self, vel: float, dist_cm: float, dist_pix: int):
        if dist_cm != 0:
            self.pix_over_cm = dist_pix / dist_cm
            self.move_dist = vel * p.PERIOD * self.pix_over_cm

    def restart_movement(self):
        if self.mode == "movie":
            self.dir = self.random_dir()

        elif self.mode == "random":
            self.dir = self.random_dir()
            self.random_counter = 0
            self.random_max_counter = randint(*self.random_max_counter_limits)

        elif self.mode == "fly":
            self.dir = self.random_dir()
            self.fly_counter = 0
            self.fly_max_counter = randint(*self.fly_max_counter_limits)

        elif self.mode == "smart_fly":
            self.dir = self.random_dir()
            self.sfly_counter = 0
            self.sfly_max_counter = randint(*self.sfly_max_counter_limits)

    def random_dir(self) -> np.ndarray:
        angle = uniform(-np.pi / 2, np.pi / 2)
        dir = np.ones(2)
        dir[0] = np.tan(angle)
        norm = np.sqrt(dir[0] ** 2 + dir[1] ** 2)
        dir = np.array([dir[0] / norm, dir[1] / norm])
        if randint(0, 1) == 1:
            dir = - dir
        return dir

    def rotate_dir(self, angle: float):
        vx = self.dir[0]
        vy = self.dir[1]
        vx_new = np.cos(angle) * vx - np.sin(angle) * vy
        vy_new = np.sin(angle) * vx + np.cos(angle) * vy
        self.dir = np.array([vx_new, vy_new])

    def random_step(self, ref_pos: list, dist_cm: float) -> list:
        self.pos = np.array(ref_pos)
        ready = False
        while not ready:
            ready = True
            self.dir = self.random_dir()
            move_dist = dist_cm * self.pix_over_cm
            potential_pos = self.pos + self.dir * move_dist
            if (potential_pos[0] > self.x_range[1] or
                    potential_pos[0] < self.x_range[0]):
                ready = False
            if (potential_pos[1] > self.y_range[1] or
                    potential_pos[1] < self.y_range[0]):
                ready = False

        new_pos = potential_pos
        return list(new_pos)

    def move(self, ref_pos: list) -> list:
        return self.mode_actions[self.mode](ref_pos)

    def movie(self, ref_pos: list) -> list:
        self.pos = np.array(ref_pos)
        potential_pos = self.pos + self.dir * self.move_dist
        new_pos = self.reflect(potential_pos)
        return list(new_pos)

    def random(self, ref_pos: list) -> list:
        self.pos = np.array(ref_pos)
        if self.random_counter >= self.random_max_counter:
            self.restart_movement()
        self.random_counter += 1
        potential_pos = self.pos + self.dir * self.move_dist
        new_pos = self.reflect(potential_pos)
        return list(new_pos)

    def fly(self, ref_pos: list) -> list:
        self.pos = np.array(ref_pos)
        if self.fly_counter >= self.fly_max_counter:
            angle = uniform(- self.fly_max_angle * np.pi / 180,
                            self.fly_max_angle * np.pi / 180)
            self.rotate_dir(angle)
            self.fly_counter = 0
            self.fly_max_counter = randint(*self.fly_max_counter_limits)
        self.fly_counter += 1
        potential_pos = self.pos + self.dir * self.move_dist
        new_pos = self.reflect(potential_pos)
        return list(new_pos)

    def smart_fly(self, ref_pos: list) -> list:
        self.pos = np.array(ref_pos)
        if self.sfly_counter >= self.sfly_max_counter:
            center_vect = np.array([sum(self.x_range) / 2 - self.pos[0],
                                    sum(self.y_range) / 2 - self.pos[1]])
            distance = np.sqrt(center_vect[0] ** 2 + center_vect[1] ** 2)
            theta = np.abs(center_vect)
            center_vect_norm = center_vect / distance
            sign = np.sign(np.cross(center_vect_norm, self.dir))
            theta = np.arccos(np.dot(center_vect_norm, self.dir)) * 180 / np.pi
            theta = theta * sign
            alpha = self.beta_scale(distance, - theta)
            beta = self.beta_scale(distance, theta)
            random_angle = betavariate(alpha, beta) * 2 * self.sfly_max_angle \
                - self.sfly_max_angle
            self.rotate_dir(random_angle * np.pi / 180)
            self.sfly_counter = 0
            self.sfly_max_counter = randint(*self.sfly_max_counter_limits)

        self.sfly_counter += 1
        potential_pos = self.pos + self.dir * self.move_dist
        new_pos = self.reflect(potential_pos)
        return list(new_pos)

    def beta_scale(self, distance: float, theta: float):
        distance_norm = 2 * distance / np.sqrt(
            sum(self.x_range) ** 2 + sum(self.y_range) ** 2)
        if theta > 0:
            return p.SFLY_MIN_BETA_VALUE + distance_norm * \
                (self.sfly_max_beta_value - p.SFLY_MIN_BETA_VALUE) * \
                theta / 180
        else:
            return p.SFLY_MIN_BETA_VALUE

    def reflect(self, potential_pos: np.array) -> np.array:
        if (potential_pos[0] > self.x_range[1] or
                potential_pos[0] < self.x_range[0]):
            self.dir[0] = - self.dir[0]

        if (potential_pos[1] > self.y_range[1] or
                potential_pos[1] < self.y_range[0]):
            self.dir[1] = - self.dir[1]

        new_pos = self.pos + self.dir * self.move_dist
        return new_pos
