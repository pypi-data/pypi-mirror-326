# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class DesignImportStatus(str, Enum):
    """
    The status of the design import job.
    """

    """
    allowed enum values
    """
    FAILED = 'failed'
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DesignImportStatus from a JSON string"""
        return cls(json.loads(json_str))


