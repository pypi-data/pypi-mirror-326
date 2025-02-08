# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.create_asset_upload_job_response import CreateAssetUploadJobResponse

class TestCreateAssetUploadJobResponse(unittest.TestCase):
    """CreateAssetUploadJobResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateAssetUploadJobResponse:
        """Test CreateAssetUploadJobResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateAssetUploadJobResponse`
        """
        model = CreateAssetUploadJobResponse()
        if include_optional:
            return CreateAssetUploadJobResponse(
                job = {"id":"e08861ae-3b29-45db-8dc1-1fe0bf7f1cc8","status":"success","asset":{"id":"Msd59349ff","name":"My Awesome Upload","tags":["image","holiday","best day ever"],"created_at":1377396000,"updated_at":1692928800,"thumbnail":{"width":595,"height":335,"url":"https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>"}}}
            )
        else:
            return CreateAssetUploadJobResponse(
                job = {"id":"e08861ae-3b29-45db-8dc1-1fe0bf7f1cc8","status":"success","asset":{"id":"Msd59349ff","name":"My Awesome Upload","tags":["image","holiday","best day ever"],"created_at":1377396000,"updated_at":1692928800,"thumbnail":{"width":595,"height":335,"url":"https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>"}}},
        )
        """

    def testCreateAssetUploadJobResponse(self):
        """Test CreateAssetUploadJobResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
