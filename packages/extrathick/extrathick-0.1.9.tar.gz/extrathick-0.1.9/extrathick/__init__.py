from steov import Anon

def anonify (obj):
    if isinstance(obj, dict):
        return Anon({k: anonify(v) for k, v in obj.items()})
    if isinstance(obj, (list, set, tuple)):
        return type(obj)(map(anonify, obj))
    return obj

def unanonify (obj):
    if isinstance(obj, Anon):
        obj = vars(obj)
    if isinstance(obj, dict):
        return {k: unanonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, set, tuple)):
        return type(obj)(map(unanonify, obj))
    return obj


def dictstat (st):
    return {attr: getattr(st, "st_"+attr) for attr in [
        "mode",
        "ino",
        "dev",
        "nlink",
        "uid",
        "gid",
        "size",
        "atime",
        "mtime",
        "ctime",
    ]}

def anonstat (st):
    return Anon(dictstat(st))



# http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized:
    """
    Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """
    def __init__ (self, function):
        self._function = function
        self._cache = dict()

    def __call__ (self, *args):
        import collections
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self._function(*args)
        if args in self._cache:
            return self._cache[args]
        else:
            value = self._cache[args] = self._function(*args)
            return value

    def reload (self):
        self._cache.clear()

    # TODO I don't understand this just yet. look up python descriptors
    def __get__ (self, obj, objtype):
        import functools
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
