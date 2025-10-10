from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_foods_search_data_type_item import GetFoodsSearchDataTypeItem
from ...models.get_foods_search_sort_by import GetFoodsSearchSortBy
from ...models.get_foods_search_sort_order import GetFoodsSearchSortOrder
from ...models.search_result_dto import SearchResultDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    query: str,
    data_type: Union[Unset, list[GetFoodsSearchDataTypeItem]] = UNSET,
    page_size: Union[Unset, float] = 50.0,
    page_number: Union[Unset, float] = 1.0,
    sort_by: Union[Unset, GetFoodsSearchSortBy] = UNSET,
    sort_order: Union[Unset, GetFoodsSearchSortOrder] = UNSET,
    brand_owner: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["query"] = query

    json_data_type: Union[Unset, list[str]] = UNSET
    if not isinstance(data_type, Unset):
        json_data_type = []
        for data_type_item_data in data_type:
            data_type_item = data_type_item_data.value
            json_data_type.append(data_type_item)

    params["dataType"] = json_data_type

    params["pageSize"] = page_size

    params["pageNumber"] = page_number

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    json_sort_order: Union[Unset, str] = UNSET
    if not isinstance(sort_order, Unset):
        json_sort_order = sort_order.value

    params["sortOrder"] = json_sort_order

    params["brandOwner"] = brand_owner

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/food-data-central/v1/foods/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, SearchResultDto]]:
    if response.status_code == 200:
        response_200 = SearchResultDto.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, SearchResultDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: str,
    data_type: Union[Unset, list[GetFoodsSearchDataTypeItem]] = UNSET,
    page_size: Union[Unset, float] = 50.0,
    page_number: Union[Unset, float] = 1.0,
    sort_by: Union[Unset, GetFoodsSearchSortBy] = UNSET,
    sort_order: Union[Unset, GetFoodsSearchSortOrder] = UNSET,
    brand_owner: Union[Unset, str] = UNSET,
) -> Response[Union[Any, SearchResultDto]]:
    """Returns a list of foods that matched search (query) keywords

     Search for foods using keywords. Results can be filtered by dataType and there are options for
    result page sizes or sorting.

    Args:
        query (str):  Example: cheddar cheese.
        data_type (Union[Unset, list[GetFoodsSearchDataTypeItem]]):  Example: ['Foundation', 'SR
            Legacy'].
        page_size (Union[Unset, float]):  Default: 50.0. Example: 25.
        page_number (Union[Unset, float]):  Default: 1.0. Example: 2.
        sort_by (Union[Unset, GetFoodsSearchSortBy]):  Example: dataType.keyword.
        sort_order (Union[Unset, GetFoodsSearchSortOrder]):  Example: asc.
        brand_owner (Union[Unset, str]):  Example: Kar Nut Products Company.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResultDto]]
    """

    kwargs = _get_kwargs(
        query=query,
        data_type=data_type,
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
        sort_order=sort_order,
        brand_owner=brand_owner,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    query: str,
    data_type: Union[Unset, list[GetFoodsSearchDataTypeItem]] = UNSET,
    page_size: Union[Unset, float] = 50.0,
    page_number: Union[Unset, float] = 1.0,
    sort_by: Union[Unset, GetFoodsSearchSortBy] = UNSET,
    sort_order: Union[Unset, GetFoodsSearchSortOrder] = UNSET,
    brand_owner: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, SearchResultDto]]:
    """Returns a list of foods that matched search (query) keywords

     Search for foods using keywords. Results can be filtered by dataType and there are options for
    result page sizes or sorting.

    Args:
        query (str):  Example: cheddar cheese.
        data_type (Union[Unset, list[GetFoodsSearchDataTypeItem]]):  Example: ['Foundation', 'SR
            Legacy'].
        page_size (Union[Unset, float]):  Default: 50.0. Example: 25.
        page_number (Union[Unset, float]):  Default: 1.0. Example: 2.
        sort_by (Union[Unset, GetFoodsSearchSortBy]):  Example: dataType.keyword.
        sort_order (Union[Unset, GetFoodsSearchSortOrder]):  Example: asc.
        brand_owner (Union[Unset, str]):  Example: Kar Nut Products Company.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchResultDto]
    """

    return sync_detailed(
        client=client,
        query=query,
        data_type=data_type,
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
        sort_order=sort_order,
        brand_owner=brand_owner,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: str,
    data_type: Union[Unset, list[GetFoodsSearchDataTypeItem]] = UNSET,
    page_size: Union[Unset, float] = 50.0,
    page_number: Union[Unset, float] = 1.0,
    sort_by: Union[Unset, GetFoodsSearchSortBy] = UNSET,
    sort_order: Union[Unset, GetFoodsSearchSortOrder] = UNSET,
    brand_owner: Union[Unset, str] = UNSET,
) -> Response[Union[Any, SearchResultDto]]:
    """Returns a list of foods that matched search (query) keywords

     Search for foods using keywords. Results can be filtered by dataType and there are options for
    result page sizes or sorting.

    Args:
        query (str):  Example: cheddar cheese.
        data_type (Union[Unset, list[GetFoodsSearchDataTypeItem]]):  Example: ['Foundation', 'SR
            Legacy'].
        page_size (Union[Unset, float]):  Default: 50.0. Example: 25.
        page_number (Union[Unset, float]):  Default: 1.0. Example: 2.
        sort_by (Union[Unset, GetFoodsSearchSortBy]):  Example: dataType.keyword.
        sort_order (Union[Unset, GetFoodsSearchSortOrder]):  Example: asc.
        brand_owner (Union[Unset, str]):  Example: Kar Nut Products Company.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResultDto]]
    """

    kwargs = _get_kwargs(
        query=query,
        data_type=data_type,
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
        sort_order=sort_order,
        brand_owner=brand_owner,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    query: str,
    data_type: Union[Unset, list[GetFoodsSearchDataTypeItem]] = UNSET,
    page_size: Union[Unset, float] = 50.0,
    page_number: Union[Unset, float] = 1.0,
    sort_by: Union[Unset, GetFoodsSearchSortBy] = UNSET,
    sort_order: Union[Unset, GetFoodsSearchSortOrder] = UNSET,
    brand_owner: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, SearchResultDto]]:
    """Returns a list of foods that matched search (query) keywords

     Search for foods using keywords. Results can be filtered by dataType and there are options for
    result page sizes or sorting.

    Args:
        query (str):  Example: cheddar cheese.
        data_type (Union[Unset, list[GetFoodsSearchDataTypeItem]]):  Example: ['Foundation', 'SR
            Legacy'].
        page_size (Union[Unset, float]):  Default: 50.0. Example: 25.
        page_number (Union[Unset, float]):  Default: 1.0. Example: 2.
        sort_by (Union[Unset, GetFoodsSearchSortBy]):  Example: dataType.keyword.
        sort_order (Union[Unset, GetFoodsSearchSortOrder]):  Example: asc.
        brand_owner (Union[Unset, str]):  Example: Kar Nut Products Company.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchResultDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            data_type=data_type,
            page_size=page_size,
            page_number=page_number,
            sort_by=sort_by,
            sort_order=sort_order,
            brand_owner=brand_owner,
        )
    ).parsed
