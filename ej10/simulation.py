import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import math

from config import Config
from map import Map
from person import Person
from timer import Timer


class Simulation:
    _INITIAL_INFECTION_RATIO = 0.03

    _DISTRIBUTIONS = {
        'slow': 0.1,
        'normal': 0.2,
        'fast': 0.7
    }
    _MOVEMENT_DELAY = {
        'slow': 3,
        'normal': 1,
        'fast': 0,
        'immobile': math.inf
    }

    _FRAMES = 1000

    def __init__(self):
        self._config = Config()
        self._timer = Timer()
        self._current_map = Map()

        self._init_plt()

        self._init_persons()
        self._infect_persons()

        self._ok_count = []
        self._infected_count = []

    def animate(self):
        return ani.FuncAnimation(self._fig, self._run, init_func=self._render_circles,
                                 frames=self._FRAMES, interval=75,
                                 blit=True, repeat=True).to_html5_video()

    def statistics(self):
        _fig, axis = plt.subplots()

        axis.set(xlim=(0, self._FRAMES), ylim=(0, len(self._persons)))
        axis.set_xlabel('Tiempo (ciclos)')
        axis.set_ylabel('Cantidad de sanos e infectados')

        axis.plot(self._ok_count, label='Personas sanas')
        axis.plot(self._infected_count, label='Personas infectadas')
        axis.legend()

    def _render_circles(self):
        return list(map(lambda x: x.circle, self._persons))

    def _run(self, _i):
        self._timer.increment()

        random_persons = self._persons.copy()
        np.random.shuffle(random_persons)

        list(map(lambda x: x.loop(), random_persons))
        list(map(lambda x: x.draw(), random_persons))

        self._fetch_statistics()

        return self._render_circles()

    def _fetch_statistics(self):
        infected_count = sum(1 if x.infected else 0 for x in self._persons)
        ok_count = len(self._persons) - infected_count

        self._ok_count.append(ok_count)
        self._infected_count.append(infected_count)

    def _init_plt(self):
        self._fig, self._ax = plt.subplots()
        for side in ['top', 'bottom', 'left', 'right']:
            self._ax.spines[side].set_linewidth(2)
        self._ax.set_aspect('equal', 'box')
        self._ax.set_xlim(0, 100)
        self._ax.set_ylim(0, 100)

    def _init_persons(self):
        self._persons = []

        mobile_population = self._config.population * (self._config.mobile / 100)
        immobile_population = self._config.population - mobile_population

        populations = {
            'slow': int(mobile_population * self._DISTRIBUTIONS['slow']),
            'normal': int(mobile_population * self._DISTRIBUTIONS['normal']),
            'fast': int(mobile_population * self._DISTRIBUTIONS['fast']),
            'immobile': int(immobile_population)
        }

        for person_type, population in populations.items():
            for _i in range(population):
                self._persons.append(Person(self._current_map, self._timer, self._ax,
                                            movement_delay=self._MOVEMENT_DELAY[person_type],
                                            infected=False))

    def _infect_persons(self):
        total_infected = int(self._config.population * self._INITIAL_INFECTION_RATIO)

        for person in np.random.choice(self._persons, total_infected):
            person.infected = True
