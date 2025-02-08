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

from playbookmedia_backend_client_sdk.models.internal_error_message_response import InternalErrorMessageResponse

class TestInternalErrorMessageResponse(unittest.TestCase):
    """InternalErrorMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> InternalErrorMessageResponse:
        """Test InternalErrorMessageResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `InternalErrorMessageResponse`
        """
        model = InternalErrorMessageResponse()
        if include_optional:
            return InternalErrorMessageResponse(
                code = 'NO_INTERNAL_ERROR',
                message = '',
                incident_id = '',
                service_status = playbookmedia_backend_client_sdk.models.service_status.ServiceStatus(
                    name = '', 
                    status = '', 
                    metrics = {
                        'key' : ''
                        }, 
                    dependencies = [
                        playbookmedia_backend_client_sdk.models.dependency.Dependency(
                            name = '', 
                            status = '', 
                            error = '', 
                            latency = 56, )
                        ], ),
                resource_utilization = playbookmedia_backend_client_sdk.models.resource_utilization.ResourceUtilization(
                    cpu_usage = 1.337, 
                    memory_usage = 1.337, 
                    active_connections = 56, 
                    quotas = {
                        'key' : 1.337
                        }, ),
                operation_details = playbookmedia_backend_client_sdk.models.operation_details.OperationDetails(
                    operation_id = '', 
                    start_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    end_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    stack_trace = [
                        ''
                        ], 
                    parameters = {
                        'key' : ''
                        }, ),
                error_response = playbookmedia_backend_client_sdk.models.base_error_message_response,_extending_google/rpc/status.Base error message response, extending google.rpc.Status(
                    status = playbookmedia_backend_client_sdk.models.status.Status(
                        code = 56, 
                        message = '', 
                        details = [
                            {
                                'key' : null
                                }
                            ], ), )
            )
        else:
            return InternalErrorMessageResponse(
        )
        """

    def testInternalErrorMessageResponse(self):
        """Test InternalErrorMessageResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
