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

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from playbookmedia_backend_client_sdk.models.lead import Lead
from typing import Optional, Set
from typing_extensions import Self

class ListLeadsResponse(BaseModel):
    """
    ListLeadsResponse
    """ # noqa: E501
    leads: Optional[List[Lead]] = None
    total_count: Optional[StrictInt] = Field(default=None, alias="totalCount")
    next_page_number: Optional[StrictInt] = Field(default=None, alias="nextPageNumber")
    __properties: ClassVar[List[str]] = ["leads", "totalCount", "nextPageNumber"]

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
        """Create an instance of ListLeadsResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in leads (list)
        _items = []
        if self.leads:
            for _item in self.leads:
                if _item:
                    _items.append(_item.to_dict())
            _dict['leads'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ListLeadsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "leads": [Lead.from_dict(_item) for _item in obj["leads"]] if obj.get("leads") is not None else None,
            "totalCount": obj.get("totalCount"),
            "nextPageNumber": obj.get("nextPageNumber")
        })
        return _obj


