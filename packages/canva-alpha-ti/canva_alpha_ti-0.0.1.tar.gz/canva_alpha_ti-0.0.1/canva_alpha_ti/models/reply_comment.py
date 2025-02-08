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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from canva_alpha_ti.models.comment_object import CommentObject
from canva_alpha_ti.models.user import User
from typing import Optional, Set
from typing_extensions import Self

class ReplyComment(BaseModel):
    """
    Data about the reply comment, including the message, author, and the object (such as a design) the comment is attached to.
    """ # noqa: E501
    type: StrictStr
    id: StrictStr = Field(description="The ID of the comment.")
    attached_to: Optional[CommentObject] = None
    message: StrictStr = Field(description="The comment message. This is the comment body shown in the Canva UI. User mentions are shown here in the format `[user_id:team_id]`.")
    author: User
    created_at: Optional[StrictInt] = Field(default=None, description="When the comment or reply was created, as a Unix timestamp (in seconds since the Unix Epoch).")
    updated_at: Optional[StrictInt] = Field(default=None, description="When the comment or reply was last updated, as a Unix timestamp (in seconds since the Unix Epoch).")
    mentions: Dict[str, Any] = Field(description="The Canva users mentioned in the comment.")
    thread_id: StrictStr = Field(description="The ID of the comment thread this reply is in. This ID is the same as the `id` of the parent comment.")
    __properties: ClassVar[List[str]] = ["type", "id", "attached_to", "message", "author", "created_at", "updated_at", "mentions", "thread_id"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['reply']):
            raise ValueError("must be one of enum values ('reply')")
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
        """Create an instance of ReplyComment from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of attached_to
        if self.attached_to:
            _dict['attached_to'] = self.attached_to.to_dict()
        # override the default output from pydantic by calling `to_dict()` of author
        if self.author:
            _dict['author'] = self.author.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ReplyComment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "id": obj.get("id"),
            "attached_to": CommentObject.from_dict(obj["attached_to"]) if obj.get("attached_to") is not None else None,
            "message": obj.get("message"),
            "author": User.from_dict(obj["author"]) if obj.get("author") is not None else None,
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "mentions": obj.get("mentions"),
            "thread_id": obj.get("thread_id")
        })
        return _obj


