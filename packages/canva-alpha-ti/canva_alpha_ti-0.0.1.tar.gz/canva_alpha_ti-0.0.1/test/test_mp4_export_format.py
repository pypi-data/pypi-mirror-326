# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.mp4_export_format import Mp4ExportFormat

class TestMp4ExportFormat(unittest.TestCase):
    """Mp4ExportFormat unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Mp4ExportFormat:
        """Test Mp4ExportFormat
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Mp4ExportFormat`
        """
        model = Mp4ExportFormat()
        if include_optional:
            return Mp4ExportFormat(
                type = 'mp4',
                export_quality = 'regular',
                quality = 'horizontal_480p',
                pages = [2,3,4]
            )
        else:
            return Mp4ExportFormat(
                type = 'mp4',
                quality = 'horizontal_480p',
        )
        """

    def testMp4ExportFormat(self):
        """Test Mp4ExportFormat"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
