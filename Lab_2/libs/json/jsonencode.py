class JsonEncoder:
    def __init__(self, tab="\t", crlf="\n"):
        self.nesting_level = 0
        self.tab = tab
        self.crlf = crlf
        self.joiner = "," + self.crlf

    def add_tab(self, level=-1):
        if level != -1:
            self.nesting_level = level
        return self.nesting_level * self.tab

    def dict_to_json(self, objs):
        bracket = self.json_brackets[type(objs)]
        if not objs:
            return bracket[0] + bracket[1]
        self.nesting_level += 1
        return (
            bracket[0]
            + self.crlf
            + self.joiner.join(
                [
                    str(
                        self.add_tab()
                        + self.json_encode(key)
                        + ": "
                        + self.json_encode(value)
                    )
                    for key, value in objs.items()
                ]
            )
            + self.crlf
            + self.add_tab(self.nesting_level - 1)
            + bracket[1]
        )

    def array_to_json(self, objs):
        bracket = self.json_brackets[type(objs)]
        if not objs:
            return bracket[0] + bracket[1]
        self.nesting_level += 1
        return (
            bracket[0]
            + self.crlf
            + self.joiner.join(
                [str(self.add_tab() + self.json_encode(obj)) for obj in objs]
            )
            + self.crlf
            + self.add_tab(self.nesting_level - 1)
            + bracket[1]
        )

    def primitive_to_json(self, obj):
        return str(obj)

    def bool_to_json(self, obj):
        return str(obj).lower()

    def none_to_json(self, obj):
        return "null"

    def string_to_json(self, obj):
        bracket = self.json_brackets[type(obj)]
        return bracket[0] + str(obj) + bracket[1]

    def json_encode(self, obj):
        if type(obj) in self.json_type:
            return self.json_type[type(obj)](self, obj)
        else:
            raise ValueError("can't encode: ", type(obj))

    json_brackets = {
        dict: ("{", "}"),
        list: ("[", "]"),
        tuple: ("[", "]"),
        str: ('"', '"'),
    }

    json_type = {
        int: primitive_to_json,
        float: primitive_to_json,
        str: string_to_json,
        bool: bool_to_json,
        dict: dict_to_json,
        list: array_to_json,
        tuple: array_to_json,
        type(None): none_to_json,
    }
