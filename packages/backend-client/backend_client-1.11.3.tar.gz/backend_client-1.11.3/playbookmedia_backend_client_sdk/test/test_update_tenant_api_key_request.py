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

from playbookmedia_backend_client_sdk.models.update_tenant_api_key_request import UpdateTenantAPIKeyRequest

class TestUpdateTenantAPIKeyRequest(unittest.TestCase):
    """UpdateTenantAPIKeyRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateTenantAPIKeyRequest:
        """Test UpdateTenantAPIKeyRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateTenantAPIKeyRequest`
        """
        model = UpdateTenantAPIKeyRequest()
        if include_optional:
            return UpdateTenantAPIKeyRequest(
                api_key = playbookmedia_backend_client_sdk.models.tenant_api_key.TenantAPIKey(
                    id = '', 
                    key_hash = '', 
                    key_prefix = '', 
                    name = '', 
                    description = '', 
                    status = 'STATUS_UNSPECIFIED', 
                    scopes = [
                        'TENANT_API_KEY_SCOPE_UNSPECIFIED'
                        ], 
                    max_uses = 56, 
                    allowed_ips = [
                        ''
                        ], 
                    use_count = 56, 
                    expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return UpdateTenantAPIKeyRequest(
        )
        """

    def testUpdateTenantAPIKeyRequest(self):
        """Test UpdateTenantAPIKeyRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
