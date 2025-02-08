# coding: utf-8

"""
    Lead Scraping Service API

    Vector Lead Scraping Service API - Manages Lead Scraping Jobs

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@vector.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from playbookmedia_backend_client_sdk.models.resource_info import ResourceInfo

class TestResourceInfo(unittest.TestCase):
    """ResourceInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ResourceInfo:
        """Test ResourceInfo
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ResourceInfo`
        """
        model = ResourceInfo()
        if include_optional:
            return ResourceInfo(
                type = '',
                id = '',
                path = '',
                tenant_id = '',
                scopes = [
                    ''
                    ]
            )
        else:
            return ResourceInfo(
        )
        """

    def testResourceInfo(self):
        """Test ResourceInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
