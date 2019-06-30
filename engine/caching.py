

class PositionCache:

    __slots__ = ('_container', '_max_size', '_history')

    def __init__(self, max_size: int = 500_000):
        self._container = {}
        self._max_size = max_size
        self._history = []

    def add_to_cache(self, position: str, score: int):
        if position not in self._container:
            if len(self._container) < self._max_size:
                self._container[position] = score
                self._history.append(position)
            else:
                key = self._history.pop()
                self._container.pop(key)
                self._container[position] = score

    def get_position(self, key):
        return self._container.get(key)