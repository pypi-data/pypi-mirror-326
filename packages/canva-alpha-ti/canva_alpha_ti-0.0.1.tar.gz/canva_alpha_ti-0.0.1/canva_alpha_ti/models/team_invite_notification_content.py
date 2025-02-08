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

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List
from canva_alpha_ti.models.team import Team
from canva_alpha_ti.models.user import User
from typing import Optional, Set
from typing_extensions import Self

class TeamInviteNotificationContent(BaseModel):
    """
    The notification content for when someone is invited to a [Canva team](https://www.canva.com/help/about-canva-for-teams/).
    """ # noqa: E501
    type: StrictStr
    triggering_user: User
    receiving_user: User
    inviting_team: Team
    __properties: ClassVar[List[str]] = ["type", "triggering_user", "receiving_user", "inviting_team"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['team_invite']):
            raise ValueError("must be one of enum values ('team_invite')")
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
        """Create an instance of TeamInviteNotificationContent from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of triggering_user
        if self.triggering_user:
            _dict['triggering_user'] = self.triggering_user.to_dict()
        # override the default output from pydantic by calling `to_dict()` of receiving_user
        if self.receiving_user:
            _dict['receiving_user'] = self.receiving_user.to_dict()
        # override the default output from pydantic by calling `to_dict()` of inviting_team
        if self.inviting_team:
            _dict['inviting_team'] = self.inviting_team.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TeamInviteNotificationContent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "triggering_user": User.from_dict(obj["triggering_user"]) if obj.get("triggering_user") is not None else None,
            "receiving_user": User.from_dict(obj["receiving_user"]) if obj.get("receiving_user") is not None else None,
            "inviting_team": Team.from_dict(obj["inviting_team"]) if obj.get("inviting_team") is not None else None
        })
        return _obj


