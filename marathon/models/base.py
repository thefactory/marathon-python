import json

from marathon.util import to_camel_case, to_snake_case, MarathonJsonEncoder


class MarathonObject(object):
    """Base Marathon object."""

    def json_repr(self):
        """Construct a JSON-friendly representation of the object.

        :rtype: dict
        """
        return {to_camel_case(k):v for k,v in vars(self).iteritems()}

    @classmethod
    def from_json(cls, attributes):
        """Construct an object from a parsed response.

        :param dict attributes: object attributes from parsed response
        """
        return cls(**{to_snake_case(k): v for k,v in attributes.iteritems()})


class MarathonResource(MarathonObject):
    """Base Marathon resource."""

    def __repr__(self):
        if 'id' in vars(self).keys():
            return "{clazz}::{id}".format(clazz=self.__class__.__name__, id=self.id)
        else:
            return "{clazz}::{obj}".format(clazz=self.__class__.__name__, obj=self.to_json())

    def to_json(self):
        """Encode an object as a JSON string.

        :rtype: str
        """
        return json.dumps(self.json_repr(), cls=MarathonJsonEncoder, sort_keys=True)
