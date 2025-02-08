# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, SecretStr, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class SensitiveDataPlane(BaseModel):
    """
    SensitiveDataPlane
    """ # noqa: E501
    created_at: datetime = Field(description="Time of record creation.")
    updated_at: datetime = Field(description="Time of last record update.")
    id: StrictStr = Field(description="ID of the data plane.")
    name: StrictStr = Field(description="Name of data plane.")
    workspace_id: StrictStr = Field(description="ID of the parent workspace.")
    description: StrictStr = Field(description="Description of data plane.")
    user_id: StrictStr = Field(description="ID of the data plane's underlying user.")
    client_id: SecretStr = Field(description="ID of the auth client.")
    client_secret: SecretStr = Field(description="Auth client secret.")
    __properties: ClassVar[List[str]] = ["created_at", "updated_at", "id", "name", "workspace_id", "description", "user_id", "client_id", "client_secret"]

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
        """Create an instance of SensitiveDataPlane from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SensitiveDataPlane from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "id": obj.get("id"),
            "name": obj.get("name"),
            "workspace_id": obj.get("workspace_id"),
            "description": obj.get("description"),
            "user_id": obj.get("user_id"),
            "client_id": obj.get("client_id"),
            "client_secret": obj.get("client_secret")
        })
        return _obj


