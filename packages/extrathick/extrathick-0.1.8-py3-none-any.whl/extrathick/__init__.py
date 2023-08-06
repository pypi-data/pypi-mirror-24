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
