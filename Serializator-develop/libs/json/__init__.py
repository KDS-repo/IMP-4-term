from .jsonencode import JsonEncoder
from .jsondecode import JsonDecoder


def dumps(obj):
    return JsonEncoder().json_encode(obj)


def loads(obj):
    return JsonDecoder().json_decode(obj)
