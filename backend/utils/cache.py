from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: tuple) -> list:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return []
        
    def put(self, key: tuple, value: dict) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
        
    def contains(self, key: tuple) -> bool:
        return key in self.cache