try:
    import json
except ImportError:
    import simplejson as json


class MarathonJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Marathon object serialization."""
    def default(self, obj):
        if hasattr(obj, 'json_encode'):
            return obj.json_encode()
        else:
            return json.JSONEncoder.default(self, obj)
