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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from backend_client.models.error_response import ErrorResponse
from typing import Optional, Set
from typing_extensions import Self

class GatewayTimeoutErrorMessageResponse(BaseModel):
    """
    Represents errors when the server did not receive a timely response from an upstream server
    """ # noqa: E501
    code: Optional[StrictInt] = None
    message: Optional[StrictStr] = None
    upstream_service: Optional[StrictStr] = Field(default=None, alias="upstreamService")
    error_response: Optional[ErrorResponse] = Field(default=None, alias="errorResponse")
    __properties: ClassVar[List[str]] = ["code", "message", "upstreamService", "errorResponse"]

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
        """Create an instance of GatewayTimeoutErrorMessageResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of error_response
        if self.error_response:
            _dict['errorResponse'] = self.error_response.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GatewayTimeoutErrorMessageResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "code": obj.get("code"),
            "message": obj.get("message"),
            "upstreamService": obj.get("upstreamService"),
            "errorResponse": ErrorResponse.from_dict(obj["errorResponse"]) if obj.get("errorResponse") is not None else None
        })
        return _obj


