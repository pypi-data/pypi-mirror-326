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


class Language(str, Enum):
    """
    - LANGUAGE_ENGLISH: en  - LANGUAGE_SPANISH: es  - LANGUAGE_FRENCH: fr  - LANGUAGE_GERMAN: de  - LANGUAGE_ITALIAN: it  - LANGUAGE_PORTUGUESE: pt  - LANGUAGE_DUTCH: nl  - LANGUAGE_RUSSIAN: ru  - LANGUAGE_CHINESE: zh  - LANGUAGE_JAPANESE: ja  - LANGUAGE_KOREAN: ko  - LANGUAGE_ARABIC: ar  - LANGUAGE_HINDI: hi  - LANGUAGE_GREEK: el  - LANGUAGE_TURKISH: tr
    """

    """
    allowed enum values
    """
    LANGUAGE_UNSPECIFIED = 'LANGUAGE_UNSPECIFIED'
    LANGUAGE_ENGLISH = 'LANGUAGE_ENGLISH'
    LANGUAGE_SPANISH = 'LANGUAGE_SPANISH'
    LANGUAGE_FRENCH = 'LANGUAGE_FRENCH'
    LANGUAGE_GERMAN = 'LANGUAGE_GERMAN'
    LANGUAGE_ITALIAN = 'LANGUAGE_ITALIAN'
    LANGUAGE_PORTUGUESE = 'LANGUAGE_PORTUGUESE'
    LANGUAGE_DUTCH = 'LANGUAGE_DUTCH'
    LANGUAGE_RUSSIAN = 'LANGUAGE_RUSSIAN'
    LANGUAGE_CHINESE = 'LANGUAGE_CHINESE'
    LANGUAGE_JAPANESE = 'LANGUAGE_JAPANESE'
    LANGUAGE_KOREAN = 'LANGUAGE_KOREAN'
    LANGUAGE_ARABIC = 'LANGUAGE_ARABIC'
    LANGUAGE_HINDI = 'LANGUAGE_HINDI'
    LANGUAGE_GREEK = 'LANGUAGE_GREEK'
    LANGUAGE_TURKISH = 'LANGUAGE_TURKISH'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Language from a JSON string"""
        return cls(json.loads(json_str))


