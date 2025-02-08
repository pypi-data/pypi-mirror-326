# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.group import Group

class TestGroup(unittest.TestCase):
    """Group unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Group:
        """Test Group
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Group`
        """
        model = Group()
        if include_optional:
            return Group(
                id = 'dl9n9SoWoExMsw6Ri1iTg',
                display_name = 'Sales team',
                external = True
            )
        else:
            return Group(
                id = 'dl9n9SoWoExMsw6Ri1iTg',
                external = True,
        )
        """

    def testGroup(self):
        """Test Group"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
