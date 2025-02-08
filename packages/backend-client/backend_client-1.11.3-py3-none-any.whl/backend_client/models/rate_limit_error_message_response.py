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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from backend_client.models.error_response import ErrorResponse
from backend_client.models.internal_error_code import InternalErrorCode
from backend_client.models.limit_info import LimitInfo
from backend_client.models.quota_info import QuotaInfo
from backend_client.models.rate_limit_context import RateLimitContext
from typing import Optional, Set
from typing_extensions import Self

class RateLimitErrorMessageResponse(BaseModel):
    """
    Represents rate limiting and quota exceeded errors
    """ # noqa: E501
    code: Optional[InternalErrorCode] = InternalErrorCode.NO_INTERNAL_ERROR
    message: Optional[StrictStr] = None
    limit_info: Optional[LimitInfo] = Field(default=None, alias="limitInfo")
    quota_info: Optional[QuotaInfo] = Field(default=None, alias="quotaInfo")
    context: Optional[RateLimitContext] = None
    error_response: Optional[ErrorResponse] = Field(default=None, alias="errorResponse")
    __properties: ClassVar[List[str]] = ["code", "message", "limitInfo", "quotaInfo", "context", "errorResponse"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RateLimitErrorMessageResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of limit_info
        if self.limit_info:
            _dict['limitInfo'] = self.limit_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of quota_info
        if self.quota_info:
            _dict['quotaInfo'] = self.quota_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of context
        if self.context:
            _dict['context'] = self.context.to_dict()
        # override the default output from pydantic by calling `to_dict()` of error_response
        if self.error_response:
            _dict['errorResponse'] = self.error_response.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RateLimitErrorMessageResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "code": obj.get("code") if obj.get("code") is not None else InternalErrorCode.NO_INTERNAL_ERROR,
            "message": obj.get("message"),
            "limitInfo": LimitInfo.from_dict(obj["limitInfo"]) if obj.get("limitInfo") is not None else None,
            "quotaInfo": QuotaInfo.from_dict(obj["quotaInfo"]) if obj.get("quotaInfo") is not None else None,
            "context": RateLimitContext.from_dict(obj["context"]) if obj.get("context") is not None else None,
            "errorResponse": ErrorResponse.from_dict(obj["errorResponse"]) if obj.get("errorResponse") is not None else None
        })
        return _obj


