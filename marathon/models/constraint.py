from ..exceptions import InvalidOperatorError


UNIQUE_OPERATOR = 'UNIQUE'
CLUSTER_OPERATOR = 'CLUSTER'
GROUP_BY_OPERATOR = 'GROUP_BY'


class MarathonConstraint(object):
    """Marathon placement constraint.

    See http://mesosphere.io/2013/11/22/marathon-a-mesos-framework-adds-placement-constraints/

    :param str field: constraint operator target
    :param str operator: must be one of [UNIQUE, CLUSTER, GROUP_BY]
    :param value: [optional] if `operator` is CLUSTER, constrain tasks to servers where `field` == `value`.
    If `operator` is GROUP_BY, place at most `value` tasks per group
    :type value: str, int, or None
    """

    def __init__(self, field, operator, value=None):
        if not operator in [UNIQUE_OPERATOR, CLUSTER_OPERATOR, GROUP_BY_OPERATOR]:
            raise InvalidOperatorError(operator)

        self.field = field
        self.operator = operator
        self.value = value

    def __repr__(self):
        if self.value:
            template = "MarathonConstraint::{field}:{operator}:{value}"
        else:
            template = "MarathonConstraint::{field}:{operator}"
        return template.format(**self.__dict__)

    @classmethod
    def json_decode(cls, obj):
        """Construct a MarathonConstraint from a parsed response.

        :param dict attributes: object attributes from parsed response

        :rtype: :class:`MarathonConstraint`
        """
        if len(obj) == 2:
            (field, operator) = obj
            return cls(field, operator)
        if len(obj) > 2:
            (field, operator, value) = obj
            return cls(field, operator, value)

    def json_encode(self):
        """Construct a JSON-friendly representation of the object.

        :rtype: dict
        """
        if self.value:
            return [self.field, self.operator, self.value]
        else:
            return [self.field, self.operator]
