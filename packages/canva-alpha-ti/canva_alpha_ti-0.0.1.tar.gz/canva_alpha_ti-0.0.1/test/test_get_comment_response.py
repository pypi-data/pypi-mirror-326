# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.get_comment_response import GetCommentResponse

class TestGetCommentResponse(unittest.TestCase):
    """GetCommentResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetCommentResponse:
        """Test GetCommentResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetCommentResponse`
        """
        model = GetCommentResponse()
        if include_optional:
            return GetCommentResponse(
                comment = canva_alpha_ti.models.comment.Comment()
            )
        else:
            return GetCommentResponse(
                comment = canva_alpha_ti.models.comment.Comment(),
        )
        """

    def testGetCommentResponse(self):
        """Test GetCommentResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
