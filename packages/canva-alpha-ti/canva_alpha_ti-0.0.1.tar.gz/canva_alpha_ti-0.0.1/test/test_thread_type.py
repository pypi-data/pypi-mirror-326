# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.thread_type import ThreadType

class TestThreadType(unittest.TestCase):
    """ThreadType unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ThreadType:
        """Test ThreadType
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ThreadType`
        """
        model = ThreadType()
        if include_optional:
            return ThreadType(
                type = 'comment',
                message = 'Great work [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!',
                mentions = {oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP={user_id=oUnPjZ2k2yuhftbWF7873o, team_id=oBpVhLW22VrqtwKgaayRbP, display_name=John Doe}},
                assignee = canva_alpha_ti.models.user.User(
                    id = 'uKakKUfI03Fg8k2gZ6OkT', 
                    display_name = 'John Doe', ),
                resolver = canva_alpha_ti.models.user.User(
                    id = 'uKakKUfI03Fg8k2gZ6OkT', 
                    display_name = 'John Doe', ),
                content = canva_alpha_ti.models.suggestion_content.SuggestionContent(),
                status = 'open'
            )
        else:
            return ThreadType(
                type = 'comment',
                message = 'Great work [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!',
                mentions = {oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP={user_id=oUnPjZ2k2yuhftbWF7873o, team_id=oBpVhLW22VrqtwKgaayRbP, display_name=John Doe}},
                content = canva_alpha_ti.models.suggestion_content.SuggestionContent(),
                status = 'open',
        )
        """

    def testThreadType(self):
        """Test ThreadType"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
