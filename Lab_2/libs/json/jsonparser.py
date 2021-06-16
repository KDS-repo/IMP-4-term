from libs.json import dumps, loads
from tools.packager import pack, unpack


class JsonParser:
    def dumps(self, obj):
        p = pack(obj)
        return dumps(p)

    def dump(self, obj, fp):
        return fp.write(self.dumps(obj))

    def loads(self, s):
        l = loads(s)
        return unpack(l)

    def load(self, fp):
        return self.loads(fp.read())

    def unpack(self, fp):
        return loads(fp.read())

    def pack(self, obj, fp):
        return fp.write(dumps(obj))
