import numpy as np

class Map:
    _MAP_SIZE = 100  # meters.
    _CELL_SIZE = 0.4  # meters.

    def __init__(self):
        self._init_cells()

    def _init_cells(self):
        self._cells = [[None] * int(self._MAP_SIZE / self._CELL_SIZE)] *\
                       int(self._MAP_SIZE / self._CELL_SIZE)

    def real_position(self, position):
        return position * self._CELL_SIZE

    def assign_cell(self, person):
        position = self._random_free_position()
        self._cells[position.item(0)][position.item(1)] = person
        person.position = position

    def cell(self, position):
        return self._cells[position.item(0)][position.item(1)]

    def move(self, person, new_position):
        self._cells[person.position.item(0)][person.position.item(1)] = None
        self._cells[new_position.item(0)][new_position.item(1)] = person

    def is_valid_position(self, position):
        return not (self._is_out_of_bounds(position) or
                    self._is_occupied(position))

    def should_be_infected(self, position, radius=5):
        for dir_x in range(-radius, radius + 1):
            for dir_y in range(-radius, radius + 1):
                new_position = np.add(position, np.array([dir_x, dir_y]))

                if (not self._is_out_of_bounds(new_position) and
                        self._is_occupied(new_position)):
                    if self.cell(new_position).infected:
                        return True

        return False

    def _random_free_position(self):
        while True:
            start_x = np.random.randint(0, len(self._cells) + 1)
            start_y = np.random.randint(0, len(self._cells) + 1)
            for pos_x in range(start_x, len(self._cells)):
                for pos_y in range(start_y, len(self._cells)):
                    if self._cells[pos_x][pos_y] is None:
                        return np.array([pos_x, pos_y])

    def _is_occupied(self, position):
        return self.cell(position) is not None

    def _is_out_of_bounds(self, position):
        return ((position.item(0) < 0 or position.item(0) >= len(self._cells)) or
                (position.item(1) < 0 or position.item(1) >= len(self._cells)))
