# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.json_web_key import JsonWebKey

class TestJsonWebKey(unittest.TestCase):
    """JsonWebKey unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> JsonWebKey:
        """Test JsonWebKey
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `JsonWebKey`
        """
        model = JsonWebKey()
        if include_optional:
            return JsonWebKey(
                alg = '',
                kid = '',
                kty = '',
                n = '',
                e = '',
                use = ''
            )
        else:
            return JsonWebKey(
                kid = '',
                kty = '',
                n = '',
                e = '',
        )
        """

    def testJsonWebKey(self):
        """Test JsonWebKey"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
