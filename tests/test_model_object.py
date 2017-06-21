# encoding: utf-8

from marathon.models.base import MarathonObject
import unittest


class MarathonObjectTest(unittest.TestCase):

    def test_hashable(self):
        """
        Regression test for issue #203

        MarathonObject defined __eq__ but not __hash__, meaning that in
        in Python2.7 MarathonObjects are hashable, but in Python3 they're not,

        This test ensures that we are hashable in all versions of python
        """
        obj = MarathonObject()
        collection = {}
        collection[obj] = True
        assert collection[obj]
