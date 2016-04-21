import json
import re

from marathon.util import to_camel_case, to_snake_case, MarathonJsonEncoder, MarathonMinimalJsonEncoder


class MarathonObject(object):

    """Base Marathon object."""

    def __repr__(self):
        return "{clazz}::{obj}".format(clazz=self.__class__.__name__, obj=self.to_json(minimal=False))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def json_repr(self, minimal=False):
        """Construct a JSON-friendly representation of the object.

        :param bool minimal: Construct a minimal representation of the object (ignore nulls and empty collections)

        :rtype: dict
        """
        if minimal:
            return {to_camel_case(k): v for k, v in vars(self).items() if (v or v is False or v == 0)}
        else:
            return {to_camel_case(k): v for k, v in vars(self).items()}

    @classmethod
    def from_json(cls, attributes):
        """Construct an object from a parsed response.

        :param dict attributes: object attributes from parsed response
        """
        return cls(**{to_snake_case(k): v for k, v in attributes.items()})

    def to_json(self, minimal=True):
        """Encode an object as a JSON string.

        :param bool minimal: Construct a minimal representation of the object (ignore nulls and empty collections)

        :rtype: str
        """
        if minimal:
            return json.dumps(self.json_repr(minimal=True), cls=MarathonMinimalJsonEncoder, sort_keys=True)
        else:
            return json.dumps(self.json_repr(), cls=MarathonJsonEncoder, sort_keys=True)


class MarathonResource(MarathonObject):

    """Base Marathon resource."""

    def __repr__(self):
        if 'id' in list(vars(self).keys()):
            return "{clazz}::{id}".format(clazz=self.__class__.__name__, id=self.id)
        else:
            return "{clazz}::{obj}".format(clazz=self.__class__.__name__, obj=self.to_json())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "{clazz}::".format(clazz=self.__class__.__name__) + str(self.__dict__)

# See:
# https://github.com/mesosphere/marathon/blob/2a9d1d20ec2f1cfcc49fbb1c0e7348b26418ef38/src/main/scala/mesosphere/marathon/api/ModelValidation.scala#L224
ID_PATTERN = re.compile(
    '^(([a-z0-9]|[a-z0-9][a-z0-9\\-]*[a-z0-9])\\.)*([a-z0-9]|[a-z0-9][a-z0-9\\-]*[a-z0-9])|(\\.|\\.\\.)$')


def assert_valid_path(path):
    """Checks if a path is a correct format that Marathon expects. Raises ValueError if not valid.

    :param str path: The app id.

    :rtype: str
    """
    if path is None:
        return
    # As seen in:
    # https://github.com/mesosphere/marathon/blob/0c11661ca2f259f8a903d114ef79023649a6f04b/src/main/scala/mesosphere/marathon/state/PathId.scala#L71
    for id in filter(None, path.strip('/').split('/')):
        if not ID_PATTERN.match(id):
            raise ValueError(
                'invalid path (allowed: lowercase letters, digits, hyphen, "/", ".", ".."): %r' % path)
    return path


def assert_valid_id(id):
    """Checks if an id is the correct format that Marathon expects. Raises ValueError if not valid.

    :param str id: App or group id.

    :rtype: str
    """
    if id is None:
        return
    if not ID_PATTERN.match(id.strip('/')):
        raise ValueError(
            'invalid id (allowed: lowercase letters, digits, hyphen, ".", ".."): %r' % id)
    return id
