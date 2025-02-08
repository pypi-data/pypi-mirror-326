# coding: utf-8

"""
    Canva Connect API

    API for building integrations with Canva via a REST api

    The version of the OpenAPI document: latest
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import Field, field_validator
from typing_extensions import Annotated
from canva_alpha_ti.models.create_comment_request import CreateCommentRequest
from canva_alpha_ti.models.create_comment_response import CreateCommentResponse
from canva_alpha_ti.models.create_reply_request import CreateReplyRequest
from canva_alpha_ti.models.create_reply_response import CreateReplyResponse
from canva_alpha_ti.models.get_comment_response import GetCommentResponse

from canva_alpha_ti.api_client import ApiClient, RequestSerialized
from canva_alpha_ti.api_response import ApiResponse
from canva_alpha_ti.rest import RESTResponseType


class CommentApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def create_comment(
        self,
        create_comment_request: CreateCommentRequest,
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> CreateCommentResponse:
        """create_comment

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Create a new top-level comment on a design. For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/). A design can have a maximum of 1000 comments.

        :param create_comment_request: (required)
        :type create_comment_request: CreateCommentRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_comment_serialize(
            create_comment_request=create_comment_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateCommentResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def create_comment_with_http_info(
        self,
        create_comment_request: CreateCommentRequest,
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> ApiResponse[CreateCommentResponse]:
        """create_comment

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Create a new top-level comment on a design. For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/). A design can have a maximum of 1000 comments.

        :param create_comment_request: (required)
        :type create_comment_request: CreateCommentRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_comment_serialize(
            create_comment_request=create_comment_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateCommentResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def create_comment_without_preload_content(
        self,
        create_comment_request: CreateCommentRequest,
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> RESTResponseType:
        """create_comment

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Create a new top-level comment on a design. For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/). A design can have a maximum of 1000 comments.

        :param create_comment_request: (required)
        :type create_comment_request: CreateCommentRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_comment_serialize(
            create_comment_request=create_comment_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateCommentResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _create_comment_serialize(
        self,
        create_comment_request,
        request_auth__,
        content_type__,
        headers__,
        host__,
    ) -> RequestSerialized:


        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = headers__ or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if create_comment_request is not None:
            _body_params = create_comment_request


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if content_type__:
            _header_params['Content-Type'] = content_type__
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
            'oauthAuthCode'
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1/comments',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            host__=host__,
            request_auth__=request_auth__
        )




    @validate_call
    def create_reply(
        self,
        comment_id: Annotated[str, Field(strict=True, description="The `id` of the comment.")],
        create_reply_request: CreateReplyRequest,
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> CreateReplyResponse:
        """create_reply

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Creates a reply to a comment in a design. To reply to an existing thread of comments, you can use either the `id` of the parent (original) comment, or the `thread_id` of a comment in the thread. Each comment can have a maximum of 100 replies created for it.  For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/).

        :param comment_id: The `id` of the comment. (required)
        :type comment_id: str
        :param create_reply_request: (required)
        :type create_reply_request: CreateReplyRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_reply_serialize(
            comment_id=comment_id,
            create_reply_request=create_reply_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateReplyResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def create_reply_with_http_info(
        self,
        comment_id: Annotated[str, Field(strict=True, description="The `id` of the comment.")],
        create_reply_request: CreateReplyRequest,
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> ApiResponse[CreateReplyResponse]:
        """create_reply

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Creates a reply to a comment in a design. To reply to an existing thread of comments, you can use either the `id` of the parent (original) comment, or the `thread_id` of a comment in the thread. Each comment can have a maximum of 100 replies created for it.  For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/).

        :param comment_id: The `id` of the comment. (required)
        :type comment_id: str
        :param create_reply_request: (required)
        :type create_reply_request: CreateReplyRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_reply_serialize(
            comment_id=comment_id,
            create_reply_request=create_reply_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateReplyResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def create_reply_without_preload_content(
        self,
        comment_id: Annotated[str, Field(strict=True, description="The `id` of the comment.")],
        create_reply_request: CreateReplyRequest,
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> RESTResponseType:
        """create_reply

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Creates a reply to a comment in a design. To reply to an existing thread of comments, you can use either the `id` of the parent (original) comment, or the `thread_id` of a comment in the thread. Each comment can have a maximum of 100 replies created for it.  For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/).

        :param comment_id: The `id` of the comment. (required)
        :type comment_id: str
        :param create_reply_request: (required)
        :type create_reply_request: CreateReplyRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_reply_serialize(
            comment_id=comment_id,
            create_reply_request=create_reply_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateReplyResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _create_reply_serialize(
        self,
        comment_id,
        create_reply_request,
        request_auth__,
        content_type__,
        headers__,
        host__,
    ) -> RequestSerialized:


        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = headers__ or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if comment_id is not None:
            _path_params['commentId'] = comment_id
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if create_reply_request is not None:
            _body_params = create_reply_request


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if content_type__:
            _header_params['Content-Type'] = content_type__
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
            'oauthAuthCode'
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1/comments/{commentId}/replies',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            host__=host__,
            request_auth__=request_auth__
        )




    @validate_call
    def get_comment(
        self,
        design_id: Annotated[str, Field(strict=True, description="The design ID.")],
        comment_id: Annotated[str, Field(strict=True, description="The `id` of the comment.")],
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> GetCommentResponse:
        """get_comment

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Gets a comment. For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/).

        :param design_id: The design ID. (required)
        :type design_id: str
        :param comment_id: The `id` of the comment. (required)
        :type comment_id: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_comment_serialize(
            design_id=design_id,
            comment_id=comment_id,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetCommentResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def get_comment_with_http_info(
        self,
        design_id: Annotated[str, Field(strict=True, description="The design ID.")],
        comment_id: Annotated[str, Field(strict=True, description="The `id` of the comment.")],
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> ApiResponse[GetCommentResponse]:
        """get_comment

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Gets a comment. For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/).

        :param design_id: The design ID. (required)
        :type design_id: str
        :param comment_id: The `id` of the comment. (required)
        :type comment_id: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_comment_serialize(
            design_id=design_id,
            comment_id=comment_id,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetCommentResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def get_comment_without_preload_content(
        self,
        design_id: Annotated[str, Field(strict=True, description="The design ID.")],
        comment_id: Annotated[str, Field(strict=True, description="The `id` of the comment.")],
        request_timeout__: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        request_auth__: Optional[Dict[StrictStr, Any]] = None,
        content_type__: Optional[StrictStr] = None,
        headers__: Optional[Dict[StrictStr, Any]] = None,
        host__: Optional[StrictStr] = None,
    ) -> RESTResponseType:
        """get_comment

        <Warning>  This API is currently provided as a preview. Be aware of the following:  - There might be unannounced breaking changes. - Any breaking changes to preview APIs won't produce a new [API version](https://www.canva.dev/docs/connect/versions/). - Public integrations that use preview APIs will not pass the review process, and can't be made available to all Canva users.  </Warning>  Gets a comment. For information on comments and how they're used in the Canva UI, see the [Canva Help Center](https://www.canva.com/help/comments/).

        :param design_id: The design ID. (required)
        :type design_id: str
        :param comment_id: The `id` of the comment. (required)
        :type comment_id: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_comment_serialize(
            design_id=design_id,
            comment_id=comment_id,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetCommentResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _get_comment_serialize(
        self,
        design_id,
        comment_id,
        request_auth__,
        content_type__,
        headers__,
        host__,
    ) -> RequestSerialized:


        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = headers__ or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if design_id is not None:
            _path_params['designId'] = design_id
        if comment_id is not None:
            _path_params['commentId'] = comment_id
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'oauthAuthCode'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1/designs/{designId}/comments/{commentId}',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            host__=host__,
            request_auth__=request_auth__
        )


