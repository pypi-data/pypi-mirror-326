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


class OutputFormat(str, Enum):
    """
    OutputFormat
    """

    """
    allowed enum values
    """
    OUTPUT_FORMAT_UNSPECIFIED = 'OUTPUT_FORMAT_UNSPECIFIED'
    OUTPUT_FORMAT_JSON = 'OUTPUT_FORMAT_JSON'
    OUTPUT_FORMAT_CSV = 'OUTPUT_FORMAT_CSV'
    OUTPUT_FORMAT_BIGQUERY = 'OUTPUT_FORMAT_BIGQUERY'
    OUTPUT_FORMAT_POSTGRES = 'OUTPUT_FORMAT_POSTGRES'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of OutputFormat from a JSON string"""
        return cls(json.loads(json_str))


