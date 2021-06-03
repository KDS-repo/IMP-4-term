from libs.json import jsonparser
from libs.yaml import yamlparser


class Serializator:
    def __init__(self):
        self.parsers = dict()

    def add_parser(self, format, parser):
        self.parsers[format.lower()] = parser

    def get_parser(self, format):
        parser = self.parsers.get(format.lower())
        if not parser:
            raise ValueError(format)
        return parser()


serializer = Serializator()
serializer.add_parser("JSON", jsonparser.JsonParser)
serializer.add_parser("Yaml", yamlparser.YamlParser)
