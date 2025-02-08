# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class DataResultFilterOp(str, Enum):
    """
    DataResultFilterOp
    """

    """
    allowed enum values
    """
    GREATER_THAN = 'greater_than'
    LESS_THAN = 'less_than'
    EQUALS = 'equals'
    NOT_EQUALS = 'not_equals'
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal'
    LESS_THAN_OR_EQUAL = 'less_than_or_equal'
    IN = 'in'
    NOT_IN = 'not_in'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DataResultFilterOp from a JSON string"""
        return cls(json.loads(json_str))


