# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from canva_alpha_ti.models.create_design_autofill_job_request import CreateDesignAutofillJobRequest

class TestCreateDesignAutofillJobRequest(unittest.TestCase):
    """CreateDesignAutofillJobRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateDesignAutofillJobRequest:
        """Test CreateDesignAutofillJobRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateDesignAutofillJobRequest`
        """
        model = CreateDesignAutofillJobRequest()
        if include_optional:
            return CreateDesignAutofillJobRequest(
                brand_template_id = 'DAFVztcvd9z',
                title = '0',
                data = {"cute_pet_image_of_the_day":{"type":"image","asset_id":"Msd59349ff"},"cute_pet_witty_pet_says":{"type":"text","text":"It was like this when I got here!"},"cute_pet_sales_chart":{"type":"chart","chart_data":{"rows":[{"cells":[{"type":"string","value":"Geographic Region"},{"type":"string","value":"Sales (millions AUD)"},{"type":"string","value":"Target met?"},{"type":"string","value":"Date met"}]},{"cells":[{"type":"string","value":"Asia Pacific"},{"type":"number","value":10.2},{"type":"boolean","value":true},{"type":"date","value":1721944387}]},{"cells":[{"type":"string","value":"EMEA"},{"type":"number","value":13.8},{"type":"boolean","value":false},{"type":"date"}]}]}}}
            )
        else:
            return CreateDesignAutofillJobRequest(
                brand_template_id = 'DAFVztcvd9z',
                data = {"cute_pet_image_of_the_day":{"type":"image","asset_id":"Msd59349ff"},"cute_pet_witty_pet_says":{"type":"text","text":"It was like this when I got here!"},"cute_pet_sales_chart":{"type":"chart","chart_data":{"rows":[{"cells":[{"type":"string","value":"Geographic Region"},{"type":"string","value":"Sales (millions AUD)"},{"type":"string","value":"Target met?"},{"type":"string","value":"Date met"}]},{"cells":[{"type":"string","value":"Asia Pacific"},{"type":"number","value":10.2},{"type":"boolean","value":true},{"type":"date","value":1721944387}]},{"cells":[{"type":"string","value":"EMEA"},{"type":"number","value":13.8},{"type":"boolean","value":false},{"type":"date"}]}]}}},
        )
        """

    def testCreateDesignAutofillJobRequest(self):
        """Test CreateDesignAutofillJobRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
