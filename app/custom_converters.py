from bson import ObjectId
from werkzeug.routing import BaseConverter
import json

class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)
        except:
            raise ValueError(f'{value} is not a valid ObjectId')

    def to_url(self, value):
        return str(value)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
