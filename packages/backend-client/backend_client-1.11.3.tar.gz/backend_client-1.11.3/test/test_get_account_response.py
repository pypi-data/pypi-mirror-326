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

from backend_client.models.get_account_response import GetAccountResponse

class TestGetAccountResponse(unittest.TestCase):
    """GetAccountResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetAccountResponse:
        """Test GetAccountResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetAccountResponse`
        """
        model = GetAccountResponse()
        if include_optional:
            return GetAccountResponse(
                account = backend_client.models.account.Account(
                    id = '', 
                    auth_platform_user_id = '', 
                    org_id = '', 
                    tenant_id = '', 
                    email = '', 
                    last_modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    scraping_jobs = [
                        backend_client.models.scraping_job.ScrapingJob(
                            id = '', 
                            name = '', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            status = 'BACKGROUND_JOB_STATUS_UNSPECIFIED', 
                            keywords = [
                                ''
                                ], 
                            lang = '', 
                            zoom = 56, 
                            lat = '', 
                            lon = '', 
                            fast_mode = True, 
                            radius = 56, 
                            depth = 56, 
                            email = True, 
                            max_time = 56, 
                            proxies = [
                                ''
                                ], 
                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            payload_type = '', 
                            priority = 56, 
                            payload = 'YQ==', )
                        ], )
            )
        else:
            return GetAccountResponse(
        )
        """

    def testGetAccountResponse(self):
        """Test GetAccountResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
