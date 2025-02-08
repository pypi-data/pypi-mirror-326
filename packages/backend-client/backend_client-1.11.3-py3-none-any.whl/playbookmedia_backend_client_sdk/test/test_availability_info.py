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

from playbookmedia_backend_client_sdk.models.availability_info import AvailabilityInfo

class TestAvailabilityInfo(unittest.TestCase):
    """AvailabilityInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AvailabilityInfo:
        """Test AvailabilityInfo
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AvailabilityInfo`
        """
        model = AvailabilityInfo()
        if include_optional:
            return AvailabilityInfo(
                retry_after = 56,
                maintenance_window = '',
                affected_services = [
                    ''
                    ],
                status_page_url = ''
            )
        else:
            return AvailabilityInfo(
        )
        """

    def testAvailabilityInfo(self):
        """Test AvailabilityInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
