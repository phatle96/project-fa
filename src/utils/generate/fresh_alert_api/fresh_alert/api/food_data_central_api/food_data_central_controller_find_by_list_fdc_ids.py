from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.food_data_central_controller_find_by_list_fdc_ids_format import (
    FoodDataCentralControllerFindByListFdcIdsFormat,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    fdc_ids: list[str],
    format_: Union[Unset, FoodDataCentralControllerFindByListFdcIdsFormat] = UNSET,
    nutrients: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_fdc_ids = fdc_ids

    params["fdcIds"] = json_fdc_ids

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    json_nutrients: Union[Unset, list[str]] = UNSET
    if not isinstance(nutrients, Unset):
        json_nutrients = nutrients

    params["nutrients"] = json_nutrients

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/food-data-central/v1/foods",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 404:
        return None

    if response.status_code == 429:
        return None

    if response.status_code == 500:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    fdc_ids: list[str],
    format_: Union[Unset, FoodDataCentralControllerFindByListFdcIdsFormat] = UNSET,
    nutrients: Union[Unset, list[str]] = UNSET,
) -> Response[Any]:
    """Get information from the food data by List FdcId

    Args:
        fdc_ids (list[str]):
        format_ (Union[Unset, FoodDataCentralControllerFindByListFdcIdsFormat]):
        nutrients (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        fdc_ids=fdc_ids,
        format_=format_,
        nutrients=nutrients,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    fdc_ids: list[str],
    format_: Union[Unset, FoodDataCentralControllerFindByListFdcIdsFormat] = UNSET,
    nutrients: Union[Unset, list[str]] = UNSET,
) -> Response[Any]:
    """Get information from the food data by List FdcId

    Args:
        fdc_ids (list[str]):
        format_ (Union[Unset, FoodDataCentralControllerFindByListFdcIdsFormat]):
        nutrients (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        fdc_ids=fdc_ids,
        format_=format_,
        nutrients=nutrients,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
