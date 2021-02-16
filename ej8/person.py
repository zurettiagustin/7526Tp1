import numpy as np
from matplotlib.patches import Circle
from config import Config

class Person:
    _INFECT_RATIO = 0.65
    _SAFE_INFECT_RATIO = 0.15
    _MOVEMENTS = [-1, 1]
    _RADIUS = 0.5

    def __init__(self, current_map, timer, ax, movement_delay=0, infected=False):
        self._current_map = current_map
        self._config = Config()

        self._current_map.assign_cell(self)
        self._movement_delay = movement_delay
        self._current_movement_delay = movement_delay

        self._timer = timer

        self._was_infected = False
        self._infected = infected
        self._infected_delay = self._config.alpha
        self._current_infected_delay = self._config.alpha

        self._ax = ax
        self._circle = Circle(np.zeros(2), radius=self._RADIUS)
        self._ax.add_patch(self._circle)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, new_value):
        self._infected = new_value

    @property
    def circle(self):
        return self._circle

    def draw(self):
        self._circle.center = self._current_map.real_position(self._position)
        self._circle.set_color('red' if self._infected else 'blue')

    def loop(self):
        self._move()
        self._heal()

        if self._current_map.should_be_infected(self._position):
            self._infect()

    def _infect(self):
        if not self._config.reinfection and self._was_infected:
            return

        self._infected = np.random.rand() <= self._infect_ratio()

    def _infect_ratio(self):
        return (self._SAFE_INFECT_RATIO if self._timer.frame >= self._config.safety_time else self._INFECT_RATIO)

    def _heal(self):
        if not self._can_heal():
            return

        self._infected = not np.random.rand() <= self._config.beta

        if not self._infected and not self._was_infected:
            self._was_infected = True

    def _move(self):
        if not self._can_move():
            return

        step = np.random.choice(a=self._MOVEMENTS, size=2)
        new_position = np.add(self._position, step)

        if self._current_map.is_valid_position(new_position):
            self._current_map.move(self, new_position)
            self._position = new_position

    def _can_heal(self):
        if not self._infected:
            return False

        if self._current_infected_delay == 0:
            return True

        self._current_infected_delay -= 1
        can_heal = self._current_infected_delay == 0

        return can_heal

    def _can_move(self):
        if self._movement_delay == 0:
            return True

        self._current_movement_delay -= 1
        can_move = self._current_movement_delay == 0

        if can_move:
            self._current_movement_delay = self._movement_delay

        return can_move
