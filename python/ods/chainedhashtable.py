import random

from utils import new_array
from arraystack import ArrayStack
from odsset import ODSSet

w = 32

class ChainedHashTable(ODSSet):
    def __init__(self, iterable=[]):
        self._initialize()
        self.add_all(iterable)
        
    def _initialize(self):
        self.d = 1
        self.t = self._alloc_table((1<<self.d))
        self.z = self.random_odd_int()
        self.n = 0

    def random_odd_int(self):
        return random.randrange(1<<w) | 1
            
    def clear(self):
        self.d = 1
        self.t = self._alloc_table((1<<self.d))
        self.n = 0
        
    def _alloc_table(self, s):
        return [ArrayStack() for _ in range(s)]
    
    def _resize(self):
        self.d = 1
        while (1 << self.d) <= self.n: self.d += 1
        self.n = 0
        old_t = self.t
        self.t = self._alloc_table(1<<self.d)
        for i in range(len(old_t)):
            for x in old_t[i]:
                self.add(x)
                    
    def size(self):
        return self.n
    
    def _hash(self, x):
        return ((self.z * hash(x)) % (1<<w)) >> (w-self.d)
    
    def add(self, x):
        if self.find(x) != None: return False
        if self.n+1 > len(self.t): self._resize()
        self.t[self._hash(x)].append(x)
        self.n += 1
        return True
    
    def remove(self, x):
        ell = self.t[self._hash(x)]
        for y in ell:
            if y == x:
                ell.remove_value(y)
                self.n -= 1
                if 3*self.n < len(self.t): self._resize() 
                return y
        return None 
        
    def find(self, x):
        for y in self.t[self._hash(x)]:
            if y == x:
                return y
        return None
    
    def __iter__(self):
        for ell in self.t:
            for x in ell:
                yield x
                
    def __str__(self):
        return str([x for x in self])
    
    def debug_print(self):
        print "len(t) = %d" % len(self.t)
        for ell in self.t:
            print ell,
        print
        


    