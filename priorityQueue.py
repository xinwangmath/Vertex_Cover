import heapq
import itertools

# priority queue data structure
class indexMinPQ:

        def __init__(self):
                self._N = 0
                self._pq = []
                self._value_finder = {}
                self._REMOVED = "<removed_task>"
                self._counter = itertools.count()

        def isEmpty(self):
                return self._N == 0

        def size(self):
                return self._N

        def push(self, value, key = 0):
                """push a new element into the priority queue"""
                if value in self._value_finder:
                        self.remove_value(value)
                count = next(self._counter)
                entry = [key, count, value]
                self._value_finder[value] = entry
                heapq.heappush(self._pq, entry)
                self._N = self._N+1

        def changeKey(self, value, newkey):
                if value in self._value_finder:
                        self.remove_value(value)
                        count = next(self._counter)
                        entry = [newkey, count, value]
                        self._value_finder[value] = entry
                        heapq.heappush(self._pq, entry)
                        self._N = self._N+1
                else:
                        raise KeyError('value not in the priority queue')

        def remove_value(self, value):
                """mark an existing value as REMOVED, Raise KeyError if not found."""
                entry = self._value_finder.pop(value)
                entry[-1] = self._REMOVED
                self._N = self._N - 1

        def pop(self):
                """remove and return the value with the minimal key"""
                while self._pq:
                        key, count, value = heapq.heappop(self._pq)
                        if value is not self._REMOVED:
                                del self._value_finder[value]
                                self._N = self._N - 1
                                return value
                raise KeyError('pop from an empty priority queue')
