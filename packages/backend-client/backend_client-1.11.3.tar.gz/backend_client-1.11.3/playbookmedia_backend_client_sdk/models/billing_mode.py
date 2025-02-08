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


class BillingMode(str, Enum):
    """
    - BILLING_MODE_LICENSED: Fixed price per seat  - BILLING_MODE_METERED: Usage-based  - BILLING_MODE_HYBRID: Base price + usage
    """

    """
    allowed enum values
    """
    BILLING_MODE_UNSPECIFIED = 'BILLING_MODE_UNSPECIFIED'
    BILLING_MODE_LICENSED = 'BILLING_MODE_LICENSED'
    BILLING_MODE_METERED = 'BILLING_MODE_METERED'
    BILLING_MODE_HYBRID = 'BILLING_MODE_HYBRID'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BillingMode from a JSON string"""
        return cls(json.loads(json_str))


