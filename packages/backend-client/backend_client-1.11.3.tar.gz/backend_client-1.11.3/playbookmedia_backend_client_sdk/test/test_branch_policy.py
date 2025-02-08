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

from playbookmedia_backend_client_sdk.models.branch_policy import BranchPolicy

class TestBranchPolicy(unittest.TestCase):
    """BranchPolicy unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BranchPolicy:
        """Test BranchPolicy
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BranchPolicy`
        """
        model = BranchPolicy()
        if include_optional:
            return BranchPolicy(
                id = '',
                branch_id = '',
                required_approvers = [
                    ''
                    ],
                minimum_approvals = 56,
                enforce_linear_history = True,
                allow_force_push = True,
                protected_paths = [
                    ''
                    ],
                merge_rules = {
                    'key' : ''
                    },
                automated_checks = [
                    ''
                    ],
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return BranchPolicy(
        )
        """

    def testBranchPolicy(self):
        """Test BranchPolicy"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
