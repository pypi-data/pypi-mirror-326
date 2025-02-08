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

from playbookmedia_backend_client_sdk.models.update_account_settings_response import UpdateAccountSettingsResponse

class TestUpdateAccountSettingsResponse(unittest.TestCase):
    """UpdateAccountSettingsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateAccountSettingsResponse:
        """Test UpdateAccountSettingsResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateAccountSettingsResponse`
        """
        model = UpdateAccountSettingsResponse()
        if include_optional:
            return UpdateAccountSettingsResponse(
                settings = playbookmedia_backend_client_sdk.models.account_wide_settings.Account-wide settings(
                    id = '', 
                    email_notifications = True, 
                    slack_notifications = True, 
                    default_data_retention = '', 
                    auto_purge_enabled = True, 
                    require2fa = True, 
                    session_timeout = '', )
            )
        else:
            return UpdateAccountSettingsResponse(
        )
        """

    def testUpdateAccountSettingsResponse(self):
        """Test UpdateAccountSettingsResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
