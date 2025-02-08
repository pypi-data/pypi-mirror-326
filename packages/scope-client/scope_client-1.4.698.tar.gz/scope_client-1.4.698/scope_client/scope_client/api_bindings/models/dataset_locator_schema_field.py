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
from scope_client.api_bindings.models.dataset_locator_field_data_type import DatasetLocatorFieldDataType
from typing import Optional, Set
from typing_extensions import Self

class DatasetLocatorSchemaField(BaseModel):
    """
    DatasetLocatorSchemaField
    """ # noqa: E501
    name: StrictStr = Field(description="Name of dataset locator field.")
    d_type: DatasetLocatorFieldDataType = Field(description="Data type of the value stored by the field.")
    is_optional: StrictBool = Field(description="If field is optional or required.")
    description: StrictStr = Field(description="Description of dataset locator schema field.")
    allowed_values: Optional[List[StrictStr]] = None
    __properties: ClassVar[List[str]] = ["name", "d_type", "is_optional", "description", "allowed_values"]

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
        """Create an instance of DatasetLocatorSchemaField from a JSON string"""
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
        # set to None if allowed_values (nullable) is None
        # and model_fields_set contains the field
        if self.allowed_values is None and "allowed_values" in self.model_fields_set:
            _dict['allowed_values'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetLocatorSchemaField from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "d_type": obj.get("d_type"),
            "is_optional": obj.get("is_optional"),
            "description": obj.get("description"),
            "allowed_values": obj.get("allowed_values")
        })
        return _obj


