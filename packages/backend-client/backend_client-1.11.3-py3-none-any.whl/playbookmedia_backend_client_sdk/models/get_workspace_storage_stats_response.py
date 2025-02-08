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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from playbookmedia_backend_client_sdk.models.storage_breakdown import StorageBreakdown
from typing import Optional, Set
from typing_extensions import Self

class GetWorkspaceStorageStatsResponse(BaseModel):
    """
    GetWorkspaceStorageStatsResponse
    """ # noqa: E501
    total_storage_used: Optional[StrictStr] = Field(default=None, alias="totalStorageUsed")
    storage_quota: Optional[StrictStr] = Field(default=None, alias="storageQuota")
    usage_percentage: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="usagePercentage")
    storage_by_type: Optional[List[StorageBreakdown]] = Field(default=None, alias="storageByType")
    total_files: Optional[StrictInt] = Field(default=None, alias="totalFiles")
    total_folders: Optional[StrictInt] = Field(default=None, alias="totalFolders")
    last_updated: Optional[datetime] = Field(default=None, alias="lastUpdated")
    __properties: ClassVar[List[str]] = ["totalStorageUsed", "storageQuota", "usagePercentage", "storageByType", "totalFiles", "totalFolders", "lastUpdated"]

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
        """Create an instance of GetWorkspaceStorageStatsResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in storage_by_type (list)
        _items = []
        if self.storage_by_type:
            for _item in self.storage_by_type:
                if _item:
                    _items.append(_item.to_dict())
            _dict['storageByType'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetWorkspaceStorageStatsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "totalStorageUsed": obj.get("totalStorageUsed"),
            "storageQuota": obj.get("storageQuota"),
            "usagePercentage": obj.get("usagePercentage"),
            "storageByType": [StorageBreakdown.from_dict(_item) for _item in obj["storageByType"]] if obj.get("storageByType") is not None else None,
            "totalFiles": obj.get("totalFiles"),
            "totalFolders": obj.get("totalFolders"),
            "lastUpdated": obj.get("lastUpdated")
        })
        return _obj


