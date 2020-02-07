import datetime
import decimal
import json


# Helper class to convert a DynamoDB item to JSON.
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(CustomJSONEncoder, self).default(o)
