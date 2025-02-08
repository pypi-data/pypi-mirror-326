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


class DesignImportErrorCode(str, Enum):
    """
    A short string about why the import failed. This field can be used to handle errors programmatically.
    """

    """
    allowed enum values
    """
    DESIGN_CREATION_THROTTLED = 'design_creation_throttled'
    DESIGN_IMPORT_THROTTLED = 'design_import_throttled'
    DUPLICATE_IMPORT = 'duplicate_import'
    INTERNAL_ERROR = 'internal_error'
    INVALID_FILE = 'invalid_file'
    FETCH_FAILED = 'fetch_failed'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DesignImportErrorCode from a JSON string"""
        return cls(json.loads(json_str))


