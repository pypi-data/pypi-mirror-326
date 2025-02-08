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
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from canva_alpha_ti.models.comment_notification_content import CommentNotificationContent
from canva_alpha_ti.models.design_access_requested_notification_content import DesignAccessRequestedNotificationContent
from canva_alpha_ti.models.design_approval_requested_notification_content import DesignApprovalRequestedNotificationContent
from canva_alpha_ti.models.design_approval_response_notification_content import DesignApprovalResponseNotificationContent
from canva_alpha_ti.models.design_approval_reviewer_invalidated_notification_content import DesignApprovalReviewerInvalidatedNotificationContent
from canva_alpha_ti.models.design_mention_notification_content import DesignMentionNotificationContent
from canva_alpha_ti.models.folder_access_requested_notification_content import FolderAccessRequestedNotificationContent
from canva_alpha_ti.models.share_design_notification_content import ShareDesignNotificationContent
from canva_alpha_ti.models.share_folder_notification_content import ShareFolderNotificationContent
from canva_alpha_ti.models.suggestion_notification_content import SuggestionNotificationContent
from canva_alpha_ti.models.team_invite_notification_content import TeamInviteNotificationContent
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

NOTIFICATIONCONTENT_ONE_OF_SCHEMAS = ["CommentNotificationContent", "DesignAccessRequestedNotificationContent", "DesignApprovalRequestedNotificationContent", "DesignApprovalResponseNotificationContent", "DesignApprovalReviewerInvalidatedNotificationContent", "DesignMentionNotificationContent", "FolderAccessRequestedNotificationContent", "ShareDesignNotificationContent", "ShareFolderNotificationContent", "SuggestionNotificationContent", "TeamInviteNotificationContent"]

class NotificationContent(BaseModel):
    """
    The notification content object, which contains metadata about the event.
    """
    # data type: ShareDesignNotificationContent
    oneof_schema_1_validator: Optional[ShareDesignNotificationContent] = None
    # data type: ShareFolderNotificationContent
    oneof_schema_2_validator: Optional[ShareFolderNotificationContent] = None
    # data type: CommentNotificationContent
    oneof_schema_3_validator: Optional[CommentNotificationContent] = None
    # data type: DesignAccessRequestedNotificationContent
    oneof_schema_4_validator: Optional[DesignAccessRequestedNotificationContent] = None
    # data type: DesignApprovalRequestedNotificationContent
    oneof_schema_5_validator: Optional[DesignApprovalRequestedNotificationContent] = None
    # data type: DesignApprovalResponseNotificationContent
    oneof_schema_6_validator: Optional[DesignApprovalResponseNotificationContent] = None
    # data type: DesignApprovalReviewerInvalidatedNotificationContent
    oneof_schema_7_validator: Optional[DesignApprovalReviewerInvalidatedNotificationContent] = None
    # data type: DesignMentionNotificationContent
    oneof_schema_8_validator: Optional[DesignMentionNotificationContent] = None
    # data type: TeamInviteNotificationContent
    oneof_schema_9_validator: Optional[TeamInviteNotificationContent] = None
    # data type: FolderAccessRequestedNotificationContent
    oneof_schema_10_validator: Optional[FolderAccessRequestedNotificationContent] = None
    # data type: SuggestionNotificationContent
    oneof_schema_11_validator: Optional[SuggestionNotificationContent] = None
    actual_instance: Optional[Union[CommentNotificationContent, DesignAccessRequestedNotificationContent, DesignApprovalRequestedNotificationContent, DesignApprovalResponseNotificationContent, DesignApprovalReviewerInvalidatedNotificationContent, DesignMentionNotificationContent, FolderAccessRequestedNotificationContent, ShareDesignNotificationContent, ShareFolderNotificationContent, SuggestionNotificationContent, TeamInviteNotificationContent]] = None
    one_of_schemas: Set[str] = { "CommentNotificationContent", "DesignAccessRequestedNotificationContent", "DesignApprovalRequestedNotificationContent", "DesignApprovalResponseNotificationContent", "DesignApprovalReviewerInvalidatedNotificationContent", "DesignMentionNotificationContent", "FolderAccessRequestedNotificationContent", "ShareDesignNotificationContent", "ShareFolderNotificationContent", "SuggestionNotificationContent", "TeamInviteNotificationContent" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = NotificationContent.model_construct()
        error_messages = []
        match = 0
        # validate data type: ShareDesignNotificationContent
        if not isinstance(v, ShareDesignNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `ShareDesignNotificationContent`")
        else:
            match += 1
        # validate data type: ShareFolderNotificationContent
        if not isinstance(v, ShareFolderNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `ShareFolderNotificationContent`")
        else:
            match += 1
        # validate data type: CommentNotificationContent
        if not isinstance(v, CommentNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `CommentNotificationContent`")
        else:
            match += 1
        # validate data type: DesignAccessRequestedNotificationContent
        if not isinstance(v, DesignAccessRequestedNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DesignAccessRequestedNotificationContent`")
        else:
            match += 1
        # validate data type: DesignApprovalRequestedNotificationContent
        if not isinstance(v, DesignApprovalRequestedNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DesignApprovalRequestedNotificationContent`")
        else:
            match += 1
        # validate data type: DesignApprovalResponseNotificationContent
        if not isinstance(v, DesignApprovalResponseNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DesignApprovalResponseNotificationContent`")
        else:
            match += 1
        # validate data type: DesignApprovalReviewerInvalidatedNotificationContent
        if not isinstance(v, DesignApprovalReviewerInvalidatedNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DesignApprovalReviewerInvalidatedNotificationContent`")
        else:
            match += 1
        # validate data type: DesignMentionNotificationContent
        if not isinstance(v, DesignMentionNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DesignMentionNotificationContent`")
        else:
            match += 1
        # validate data type: TeamInviteNotificationContent
        if not isinstance(v, TeamInviteNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TeamInviteNotificationContent`")
        else:
            match += 1
        # validate data type: FolderAccessRequestedNotificationContent
        if not isinstance(v, FolderAccessRequestedNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FolderAccessRequestedNotificationContent`")
        else:
            match += 1
        # validate data type: SuggestionNotificationContent
        if not isinstance(v, SuggestionNotificationContent):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SuggestionNotificationContent`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in NotificationContent with oneOf schemas: CommentNotificationContent, DesignAccessRequestedNotificationContent, DesignApprovalRequestedNotificationContent, DesignApprovalResponseNotificationContent, DesignApprovalReviewerInvalidatedNotificationContent, DesignMentionNotificationContent, FolderAccessRequestedNotificationContent, ShareDesignNotificationContent, ShareFolderNotificationContent, SuggestionNotificationContent, TeamInviteNotificationContent. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in NotificationContent with oneOf schemas: CommentNotificationContent, DesignAccessRequestedNotificationContent, DesignApprovalRequestedNotificationContent, DesignApprovalResponseNotificationContent, DesignApprovalReviewerInvalidatedNotificationContent, DesignMentionNotificationContent, FolderAccessRequestedNotificationContent, ShareDesignNotificationContent, ShareFolderNotificationContent, SuggestionNotificationContent, TeamInviteNotificationContent. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into ShareDesignNotificationContent
        try:
            instance.actual_instance = ShareDesignNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into ShareFolderNotificationContent
        try:
            instance.actual_instance = ShareFolderNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into CommentNotificationContent
        try:
            instance.actual_instance = CommentNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DesignAccessRequestedNotificationContent
        try:
            instance.actual_instance = DesignAccessRequestedNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DesignApprovalRequestedNotificationContent
        try:
            instance.actual_instance = DesignApprovalRequestedNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DesignApprovalResponseNotificationContent
        try:
            instance.actual_instance = DesignApprovalResponseNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DesignApprovalReviewerInvalidatedNotificationContent
        try:
            instance.actual_instance = DesignApprovalReviewerInvalidatedNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DesignMentionNotificationContent
        try:
            instance.actual_instance = DesignMentionNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into TeamInviteNotificationContent
        try:
            instance.actual_instance = TeamInviteNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FolderAccessRequestedNotificationContent
        try:
            instance.actual_instance = FolderAccessRequestedNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SuggestionNotificationContent
        try:
            instance.actual_instance = SuggestionNotificationContent.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into NotificationContent with oneOf schemas: CommentNotificationContent, DesignAccessRequestedNotificationContent, DesignApprovalRequestedNotificationContent, DesignApprovalResponseNotificationContent, DesignApprovalReviewerInvalidatedNotificationContent, DesignMentionNotificationContent, FolderAccessRequestedNotificationContent, ShareDesignNotificationContent, ShareFolderNotificationContent, SuggestionNotificationContent, TeamInviteNotificationContent. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into NotificationContent with oneOf schemas: CommentNotificationContent, DesignAccessRequestedNotificationContent, DesignApprovalRequestedNotificationContent, DesignApprovalResponseNotificationContent, DesignApprovalReviewerInvalidatedNotificationContent, DesignMentionNotificationContent, FolderAccessRequestedNotificationContent, ShareDesignNotificationContent, ShareFolderNotificationContent, SuggestionNotificationContent, TeamInviteNotificationContent. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], CommentNotificationContent, DesignAccessRequestedNotificationContent, DesignApprovalRequestedNotificationContent, DesignApprovalResponseNotificationContent, DesignApprovalReviewerInvalidatedNotificationContent, DesignMentionNotificationContent, FolderAccessRequestedNotificationContent, ShareDesignNotificationContent, ShareFolderNotificationContent, SuggestionNotificationContent, TeamInviteNotificationContent]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


