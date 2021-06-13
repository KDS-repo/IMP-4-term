from tools.packager import pack, unpack
from yaml import load, dump


class YamlParser:
    def dumps(self, obj):
        p = pack(obj)
        return dump(p, indent = 4)

    def dump(self, obj, fp):
        return fp.write(self.dumps(obj))

    def loads(self, s):
        l = load(s)
        return unpack(l)

    def load(self, fp):
        return self.loads(fp.read())

    def unpack(self, fp):
        return load(fp.read())

    def pack(self, obj, fp):
        return fp.write(dump(obj))
