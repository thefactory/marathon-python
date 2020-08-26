from marathon.models.group import MarathonGroup
import unittest


class MarathonGroupTest(unittest.TestCase):

    def test_from_json_parses_root_group(self):
        data = {
                   "id": "/",
                   "groups": [
                       {"id": "/foo", "apps": []},
                       {"id": "/bla", "apps": []},
                   ],
                   "apps": []
        }
        group = MarathonGroup().from_json(data)
        self.assertEqual("/", group.id)

    def test_from_json_parses_group_with_enforce_role(self):
        data = {
                   "id": "/mygroup/works",
                   "groups": [
                       {"id": "/foo", "apps": []},
                   ],
                   "apps": [],
                   "enforceRole": False,

        }
        group = MarathonGroup().from_json(data)
        self.assertEqual("/mygroup/works", group.id)
