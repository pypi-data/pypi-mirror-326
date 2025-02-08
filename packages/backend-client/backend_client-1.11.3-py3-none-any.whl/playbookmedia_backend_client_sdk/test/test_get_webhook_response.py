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

from playbookmedia_backend_client_sdk.models.get_webhook_response import GetWebhookResponse

class TestGetWebhookResponse(unittest.TestCase):
    """GetWebhookResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetWebhookResponse:
        """Test GetWebhookResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetWebhookResponse`
        """
        model = GetWebhookResponse()
        if include_optional:
            return GetWebhookResponse(
                webhook = playbookmedia_backend_client_sdk.models.webhook_config_represents_a_webhook_integration_configuration
it_defines_how_and_when_notifications_should_be_sent_to_external_systems.WebhookConfig represents a webhook integration configuration
It defines how and when notifications should be sent to external systems(
                    id = '', 
                    url = '', 
                    auth_type = '', 
                    auth_token = '', 
                    custom_headers = {
                        'key' : ''
                        }, 
                    max_retries = 56, 
                    retry_interval = '', 
                    trigger_events = [
                        'TRIGGER_EVENT_UNSPECIFIED'
                        ], 
                    included_fields = [
                        'INCLUDED_FIELD_UNSPECIFIED'
                        ], 
                    include_full_results = True, 
                    payload_format = 'PAYLOAD_FORMAT_UNSPECIFIED', 
                    verify_ssl = True, 
                    signing_secret = '', 
                    rate_limit = 56, 
                    rate_limit_interval = '', 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    last_triggered_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    successful_calls = 56, 
                    failed_calls = 56, 
                    metadata = playbookmedia_backend_client_sdk.models.flexible_metadata_storage_using_google_struct.Flexible metadata storage using Google struct(), 
                    webhook_name = '', )
            )
        else:
            return GetWebhookResponse(
        )
        """

    def testGetWebhookResponse(self):
        """Test GetWebhookResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
