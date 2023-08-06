import json
from decimal import Decimal


class JsonUtil:
    @staticmethod
    def decode_json(data):
        return json.loads(data)

    @staticmethod
    def encode_json(obj):
        class fakefloat(float):
            def __init__(self, value):
                self._value = value

            def __repr__(self):
                return str(self._value)

        def defaultencode(o):
            if isinstance(o, Decimal):
                # Subclass float with custom repr?
                return fakefloat(o)
            raise TypeError(repr(o) + " is not JSON serializable")

        return json.dumps(obj, default=defaultencode)
