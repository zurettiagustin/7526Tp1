class Timer:
    def __init__(self):
        self._frame = 0

    @property
    def frame(self):
        return self._frame

    def increment(self):
        self._frame += 1
