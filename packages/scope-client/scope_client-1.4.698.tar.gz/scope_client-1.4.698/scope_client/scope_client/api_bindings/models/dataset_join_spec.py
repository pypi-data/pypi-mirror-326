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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from scope_client.api_bindings.models.dataset_join_kind import DatasetJoinKind
from scope_client.api_bindings.models.joined_dataset import JoinedDataset
from typing import Optional, Set
from typing_extensions import Self

class DatasetJoinSpec(BaseModel):
    """
    DatasetJoinSpec
    """ # noqa: E501
    left_joined_dataset: JoinedDataset = Field(description="Left dataset in the join.")
    right_joined_dataset: JoinedDataset = Field(description="Right dataset in the join.")
    join_type: Optional[DatasetJoinKind] = Field(default=None, description="Kind of SQL join to perform")
    __properties: ClassVar[List[str]] = ["left_joined_dataset", "right_joined_dataset", "join_type"]

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
        """Create an instance of DatasetJoinSpec from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of left_joined_dataset
        if self.left_joined_dataset:
            _dict['left_joined_dataset'] = self.left_joined_dataset.to_dict()
        # override the default output from pydantic by calling `to_dict()` of right_joined_dataset
        if self.right_joined_dataset:
            _dict['right_joined_dataset'] = self.right_joined_dataset.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetJoinSpec from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "left_joined_dataset": JoinedDataset.from_dict(obj["left_joined_dataset"]) if obj.get("left_joined_dataset") is not None else None,
            "right_joined_dataset": JoinedDataset.from_dict(obj["right_joined_dataset"]) if obj.get("right_joined_dataset") is not None else None,
            "join_type": obj.get("join_type")
        })
        return _obj


