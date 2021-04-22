import json


class ServiceBusCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_')]:
            data = getattr(obj, field)
            try:
                fields[field] = str(data)
            except TypeError:
                fields[field] = None

        return fields
