# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.api.oauth_api import OauthApi


class TestOauthApi(unittest.TestCase):
    """OauthApi unit test stubs"""

    def setUp(self) -> None:
        self.api = OauthApi()

    def tearDown(self) -> None:
        pass

    def test_exchange_access_token(self) -> None:
        """Test case for exchange_access_token

        """
        pass

    def test_introspect_token(self) -> None:
        """Test case for introspect_token

        """
        pass

    def test_revoke_tokens(self) -> None:
        """Test case for revoke_tokens

        """
        pass


if __name__ == '__main__':
    unittest.main()
