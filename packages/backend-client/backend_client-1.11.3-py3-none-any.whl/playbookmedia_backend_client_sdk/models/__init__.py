# coding: utf-8

# flake8: noqa
"""
    Lead Scraping Service API

    Vector Lead Scraping Service API - Manages Lead Scraping Jobs

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@vector.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


# import models into model package
from playbookmedia_backend_client_sdk.models.ai_assistance_log import AIAssistanceLog
from playbookmedia_backend_client_sdk.models.api_info import APIInfo
from playbookmedia_backend_client_sdk.models.api_key import APIKey
from playbookmedia_backend_client_sdk.models.account import Account
from playbookmedia_backend_client_sdk.models.account1 import Account1
from playbookmedia_backend_client_sdk.models.account_settings import AccountSettings
from playbookmedia_backend_client_sdk.models.account_status import AccountStatus
from playbookmedia_backend_client_sdk.models.activity_metrics import ActivityMetrics
from playbookmedia_backend_client_sdk.models.any import Any
from playbookmedia_backend_client_sdk.models.app_analytics import AppAnalytics
from playbookmedia_backend_client_sdk.models.app_category import AppCategory
from playbookmedia_backend_client_sdk.models.app_development_info import AppDevelopmentInfo
from playbookmedia_backend_client_sdk.models.app_installation import AppInstallation
from playbookmedia_backend_client_sdk.models.app_permission import AppPermission
from playbookmedia_backend_client_sdk.models.app_review import AppReview
from playbookmedia_backend_client_sdk.models.app_version import AppVersion
from playbookmedia_backend_client_sdk.models.app_webhook import AppWebhook
from playbookmedia_backend_client_sdk.models.auth_context import AuthContext
from playbookmedia_backend_client_sdk.models.auth_error_code import AuthErrorCode
from playbookmedia_backend_client_sdk.models.authentication_error_message_response import AuthenticationErrorMessageResponse
from playbookmedia_backend_client_sdk.models.authentication_error_message_response1 import AuthenticationErrorMessageResponse1
from playbookmedia_backend_client_sdk.models.availability_info import AvailabilityInfo
from playbookmedia_backend_client_sdk.models.background_job_status import BackgroundJobStatus
from playbookmedia_backend_client_sdk.models.bad_gateway_error_message_response import BadGatewayErrorMessageResponse
from playbookmedia_backend_client_sdk.models.billing_mode import BillingMode
from playbookmedia_backend_client_sdk.models.billing_plan import BillingPlan
from playbookmedia_backend_client_sdk.models.branch_merge import BranchMerge
from playbookmedia_backend_client_sdk.models.branch_policy import BranchPolicy
from playbookmedia_backend_client_sdk.models.business_hours import BusinessHours
from playbookmedia_backend_client_sdk.models.change_set import ChangeSet
from playbookmedia_backend_client_sdk.models.comment_thread import CommentThread
from playbookmedia_backend_client_sdk.models.compliance_check import ComplianceCheck
from playbookmedia_backend_client_sdk.models.compliance_level import ComplianceLevel
from playbookmedia_backend_client_sdk.models.compliance_metrics import ComplianceMetrics
from playbookmedia_backend_client_sdk.models.compliance_score import ComplianceScore
from playbookmedia_backend_client_sdk.models.compliance_violation import ComplianceViolation
from playbookmedia_backend_client_sdk.models.conflict_error_message_response import ConflictErrorMessageResponse
from playbookmedia_backend_client_sdk.models.conflict_info import ConflictInfo
from playbookmedia_backend_client_sdk.models.contextual_summary import ContextualSummary
from playbookmedia_backend_client_sdk.models.contract_intelligence import ContractIntelligence
from playbookmedia_backend_client_sdk.models.create_api_key_request import CreateAPIKeyRequest
from playbookmedia_backend_client_sdk.models.create_api_key_response import CreateAPIKeyResponse
from playbookmedia_backend_client_sdk.models.create_account_request import CreateAccountRequest
from playbookmedia_backend_client_sdk.models.create_account_request1 import CreateAccountRequest1
from playbookmedia_backend_client_sdk.models.create_account_response import CreateAccountResponse
from playbookmedia_backend_client_sdk.models.create_account_response1 import CreateAccountResponse1
from playbookmedia_backend_client_sdk.models.create_organization_request import CreateOrganizationRequest
from playbookmedia_backend_client_sdk.models.create_organization_response import CreateOrganizationResponse
from playbookmedia_backend_client_sdk.models.create_scraping_job_request import CreateScrapingJobRequest
from playbookmedia_backend_client_sdk.models.create_scraping_job_response import CreateScrapingJobResponse
from playbookmedia_backend_client_sdk.models.create_tenant_api_key_request import CreateTenantAPIKeyRequest
from playbookmedia_backend_client_sdk.models.create_tenant_api_key_response import CreateTenantAPIKeyResponse
from playbookmedia_backend_client_sdk.models.create_tenant_body import CreateTenantBody
from playbookmedia_backend_client_sdk.models.create_tenant_response import CreateTenantResponse
from playbookmedia_backend_client_sdk.models.create_webhook_request import CreateWebhookRequest
from playbookmedia_backend_client_sdk.models.create_webhook_response import CreateWebhookResponse
from playbookmedia_backend_client_sdk.models.create_workflow_body import CreateWorkflowBody
from playbookmedia_backend_client_sdk.models.create_workflow_response import CreateWorkflowResponse
from playbookmedia_backend_client_sdk.models.create_workspace_request import CreateWorkspaceRequest
from playbookmedia_backend_client_sdk.models.create_workspace_request1 import CreateWorkspaceRequest1
from playbookmedia_backend_client_sdk.models.create_workspace_response import CreateWorkspaceResponse
from playbookmedia_backend_client_sdk.models.create_workspace_response1 import CreateWorkspaceResponse1
from playbookmedia_backend_client_sdk.models.data_profile import DataProfile
from playbookmedia_backend_client_sdk.models.day_of_week import DayOfWeek
from playbookmedia_backend_client_sdk.models.delete_api_key_response import DeleteAPIKeyResponse
from playbookmedia_backend_client_sdk.models.delete_account_response import DeleteAccountResponse
from playbookmedia_backend_client_sdk.models.delete_organization_response import DeleteOrganizationResponse
from playbookmedia_backend_client_sdk.models.delete_scraping_job_response import DeleteScrapingJobResponse
from playbookmedia_backend_client_sdk.models.delete_tenant_api_key_response import DeleteTenantAPIKeyResponse
from playbookmedia_backend_client_sdk.models.delete_tenant_response import DeleteTenantResponse
from playbookmedia_backend_client_sdk.models.delete_webhook_response import DeleteWebhookResponse
from playbookmedia_backend_client_sdk.models.delete_workflow_response import DeleteWorkflowResponse
from playbookmedia_backend_client_sdk.models.delete_workspace_response import DeleteWorkspaceResponse
from playbookmedia_backend_client_sdk.models.dependency import Dependency
from playbookmedia_backend_client_sdk.models.document_branch import DocumentBranch
from playbookmedia_backend_client_sdk.models.document_instance import DocumentInstance
from playbookmedia_backend_client_sdk.models.document_snapshot import DocumentSnapshot
from playbookmedia_backend_client_sdk.models.document_status import DocumentStatus
from playbookmedia_backend_client_sdk.models.document_template import DocumentTemplate
from playbookmedia_backend_client_sdk.models.document_version import DocumentVersion
from playbookmedia_backend_client_sdk.models.download_scraping_results_response import DownloadScrapingResultsResponse
from playbookmedia_backend_client_sdk.models.employee_benefit import EmployeeBenefit
from playbookmedia_backend_client_sdk.models.error_response import ErrorResponse
from playbookmedia_backend_client_sdk.models.explanation_block import ExplanationBlock
from playbookmedia_backend_client_sdk.models.field_error import FieldError
from playbookmedia_backend_client_sdk.models.field_violation import FieldViolation
from playbookmedia_backend_client_sdk.models.file_embeddings import FileEmbeddings
from playbookmedia_backend_client_sdk.models.file_metadata import FileMetadata
from playbookmedia_backend_client_sdk.models.file_sharing import FileSharing
from playbookmedia_backend_client_sdk.models.file_version import FileVersion
from playbookmedia_backend_client_sdk.models.folder_metadata import FolderMetadata
from playbookmedia_backend_client_sdk.models.forbidden_error_message_response import ForbiddenErrorMessageResponse
from playbookmedia_backend_client_sdk.models.gateway_timeout_error_message_response import GatewayTimeoutErrorMessageResponse
from playbookmedia_backend_client_sdk.models.get_api_key_response import GetAPIKeyResponse
from playbookmedia_backend_client_sdk.models.get_account_response import GetAccountResponse
from playbookmedia_backend_client_sdk.models.get_account_response1 import GetAccountResponse1
from playbookmedia_backend_client_sdk.models.get_account_usage_response import GetAccountUsageResponse
from playbookmedia_backend_client_sdk.models.get_lead_response import GetLeadResponse
from playbookmedia_backend_client_sdk.models.get_organization_response import GetOrganizationResponse
from playbookmedia_backend_client_sdk.models.get_scraping_job_response import GetScrapingJobResponse
from playbookmedia_backend_client_sdk.models.get_tenant_api_key_response import GetTenantAPIKeyResponse
from playbookmedia_backend_client_sdk.models.get_tenant_response import GetTenantResponse
from playbookmedia_backend_client_sdk.models.get_webhook_response import GetWebhookResponse
from playbookmedia_backend_client_sdk.models.get_workflow_response import GetWorkflowResponse
from playbookmedia_backend_client_sdk.models.get_workspace_analytics_response import GetWorkspaceAnalyticsResponse
from playbookmedia_backend_client_sdk.models.get_workspace_analytics_response1 import GetWorkspaceAnalyticsResponse1
from playbookmedia_backend_client_sdk.models.get_workspace_compliance_report_response import GetWorkspaceComplianceReportResponse
from playbookmedia_backend_client_sdk.models.get_workspace_response import GetWorkspaceResponse
from playbookmedia_backend_client_sdk.models.get_workspace_storage_stats_response import GetWorkspaceStorageStatsResponse
from playbookmedia_backend_client_sdk.models.gone_error_message_response import GoneErrorMessageResponse
from playbookmedia_backend_client_sdk.models.included_field import IncludedField
from playbookmedia_backend_client_sdk.models.internal_error_code import InternalErrorCode
from playbookmedia_backend_client_sdk.models.internal_error_message_response import InternalErrorMessageResponse
from playbookmedia_backend_client_sdk.models.interval import Interval
from playbookmedia_backend_client_sdk.models.job_success_rate import JobSuccessRate
from playbookmedia_backend_client_sdk.models.language import Language
from playbookmedia_backend_client_sdk.models.lead import Lead
from playbookmedia_backend_client_sdk.models.limit_info import LimitInfo
from playbookmedia_backend_client_sdk.models.list_api_keys_response import ListAPIKeysResponse
from playbookmedia_backend_client_sdk.models.list_accounts_response import ListAccountsResponse
from playbookmedia_backend_client_sdk.models.list_accounts_response1 import ListAccountsResponse1
from playbookmedia_backend_client_sdk.models.list_leads_response import ListLeadsResponse
from playbookmedia_backend_client_sdk.models.list_organizations_response import ListOrganizationsResponse
from playbookmedia_backend_client_sdk.models.list_scraping_jobs_response import ListScrapingJobsResponse
from playbookmedia_backend_client_sdk.models.list_tenant_api_keys_response import ListTenantAPIKeysResponse
from playbookmedia_backend_client_sdk.models.list_tenants_response import ListTenantsResponse
from playbookmedia_backend_client_sdk.models.list_webhooks_response import ListWebhooksResponse
from playbookmedia_backend_client_sdk.models.list_workflows_response import ListWorkflowsResponse
from playbookmedia_backend_client_sdk.models.list_workspace_sharings_response import ListWorkspaceSharingsResponse
from playbookmedia_backend_client_sdk.models.list_workspaces_response import ListWorkspacesResponse
from playbookmedia_backend_client_sdk.models.list_workspaces_response1 import ListWorkspacesResponse1
from playbookmedia_backend_client_sdk.models.mfa_info import MFAInfo
from playbookmedia_backend_client_sdk.models.marketplace_app import MarketplaceApp
from playbookmedia_backend_client_sdk.models.merge_request import MergeRequest
from playbookmedia_backend_client_sdk.models.method_not_allowed_error_message_response import MethodNotAllowedErrorMessageResponse
from playbookmedia_backend_client_sdk.models.negotiation_history import NegotiationHistory
from playbookmedia_backend_client_sdk.models.negotiation_round import NegotiationRound
from playbookmedia_backend_client_sdk.models.not_found_error_code import NotFoundErrorCode
from playbookmedia_backend_client_sdk.models.not_found_error_message_response import NotFoundErrorMessageResponse
from playbookmedia_backend_client_sdk.models.not_implemented_error_message_response import NotImplementedErrorMessageResponse
from playbookmedia_backend_client_sdk.models.null_value import NullValue
from playbookmedia_backend_client_sdk.models.operation_details import OperationDetails
from playbookmedia_backend_client_sdk.models.organization import Organization
from playbookmedia_backend_client_sdk.models.output_format import OutputFormat
from playbookmedia_backend_client_sdk.models.pause_workflow_body import PauseWorkflowBody
from playbookmedia_backend_client_sdk.models.pause_workflow_response import PauseWorkflowResponse
from playbookmedia_backend_client_sdk.models.payload_format import PayloadFormat
from playbookmedia_backend_client_sdk.models.payment_info import PaymentInfo
from playbookmedia_backend_client_sdk.models.payment_required_error_message_response import PaymentRequiredErrorMessageResponse
from playbookmedia_backend_client_sdk.models.payment_status import PaymentStatus
from playbookmedia_backend_client_sdk.models.permission import Permission
from playbookmedia_backend_client_sdk.models.plan_tier import PlanTier
from playbookmedia_backend_client_sdk.models.precondition_failed_error_message_response import PreconditionFailedErrorMessageResponse
from playbookmedia_backend_client_sdk.models.pricing_model import PricingModel
from playbookmedia_backend_client_sdk.models.quota_info import QuotaInfo
from playbookmedia_backend_client_sdk.models.rate_limit_context import RateLimitContext
from playbookmedia_backend_client_sdk.models.rate_limit_error_message_response import RateLimitErrorMessageResponse
from playbookmedia_backend_client_sdk.models.remove_workspace_sharing_response import RemoveWorkspaceSharingResponse
from playbookmedia_backend_client_sdk.models.resource_info import ResourceInfo
from playbookmedia_backend_client_sdk.models.resource_utilization import ResourceUtilization
from playbookmedia_backend_client_sdk.models.resource_validation import ResourceValidation
from playbookmedia_backend_client_sdk.models.revenue_range import RevenueRange
from playbookmedia_backend_client_sdk.models.review import Review
from playbookmedia_backend_client_sdk.models.risk_assessment import RiskAssessment
from playbookmedia_backend_client_sdk.models.role import Role
from playbookmedia_backend_client_sdk.models.rotate_api_key_request import RotateAPIKeyRequest
from playbookmedia_backend_client_sdk.models.rotate_api_key_response import RotateAPIKeyResponse
from playbookmedia_backend_client_sdk.models.rotate_tenant_api_key_request import RotateTenantAPIKeyRequest
from playbookmedia_backend_client_sdk.models.rotate_tenant_api_key_response import RotateTenantAPIKeyResponse
from playbookmedia_backend_client_sdk.models.rpc_status import RpcStatus
from playbookmedia_backend_client_sdk.models.schema_validation import SchemaValidation
from playbookmedia_backend_client_sdk.models.scraping_job import ScrapingJob
from playbookmedia_backend_client_sdk.models.scraping_workflow import ScrapingWorkflow
from playbookmedia_backend_client_sdk.models.service_status import ServiceStatus
from playbookmedia_backend_client_sdk.models.service_unavailable_error_message_response import ServiceUnavailableErrorMessageResponse
from playbookmedia_backend_client_sdk.models.session_info import SessionInfo
from playbookmedia_backend_client_sdk.models.share_workspace_body import ShareWorkspaceBody
from playbookmedia_backend_client_sdk.models.share_workspace_response import ShareWorkspaceResponse
from playbookmedia_backend_client_sdk.models.signature_block import SignatureBlock
from playbookmedia_backend_client_sdk.models.signature_request import SignatureRequest
from playbookmedia_backend_client_sdk.models.signature_status import SignatureStatus
from playbookmedia_backend_client_sdk.models.signature_workflow import SignatureWorkflow
from playbookmedia_backend_client_sdk.models.status import Status
from playbookmedia_backend_client_sdk.models.storage_breakdown import StorageBreakdown
from playbookmedia_backend_client_sdk.models.subscription import Subscription
from playbookmedia_backend_client_sdk.models.suggestions import Suggestions
from playbookmedia_backend_client_sdk.models.template_type import TemplateType
from playbookmedia_backend_client_sdk.models.template_variable import TemplateVariable
from playbookmedia_backend_client_sdk.models.template_version import TemplateVersion
from playbookmedia_backend_client_sdk.models.tenant import Tenant
from playbookmedia_backend_client_sdk.models.tenant_api_key import TenantAPIKey
from playbookmedia_backend_client_sdk.models.tenant_api_key_scope import TenantAPIKeyScope
from playbookmedia_backend_client_sdk.models.timezone import Timezone
from playbookmedia_backend_client_sdk.models.token_info import TokenInfo
from playbookmedia_backend_client_sdk.models.too_early_error_message_response import TooEarlyErrorMessageResponse
from playbookmedia_backend_client_sdk.models.trigger_event import TriggerEvent
from playbookmedia_backend_client_sdk.models.trigger_workflow_body import TriggerWorkflowBody
from playbookmedia_backend_client_sdk.models.trigger_workflow_response import TriggerWorkflowResponse
from playbookmedia_backend_client_sdk.models.unprocessable_entity_error_message_response import UnprocessableEntityErrorMessageResponse
from playbookmedia_backend_client_sdk.models.update_api_key_request import UpdateAPIKeyRequest
from playbookmedia_backend_client_sdk.models.update_api_key_response import UpdateAPIKeyResponse
from playbookmedia_backend_client_sdk.models.update_account_request import UpdateAccountRequest
from playbookmedia_backend_client_sdk.models.update_account_request1 import UpdateAccountRequest1
from playbookmedia_backend_client_sdk.models.update_account_request_payload import UpdateAccountRequestPayload
from playbookmedia_backend_client_sdk.models.update_account_response import UpdateAccountResponse
from playbookmedia_backend_client_sdk.models.update_account_settings_request import UpdateAccountSettingsRequest
from playbookmedia_backend_client_sdk.models.update_account_settings_response import UpdateAccountSettingsResponse
from playbookmedia_backend_client_sdk.models.update_organization_request import UpdateOrganizationRequest
from playbookmedia_backend_client_sdk.models.update_organization_response import UpdateOrganizationResponse
from playbookmedia_backend_client_sdk.models.update_tenant_api_key_request import UpdateTenantAPIKeyRequest
from playbookmedia_backend_client_sdk.models.update_tenant_api_key_response import UpdateTenantAPIKeyResponse
from playbookmedia_backend_client_sdk.models.update_tenant_request import UpdateTenantRequest
from playbookmedia_backend_client_sdk.models.update_tenant_response import UpdateTenantResponse
from playbookmedia_backend_client_sdk.models.update_webhook_request import UpdateWebhookRequest
from playbookmedia_backend_client_sdk.models.update_webhook_response import UpdateWebhookResponse
from playbookmedia_backend_client_sdk.models.update_workflow_request import UpdateWorkflowRequest
from playbookmedia_backend_client_sdk.models.update_workflow_response import UpdateWorkflowResponse
from playbookmedia_backend_client_sdk.models.update_workspace_request import UpdateWorkspaceRequest
from playbookmedia_backend_client_sdk.models.update_workspace_response import UpdateWorkspaceResponse
from playbookmedia_backend_client_sdk.models.update_workspace_sharing_request import UpdateWorkspaceSharingRequest
from playbookmedia_backend_client_sdk.models.update_workspace_sharing_response import UpdateWorkspaceSharingResponse
from playbookmedia_backend_client_sdk.models.user_activity import UserActivity
from playbookmedia_backend_client_sdk.models.v1_status import V1Status
from playbookmedia_backend_client_sdk.models.validation_error_code import ValidationErrorCode
from playbookmedia_backend_client_sdk.models.validation_error_message_response import ValidationErrorMessageResponse
from playbookmedia_backend_client_sdk.models.webhook_config import WebhookConfig
from playbookmedia_backend_client_sdk.models.workflow_status import WorkflowStatus
from playbookmedia_backend_client_sdk.models.workspace import Workspace
from playbookmedia_backend_client_sdk.models.workspace1 import Workspace1
from playbookmedia_backend_client_sdk.models.workspace_activity import WorkspaceActivity
from playbookmedia_backend_client_sdk.models.workspace_compliance import WorkspaceCompliance
from playbookmedia_backend_client_sdk.models.workspace_sharing import WorkspaceSharing
