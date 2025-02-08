# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.update_folder_response import UpdateFolderResponse

class TestUpdateFolderResponse(unittest.TestCase):
    """UpdateFolderResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateFolderResponse:
        """Test UpdateFolderResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateFolderResponse`
        """
        model = UpdateFolderResponse()
        if include_optional:
            return UpdateFolderResponse(
                folder = canva_alpha_ti.models.folder.Folder(
                    id = 'FAF2lZtloor', 
                    name = 'My awesome holiday', 
                    created_at = 1377396000, 
                    updated_at = 1692928800, 
                    thumbnail = canva_alpha_ti.models.thumbnail.Thumbnail(
                        width = 595, 
                        height = 335, 
                        url = 'https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>', ), )
            )
        else:
            return UpdateFolderResponse(
        )
        """

    def testUpdateFolderResponse(self):
        """Test UpdateFolderResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
