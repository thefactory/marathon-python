import collections
import datetime

try:
    import json
except ImportError:
    import simplejson as json
import re

from ._compat import string_types


def is_stringy(obj):
    return isinstance(obj, string_types)


class MarathonJsonEncoder(json.JSONEncoder):

    """Custom JSON encoder for Marathon object serialization."""

    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return self.default(obj.json_repr())

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        if isinstance(obj, collections.Iterable) and not is_stringy(obj):
            try:
                return {k: self.default(v) for k, v in obj.items()}
            except AttributeError:
                return [self.default(e) for e in obj]

        return obj


class MarathonMinimalJsonEncoder(json.JSONEncoder):

    """Custom JSON encoder for Marathon object serialization."""

    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return self.default(obj.json_repr(minimal=True))

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        if isinstance(obj, collections.Iterable) and not is_stringy(obj):
            try:
                return {k: self.default(v) for k, v in obj.items() if (v or v in (False, 0))}
            except AttributeError:
                return [self.default(e) for e in obj if (e or e in (False, 0))]

        return obj


def to_camel_case(snake_str):
    words = snake_str.split('_')
    return words[0] + ''.join(w.title() for w in words[1:])


def to_snake_case(camel_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
