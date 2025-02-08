# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.design_import_metadata import DesignImportMetadata

class TestDesignImportMetadata(unittest.TestCase):
    """DesignImportMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DesignImportMetadata:
        """Test DesignImportMetadata
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DesignImportMetadata`
        """
        model = DesignImportMetadata()
        if include_optional:
            return DesignImportMetadata(
                title_base64 = 'TXkgQXdlc29tZSBEZXNpZ24g8J+YjQ==',
                mime_type = 'application/pdf'
            )
        else:
            return DesignImportMetadata(
                title_base64 = 'TXkgQXdlc29tZSBEZXNpZ24g8J+YjQ==',
        )
        """

    def testDesignImportMetadata(self):
        """Test DesignImportMetadata"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
