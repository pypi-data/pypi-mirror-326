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

from backend_client.models.conflict_info import ConflictInfo

class TestConflictInfo(unittest.TestCase):
    """ConflictInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ConflictInfo:
        """Test ConflictInfo
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ConflictInfo`
        """
        model = ConflictInfo()
        if include_optional:
            return ConflictInfo(
                resource_type = '',
                identifier = '',
                conflict_reason = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_by = ''
            )
        else:
            return ConflictInfo(
        )
        """

    def testConflictInfo(self):
        """Test ConflictInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
