from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.product_controller_find_all_by_user_lookback_days_response_200 import (
    ProductControllerFindAllByUserLookbackDaysResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    days: Union[Unset, float] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["days"] = days

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/product/user/expired",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]:
    if response.status_code == 200:
        response_200 = ProductControllerFindAllByUserLookbackDaysResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, float] = UNSET,
) -> Response[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]:
    """Get Product list by user with lookback day

    Args:
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]
    """

    kwargs = _get_kwargs(
        days=days,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, float] = UNSET,
) -> Optional[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]:
    """Get Product list by user with lookback day

    Args:
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]
    """

    return sync_detailed(
        client=client,
        days=days,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, float] = UNSET,
) -> Response[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]:
    """Get Product list by user with lookback day

    Args:
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]
    """

    kwargs = _get_kwargs(
        days=days,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, float] = UNSET,
) -> Optional[Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]]:
    """Get Product list by user with lookback day

    Args:
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProductControllerFindAllByUserLookbackDaysResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            days=days,
        )
    ).parsed
