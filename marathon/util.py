import collections
import datetime
import logging

try:
    import json
except ImportError:
    import simplejson as json
import re


def get_log():
    return logging.getLogger(__name__.split('.')[0])


class MarathonJsonEncoder(json.JSONEncoder):

    """Custom JSON encoder for Marathon object serialization."""

    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return self.default(obj.json_repr())

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        if isinstance(obj, collections.Iterable) and not isinstance(obj, str):
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

        if isinstance(obj, collections.Iterable) and not isinstance(obj, str):
            try:
                return {k: self.default(v) for k, v in obj.items() if (v or v in (False, 0))}
            except AttributeError:
                return [self.default(e) for e in obj if (e or e in (False, 0))]

        return obj


def to_camel_case(snake_str):
    words = snake_str.split('_')
    return words[0] + ''.join(w.capitalize() for w in words[1:])


def to_snake_case(camel_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


DATETIME_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%SZ',  # Marathon omits milliseconds when they would be .000
]


def to_datetime(timestamp):
    if (timestamp is None or isinstance(timestamp, datetime.datetime)):
        return timestamp
    else:
        for fmt in DATETIME_FORMATS:
            try:
                return datetime.datetime.strptime(timestamp, fmt).replace(tzinfo=datetime.timezone.utc)
            except ValueError:
                pass
        raise ValueError(f'Unrecognized datetime format: {timestamp}')
