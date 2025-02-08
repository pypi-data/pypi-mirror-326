# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from canva_alpha_ti.models.export_quality import ExportQuality
from typing import Optional, Set
from typing_extensions import Self

class GifExportFormat(BaseModel):
    """
    Export the design as a GIF. Height or width (or both) may be specified, otherwise the file will be exported at it's default size. Large designs will be scaled down, and aspect ratio will always be maintained.
    """ # noqa: E501
    type: StrictStr
    export_quality: Optional[ExportQuality] = ExportQuality.REGULAR
    height: Optional[Annotated[int, Field(le=25000, strict=True, ge=40)]] = Field(default=None, description="Specify the height in pixels of the exported image. If only one of height or width is specified, then the image will be scaled to match that dimension, respecting the design's aspect ratio. If no width or height is specified, the image will be exported using the dimensions of the design.")
    width: Optional[Annotated[int, Field(le=25000, strict=True, ge=40)]] = Field(default=None, description="Specify the width in pixels of the exported image. If only one of height or width is specified, then the image will be scaled to match that dimension, respecting the design's aspect ratio. If no width or height is specified, the image will be exported using the dimensions of the design.")
    pages: Optional[List[Annotated[int, Field(strict=True, ge=1)]]] = Field(default=None, description="To specify which pages to export in a multi-page design, provide the page numbers as an array. The first page in a design is page `1`. If `pages` isn't specified, all the pages are exported.")
    __properties: ClassVar[List[str]] = ["type", "export_quality", "height", "width", "pages"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['gif']):
            raise ValueError("must be one of enum values ('gif')")
        return value

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
        """Create an instance of GifExportFormat from a JSON string"""
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
        """Create an instance of GifExportFormat from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "export_quality": obj.get("export_quality") if obj.get("export_quality") is not None else ExportQuality.REGULAR,
            "height": obj.get("height"),
            "width": obj.get("width"),
            "pages": obj.get("pages")
        })
        return _obj


