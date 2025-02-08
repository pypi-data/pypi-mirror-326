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


class JobPriority(int, Enum):
    """
    JobPriority
    """

    """
    allowed enum values
    """
    NUMBER_100 = 100
    NUMBER_200 = 200
    NUMBER_300 = 300
    NUMBER_400 = 400

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of JobPriority from a JSON string"""
        return cls(json.loads(json_str))


