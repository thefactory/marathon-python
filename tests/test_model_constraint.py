from marathon.models.app import MarathonConstraint
import unittest


class MarathonConstraintTests(unittest.TestCase):
    def test_repr_with_value(self):
        constraint = MarathonConstraint('a_field', 'OPERATOR', 'a_value')
        representation = repr(constraint)
        self.assertEqual(representation,
                         "MarathonConstraint::a_field:OPERATOR:a_value")

    def test_repr_without_value(self):
        constraint = MarathonConstraint('a_field', 'OPERATOR')
        representation = repr(constraint)
        self.assertEqual(representation,
                         "MarathonConstraint::a_field:OPERATOR")

    def test_json_repr_with_value(self):
        constraint = MarathonConstraint('a_field', 'OPERATOR', 'a_value')
        json_repr = constraint.json_repr()
        self.assertEqual(json_repr, ['a_field', 'OPERATOR', 'a_value'])

    def test_json_repr_without_value(self):
        constraint = MarathonConstraint('a_field', 'OPERATOR')
        json_repr = constraint.json_repr()
        self.assertEqual(json_repr, ['a_field', 'OPERATOR'])

    def test_from_json_with_value(self):
        constraint = MarathonConstraint.from_json(['a_field', 'OPERATOR', 'a_value'])
        self.assertEqual(constraint,
                         MarathonConstraint('a_field', 'OPERATOR', 'a_value'))

    def test_from_json_without_value(self):
        constraint = MarathonConstraint.from_json(['a_field', 'OPERATOR'])
        self.assertEqual(constraint, MarathonConstraint('a_field', 'OPERATOR'))

    def test_from_string_with_value(self):
        constraint = MarathonConstraint.from_string('a_field:OPERATOR:a_value')
        self.assertEqual(constraint,
                         MarathonConstraint('a_field', 'OPERATOR', 'a_value'))

    def test_from_string_without_value(self):
        constraint = MarathonConstraint.from_string('a_field:OPERATOR')
        self.assertEqual(constraint, MarathonConstraint('a_field', 'OPERATOR'))

    def test_from_string_raises_an_error_for_invalid_format(self):
        with self.assertRaises(ValueError):
            MarathonConstraint.from_string('a_field:OPERATOR:a_value:')

        with self.assertRaises(ValueError):
            MarathonConstraint.from_string('a_field')

        with self.assertRaises(ValueError):
            MarathonConstraint.from_string('a_field:OPERATOR:a_value:something')
