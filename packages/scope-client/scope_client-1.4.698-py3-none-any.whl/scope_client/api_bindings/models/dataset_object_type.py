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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from scope_client.api_bindings.models.scope_schema_tag import ScopeSchemaTag
from typing import Optional, Set
from typing_extensions import Self

class DatasetObjectType(BaseModel):
    """
    DatasetObjectType
    """ # noqa: E501
    tag_hints: Optional[List[ScopeSchemaTag]] = None
    nullable: Optional[StrictBool] = None
    id: Optional[StrictStr] = Field(default=None, description="Unique ID of the schema node.")
    object: Dict[str, ObjectValue]
    __properties: ClassVar[List[str]] = ["tag_hints", "nullable", "id", "object"]

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
        """Create an instance of DatasetObjectType from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in object (dict)
        _field_dict = {}
        if self.object:
            for _key_object in self.object:
                if self.object[_key_object]:
                    _field_dict[_key_object] = self.object[_key_object].to_dict()
            _dict['object'] = _field_dict
        # set to None if nullable (nullable) is None
        # and model_fields_set contains the field
        if self.nullable is None and "nullable" in self.model_fields_set:
            _dict['nullable'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetObjectType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "tag_hints": obj.get("tag_hints"),
            "nullable": obj.get("nullable"),
            "id": obj.get("id"),
            "object": dict(
                (_k, ObjectValue.from_dict(_v))
                for _k, _v in obj["object"].items()
            )
            if obj.get("object") is not None
            else None
        })
        return _obj

from scope_client.api_bindings.models.object_value import ObjectValue
# TODO: Rewrite to not use raise_errors
DatasetObjectType.model_rebuild(raise_errors=False)

