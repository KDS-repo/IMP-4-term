from .dumper import get_dump_obj
from .loader import get_load_obj


def pack(obj):
    return get_dump_obj(obj)


def unpack(obj):
    return get_load_obj(obj)
