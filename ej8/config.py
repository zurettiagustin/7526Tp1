from singleton import Singleton

class Config(metaclass=Singleton):
    @property
    def population(self):
        return self._population

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta(self):
        return self._beta

    @property
    def mobile(self):
        return self._mobile

    @property
    def safety_time(self):
        return self._safety_time

    @property
    def reinfection(self):
        return self._reinfection

    @reinfection.setter
    def reinfection(self, x):
        self._reinfection = x

    @population.setter
    def population(self, x):
        self._population = x

    @alpha.setter
    def alpha(self, x):
        self._alpha = x

    @beta.setter
    def beta(self, x):
        self._beta = x

    @mobile.setter
    def mobile(self, x):
        self._mobile = x

    @safety_time.setter
    def safety_time(self, x):
        self._safety_time = x
