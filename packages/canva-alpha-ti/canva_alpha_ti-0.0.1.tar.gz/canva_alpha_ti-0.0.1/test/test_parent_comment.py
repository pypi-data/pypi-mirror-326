# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.parent_comment import ParentComment

class TestParentComment(unittest.TestCase):
    """ParentComment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ParentComment:
        """Test ParentComment
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ParentComment`
        """
        model = ParentComment()
        if include_optional:
            return ParentComment(
                type = 'parent',
                id = 'KeAbiEAjZEj',
                attached_to = {"design_id":"DAFVztcvd9z","type":"design"},
                message = 'Great work [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!',
                author = canva_alpha_ti.models.user.User(
                    id = 'uKakKUfI03Fg8k2gZ6OkT', 
                    display_name = 'John Doe', ),
                created_at = 1692928800,
                updated_at = 1692928900,
                mentions = {"oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP":{"user_id":"oUnPjZ2k2yuhftbWF7873o","team_id":"oBpVhLW22VrqtwKgaayRbP","display_name":"John Doe"}},
                assignee = canva_alpha_ti.models.user.User(
                    id = 'uKakKUfI03Fg8k2gZ6OkT', 
                    display_name = 'John Doe', ),
                resolver = canva_alpha_ti.models.user.User(
                    id = 'uKakKUfI03Fg8k2gZ6OkT', 
                    display_name = 'John Doe', )
            )
        else:
            return ParentComment(
                type = 'parent',
                id = 'KeAbiEAjZEj',
                message = 'Great work [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!',
                author = canva_alpha_ti.models.user.User(
                    id = 'uKakKUfI03Fg8k2gZ6OkT', 
                    display_name = 'John Doe', ),
                mentions = {"oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP":{"user_id":"oUnPjZ2k2yuhftbWF7873o","team_id":"oBpVhLW22VrqtwKgaayRbP","display_name":"John Doe"}},
        )
        """

    def testParentComment(self):
        """Test ParentComment"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
