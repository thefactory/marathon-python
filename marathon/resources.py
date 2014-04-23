class MarathonResource(object):
    """Base Marathon resource"""

    def __init__(self, attributes):
        for attr in attributes.keys():
            setattr(self, attr, attributes[attr])

    def __repr__(self):
        return "{clazz}:{id}".format(clazz=self.__class__.__name__, id=self.id)


class MarathonApp(MarathonResource):
    """Marathon Application resource"""


class MarathonTask(MarathonResource):
    """Marathon Task resource"""
