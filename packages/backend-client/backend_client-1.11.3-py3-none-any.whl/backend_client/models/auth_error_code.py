# coding: utf-8

"""
    Lead Scraping Service API

    Vector Lead Scraping Service API - Manages Lead Scraping Jobs

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@vector.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class AuthErrorCode(str, Enum):
    """
    - AUTH_FAILED_INVALID_BEARER_TOKEN: Authentication errors  - SESSION_EXPIRED: Session errors  - UNAUTHENTICATED: Other authentication errors  - ACCOUNT_LOCKED: New authentication error codes  Account is locked due to too many failed login attempts  - ACCOUNT_DISABLED: Account has been disabled by admin  - PASSWORD_EXPIRED: Password has expired and must be changed  - PASSWORD_RESET_REQUIRED: Password reset is required  - UNRECOGNIZED_DEVICE: Login attempt from an unrecognized device
    """

    """
    allowed enum values
    """
    NO_AUTH_ERROR = 'NO_AUTH_ERROR'
    AUTH_FAILED_INVALID_BEARER_TOKEN = 'AUTH_FAILED_INVALID_BEARER_TOKEN'
    AUTH_FAILED_INVALID_SUBJECT = 'AUTH_FAILED_INVALID_SUBJECT'
    AUTH_FAILED_INVALID_AUDIENCE = 'AUTH_FAILED_INVALID_AUDIENCE'
    AUTH_FAILED_INVALID_ISSUER = 'AUTH_FAILED_INVALID_ISSUER'
    BEARER_TOKEN_MISSING = 'BEARER_TOKEN_MISSING'
    TOKEN_EXPIRED = 'TOKEN_EXPIRED'
    TOKEN_NOT_ACTIVE = 'TOKEN_NOT_ACTIVE'
    TOKEN_REVOKED = 'TOKEN_REVOKED'
    INVALID_CLAIMS = 'INVALID_CLAIMS'
    MISSING_REQUIRED_CLAIMS = 'MISSING_REQUIRED_CLAIMS'
    INVALID_SCOPE = 'INVALID_SCOPE'
    INVALID_PERMISSIONS = 'INVALID_PERMISSIONS'
    SESSION_EXPIRED = 'SESSION_EXPIRED'
    SESSION_INVALID = 'SESSION_INVALID'
    SESSION_REVOKED = 'SESSION_REVOKED'
    UNAUTHENTICATED = 'UNAUTHENTICATED'
    MULTI_FACTOR_REQUIRED = 'MULTI_FACTOR_REQUIRED'
    MULTI_FACTOR_FAILED = 'MULTI_FACTOR_FAILED'
    ACCOUNT_LOCKED = 'ACCOUNT_LOCKED'
    ACCOUNT_DISABLED = 'ACCOUNT_DISABLED'
    PASSWORD_EXPIRED = 'PASSWORD_EXPIRED'
    PASSWORD_RESET_REQUIRED = 'PASSWORD_RESET_REQUIRED'
    UNRECOGNIZED_DEVICE = 'UNRECOGNIZED_DEVICE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AuthErrorCode from a JSON string"""
        return cls(json.loads(json_str))


