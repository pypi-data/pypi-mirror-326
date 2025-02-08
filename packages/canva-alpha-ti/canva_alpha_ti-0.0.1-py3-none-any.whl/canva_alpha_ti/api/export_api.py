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
from typing import Optional
from typing_extensions import Annotated
from canva_alpha_ti.models.create_design_export_job_request import CreateDesignExportJobRequest
from canva_alpha_ti.models.create_design_export_job_response import CreateDesignExportJobResponse
from canva_alpha_ti.models.get_design_export_job_response import GetDesignExportJobResponse

from canva_alpha_ti.api_client import ApiClient, RequestSerialized
from canva_alpha_ti.api_response import ApiResponse
from canva_alpha_ti.rest import RESTResponseType


class ExportApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def create_design_export_job(
        self,
        create_design_export_job_request: Optional[CreateDesignExportJobRequest] = None,
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
    ) -> CreateDesignExportJobResponse:
        """create_design_export_job

        Starts a new [asynchronous job](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints) to export a file from Canva. Once the exported file is generated, you can download it using the link(s) provided.  The request requires the design ID and the exported file format type.  Supported file formats (and export file type values): PDF (`pdf`), JPG (`jpg`), PNG (`png`), GIF (`gif`), Microsoft PowerPoint (`pptx`), and MP4 (`mp4`).  <Note>  For more information on the workflow for using asynchronous jobs, see [API requests and responses](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints). You can check the status and get the results of export jobs created with this API using the [Get design export job API](https://www.canva.dev/docs/connect/api-reference/exports/get-design-export-job/).  </Note>

        :param create_design_export_job_request:
        :type create_design_export_job_request: CreateDesignExportJobRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_design_export_job_serialize(
            create_design_export_job_request=create_design_export_job_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateDesignExportJobResponse",
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
    def create_design_export_job_with_http_info(
        self,
        create_design_export_job_request: Optional[CreateDesignExportJobRequest] = None,
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
    ) -> ApiResponse[CreateDesignExportJobResponse]:
        """create_design_export_job

        Starts a new [asynchronous job](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints) to export a file from Canva. Once the exported file is generated, you can download it using the link(s) provided.  The request requires the design ID and the exported file format type.  Supported file formats (and export file type values): PDF (`pdf`), JPG (`jpg`), PNG (`png`), GIF (`gif`), Microsoft PowerPoint (`pptx`), and MP4 (`mp4`).  <Note>  For more information on the workflow for using asynchronous jobs, see [API requests and responses](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints). You can check the status and get the results of export jobs created with this API using the [Get design export job API](https://www.canva.dev/docs/connect/api-reference/exports/get-design-export-job/).  </Note>

        :param create_design_export_job_request:
        :type create_design_export_job_request: CreateDesignExportJobRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_design_export_job_serialize(
            create_design_export_job_request=create_design_export_job_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateDesignExportJobResponse",
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
    def create_design_export_job_without_preload_content(
        self,
        create_design_export_job_request: Optional[CreateDesignExportJobRequest] = None,
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
        """create_design_export_job

        Starts a new [asynchronous job](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints) to export a file from Canva. Once the exported file is generated, you can download it using the link(s) provided.  The request requires the design ID and the exported file format type.  Supported file formats (and export file type values): PDF (`pdf`), JPG (`jpg`), PNG (`png`), GIF (`gif`), Microsoft PowerPoint (`pptx`), and MP4 (`mp4`).  <Note>  For more information on the workflow for using asynchronous jobs, see [API requests and responses](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints). You can check the status and get the results of export jobs created with this API using the [Get design export job API](https://www.canva.dev/docs/connect/api-reference/exports/get-design-export-job/).  </Note>

        :param create_design_export_job_request:
        :type create_design_export_job_request: CreateDesignExportJobRequest
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_design_export_job_serialize(
            create_design_export_job_request=create_design_export_job_request,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateDesignExportJobResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _create_design_export_job_serialize(
        self,
        create_design_export_job_request,
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
        if create_design_export_job_request is not None:
            _body_params = create_design_export_job_request


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
            resource_path='/v1/exports',
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
    def get_design_export_job(
        self,
        export_id: Annotated[str, Field(strict=True, description="The export job ID.")],
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
    ) -> GetDesignExportJobResponse:
        """get_design_export_job

        Gets the result of a design export job that was created using the [Create design export job API](https://www.canva.dev/docs/connect/api-reference/exports/create-design-export-job/).  If the job is successful, the response includes an array of download links for each page of the design.  You might need to make multiple requests to this endpoint until you get a `success` or `failed` status. For more information on the workflow for using asynchronous jobs, see [API requests and responses](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints).

        :param export_id: The export job ID. (required)
        :type export_id: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_design_export_job_serialize(
            export_id=export_id,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetDesignExportJobResponse",
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
    def get_design_export_job_with_http_info(
        self,
        export_id: Annotated[str, Field(strict=True, description="The export job ID.")],
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
    ) -> ApiResponse[GetDesignExportJobResponse]:
        """get_design_export_job

        Gets the result of a design export job that was created using the [Create design export job API](https://www.canva.dev/docs/connect/api-reference/exports/create-design-export-job/).  If the job is successful, the response includes an array of download links for each page of the design.  You might need to make multiple requests to this endpoint until you get a `success` or `failed` status. For more information on the workflow for using asynchronous jobs, see [API requests and responses](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints).

        :param export_id: The export job ID. (required)
        :type export_id: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_design_export_job_serialize(
            export_id=export_id,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetDesignExportJobResponse",
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
    def get_design_export_job_without_preload_content(
        self,
        export_id: Annotated[str, Field(strict=True, description="The export job ID.")],
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
        """get_design_export_job

        Gets the result of a design export job that was created using the [Create design export job API](https://www.canva.dev/docs/connect/api-reference/exports/create-design-export-job/).  If the job is successful, the response includes an array of download links for each page of the design.  You might need to make multiple requests to this endpoint until you get a `success` or `failed` status. For more information on the workflow for using asynchronous jobs, see [API requests and responses](https://www.canva.dev/docs/connect/api-requests-responses/#asynchronous-job-endpoints).

        :param export_id: The export job ID. (required)
        :type export_id: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_design_export_job_serialize(
            export_id=export_id,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetDesignExportJobResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _get_design_export_job_serialize(
        self,
        export_id,
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
        if export_id is not None:
            _path_params['exportId'] = export_id
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
            resource_path='/v1/exports/{exportId}',
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


