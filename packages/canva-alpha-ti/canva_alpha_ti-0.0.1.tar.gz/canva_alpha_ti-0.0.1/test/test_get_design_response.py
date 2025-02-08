# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.get_design_response import GetDesignResponse

class TestGetDesignResponse(unittest.TestCase):
    """GetDesignResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetDesignResponse:
        """Test GetDesignResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetDesignResponse`
        """
        model = GetDesignResponse()
        if include_optional:
            return GetDesignResponse(
                design = canva_alpha_ti.models.design.Design(
                    id = 'DAFVztcvd9z', 
                    title = 'My summer holiday', 
                    owner = canva_alpha_ti.models.team_user_summary.TeamUserSummary(
                        user_id = 'auDAbliZ2rQNNOsUl5OLu', 
                        team_id = 'Oi2RJILTrKk0KRhRUZozX', ), 
                    thumbnail = canva_alpha_ti.models.thumbnail.Thumbnail(
                        width = 595, 
                        height = 335, 
                        url = 'https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>', ), 
                    urls = canva_alpha_ti.models.design_links.DesignLinks(
                        edit_url = 'https://www.canva.com/api/design/{token}/edit', 
                        view_url = 'https://www.canva.com/api/design/{token}/view', ), 
                    created_at = 1377396000, 
                    updated_at = 1692928800, 
                    page_count = 5, )
            )
        else:
            return GetDesignResponse(
                design = canva_alpha_ti.models.design.Design(
                    id = 'DAFVztcvd9z', 
                    title = 'My summer holiday', 
                    owner = canva_alpha_ti.models.team_user_summary.TeamUserSummary(
                        user_id = 'auDAbliZ2rQNNOsUl5OLu', 
                        team_id = 'Oi2RJILTrKk0KRhRUZozX', ), 
                    thumbnail = canva_alpha_ti.models.thumbnail.Thumbnail(
                        width = 595, 
                        height = 335, 
                        url = 'https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>', ), 
                    urls = canva_alpha_ti.models.design_links.DesignLinks(
                        edit_url = 'https://www.canva.com/api/design/{token}/edit', 
                        view_url = 'https://www.canva.com/api/design/{token}/view', ), 
                    created_at = 1377396000, 
                    updated_at = 1692928800, 
                    page_count = 5, ),
        )
        """

    def testGetDesignResponse(self):
        """Test GetDesignResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
