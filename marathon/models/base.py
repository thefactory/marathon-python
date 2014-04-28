class MarathonResource(object):
    """Base Marathon resource."""

    def __repr__(self):
        return "{clazz}::{id}".format(clazz=self.__class__.__name__, id=self.id)

    @classmethod
    def json_decode(cls, attributes):
        """Construct an object from a parsed response.

        :param dict attributes: object attributes from parsed response
        """
        obj = cls()
        for attr in attributes.keys():
            setattr(obj, attr, attributes[attr])
        return obj

    def json_encode(self):
        """Construct a JSON-friendly representation of the object.

        :rtype: dict
        """
        return self.__dict__