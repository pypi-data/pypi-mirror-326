# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.design_autofill_job_result import DesignAutofillJobResult

class TestDesignAutofillJobResult(unittest.TestCase):
    """DesignAutofillJobResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DesignAutofillJobResult:
        """Test DesignAutofillJobResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DesignAutofillJobResult`
        """
        model = DesignAutofillJobResult()
        if include_optional:
            return DesignAutofillJobResult(
                type = 'create_design',
                design = canva_alpha_ti.models.design_summary.DesignSummary(
                    id = 'DAFVztcvd9z', 
                    title = 'My summer holiday', 
                    url = 'https://www.canva.com/design/DAFVztcvd9z/edit', 
                    thumbnail = canva_alpha_ti.models.thumbnail.Thumbnail(
                        width = 595, 
                        height = 335, 
                        url = 'https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>', ), 
                    urls = canva_alpha_ti.models.design_links.DesignLinks(
                        edit_url = 'https://www.canva.com/api/design/{token}/edit', 
                        view_url = 'https://www.canva.com/api/design/{token}/view', ), 
                    created_at = 1377396000, 
                    updated_at = 1692928800, 
                    page_count = 3, )
            )
        else:
            return DesignAutofillJobResult(
                type = 'create_design',
                design = canva_alpha_ti.models.design_summary.DesignSummary(
                    id = 'DAFVztcvd9z', 
                    title = 'My summer holiday', 
                    url = 'https://www.canva.com/design/DAFVztcvd9z/edit', 
                    thumbnail = canva_alpha_ti.models.thumbnail.Thumbnail(
                        width = 595, 
                        height = 335, 
                        url = 'https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>', ), 
                    urls = canva_alpha_ti.models.design_links.DesignLinks(
                        edit_url = 'https://www.canva.com/api/design/{token}/edit', 
                        view_url = 'https://www.canva.com/api/design/{token}/view', ), 
                    created_at = 1377396000, 
                    updated_at = 1692928800, 
                    page_count = 3, ),
        )
        """

    def testDesignAutofillJobResult(self):
        """Test DesignAutofillJobResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
