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

from playbookmedia_backend_client_sdk.models.compliance_check import ComplianceCheck

class TestComplianceCheck(unittest.TestCase):
    """ComplianceCheck unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ComplianceCheck:
        """Test ComplianceCheck
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ComplianceCheck`
        """
        model = ComplianceCheck()
        if include_optional:
            return ComplianceCheck(
                id = '',
                intelligence_id = '',
                compliance_standard = '',
                check_result = '',
                violations = [
                    ''
                    ],
                remediation_steps = '',
                check_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return ComplianceCheck(
        )
        """

    def testComplianceCheck(self):
        """Test ComplianceCheck"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
