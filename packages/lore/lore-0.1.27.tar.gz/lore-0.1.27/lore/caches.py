import hashlib
import os
import pickle

import lore
from lore.util import timer


class Cache(dict):
    def key(self, instance, caller, **kwargs):
        return '.'.join((
            instance.__module__,
            instance.__class__.__name__,
            caller.__code__.co_name,
            hashlib.sha1(str(kwargs).encode('utf-8')).hexdigest()
        ))


class PickleCache(Cache):
    def __init__(self, dir):
        self.dir = dir
        
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
    
    def __getitem__(self, key):
        if key in self:
            with timer('pickle cache read %s:' % key):
                with open(self._path(key), 'rb') as f:
                    return pickle.load(f)
        return None
    
    def __setitem__(self, key, value):
        with timer('pickle cache write %s:' % key):
            with open(self._path(key), 'wb') as f:
                pickle.dump(value, f)
    
    def __delitem__(self, key):
        os.remove(self._path(key))
    
    def __contains__(self, key):
        return os.path.isfile(self._path(key))
        
    def _path(self, key):
        return os.path.join(self.dir, key + '.pickle')


cache = Cache()
query_cache = PickleCache(os.path.join(lore.env.data_dir, 'query_cache'))


def cached(func):
    global cache
    return _cached(func, cache)


def query_cached(func):
    global query_cache
    return _cached(func, query_cache)


def _cached(func, store):
    def wrapper(self, **kwargs):
        if 'cache' in kwargs and not kwargs['cache']:
            return func(self, **kwargs)
        
        key = store.key(self, func, **kwargs)
        if key not in store:
            store[key] = func(self, **kwargs)
        return store[key]
    
    return wrapper
