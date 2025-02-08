# coding: utf-8

"""
    Notion API

    Hello and welcome!  To make use of this API collection collection as it's written, please duplicate [this database template](https://www.notion.so/8e2c2b769e1d47d287b9ed3035d607ae?v=dc1b92875fb94f10834ba8d36549bd2a).  ﻿Under the `Variables` tab, add your environment variables to start making requests. You will need to [create an integration](https://www.notion.so/my-integrations) to retrieve an API token. You will also need additional values, such as a database ID and page ID, which can be found in your Notion workspace or from the database template mentioned above.  For our full documentation, including sample integrations and guides, visit [developers.notion.com](https://developers.notion.com/)﻿.  Please note: Pages that are parented by a database _must_ have the same properties as the parent database. If you are not using the database template provided, the request `body` for the page endpoints included in this collection should be updated to match the properties in the parent database being used. See documentation for [Creating a page](https://developers.notion.com/reference/post-page) for more information.  To learn more about creating an access token, see our [official documentation](https://developers.notion.com/reference/create-a-token) and read our [Authorization](https://developers.notion.com/docs/authorization#step-3-send-the-code-in-a-post-request-to-the-notion-api) guide.  Need more help? Join our [developer community on Slack](https://join.slack.com/t/notiondevs/shared_invite/zt-20b5996xv-DzJdLiympy6jP0GGzu3AMg)﻿.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import StrictStr
from typing import Any, Dict, Optional

from notion_beta_ti.api_client import ApiClient, RequestSerialized
from notion_beta_ti.api_response import ApiResponse
from notion_beta_ti.rest import RESTResponseType


class UsersApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def v1_users_get(
        self,
        notion_version: Optional[StrictStr] = None,
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
    ) -> object:
        """List all users

        Returns a paginated list of user objects for a workspace

        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_get_serialize(
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
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
    def v1_users_get_with_http_info(
        self,
        notion_version: Optional[StrictStr] = None,
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
    ) -> ApiResponse[object]:
        """List all users

        Returns a paginated list of user objects for a workspace

        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_get_serialize(
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
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
    def v1_users_get_without_preload_content(
        self,
        notion_version: Optional[StrictStr] = None,
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
        """List all users

        Returns a paginated list of user objects for a workspace

        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_get_serialize(
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _v1_users_get_serialize(
        self,
        notion_version,
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
        if notion_version is not None:
            _header_params['Notion-Version'] = notion_version
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
            'bearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1/users',
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
    def v1_users_id_get(
        self,
        id: StrictStr,
        notion_version: Optional[StrictStr] = None,
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
    ) -> object:
        """Retrieve a user

        Retrieve a user object using the ID specified in the request path.

        :param id: (required)
        :type id: str
        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_id_get_serialize(
            id=id,
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
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
    def v1_users_id_get_with_http_info(
        self,
        id: StrictStr,
        notion_version: Optional[StrictStr] = None,
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
    ) -> ApiResponse[object]:
        """Retrieve a user

        Retrieve a user object using the ID specified in the request path.

        :param id: (required)
        :type id: str
        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_id_get_serialize(
            id=id,
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
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
    def v1_users_id_get_without_preload_content(
        self,
        id: StrictStr,
        notion_version: Optional[StrictStr] = None,
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
        """Retrieve a user

        Retrieve a user object using the ID specified in the request path.

        :param id: (required)
        :type id: str
        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_id_get_serialize(
            id=id,
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _v1_users_id_get_serialize(
        self,
        id,
        notion_version,
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
        if id is not None:
            _path_params['id'] = id
        # process the query parameters
        # process the header parameters
        if notion_version is not None:
            _header_params['Notion-Version'] = notion_version
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
            'bearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1/users/{id}',
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
    def v1_users_me_get(
        self,
        notion_version: Optional[StrictStr] = None,
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
    ) -> object:
        """Retrieve your token’s bot user


        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_me_get_serialize(
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
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
    def v1_users_me_get_with_http_info(
        self,
        notion_version: Optional[StrictStr] = None,
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
    ) -> ApiResponse[object]:
        """Retrieve your token’s bot user


        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_me_get_serialize(
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
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
    def v1_users_me_get_without_preload_content(
        self,
        notion_version: Optional[StrictStr] = None,
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
        """Retrieve your token’s bot user


        :param notion_version:
        :type notion_version: str
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._v1_users_me_get_serialize(
            notion_version=notion_version,
            request_auth__=request_auth__,
            content_type__=content_type__,
            headers__=headers__,
            host__=host__
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
        }
        response_data = self.api_client.call_api(
            *_param,
            request_timeout__=request_timeout__
        )
        return response_data.response


    def _v1_users_me_get_serialize(
        self,
        notion_version,
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
        if notion_version is not None:
            _header_params['Notion-Version'] = notion_version
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
            'bearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1/users/me',
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


