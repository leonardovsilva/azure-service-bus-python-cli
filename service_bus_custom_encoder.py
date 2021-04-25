import json


class ServiceBusCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_')]:
            try:
                data = getattr(obj, field)
                fields[field] = str(data)
            except Exception:
                fields[field] = None

        return fields
