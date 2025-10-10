from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.date_controller_calculate_quantity_body import DateControllerCalculateQuantityBody
from ...models.date_controller_calculate_quantity_response_200 import DateControllerCalculateQuantityResponse200
from ...types import Response


def _get_kwargs(
    date_id: str,
    *,
    body: DateControllerCalculateQuantityBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/date/calculate-quantity/{date_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DateControllerCalculateQuantityResponse200]]:
    if response.status_code == 200:
        response_200 = DateControllerCalculateQuantityResponse200.from_dict(response.json())

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
) -> Response[Union[Any, DateControllerCalculateQuantityResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    date_id: str,
    *,
    client: AuthenticatedClient,
    body: DateControllerCalculateQuantityBody,
) -> Response[Union[Any, DateControllerCalculateQuantityResponse200]]:
    """Calculate quantity

    Args:
        date_id (str):
        body (DateControllerCalculateQuantityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DateControllerCalculateQuantityResponse200]]
    """

    kwargs = _get_kwargs(
        date_id=date_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    date_id: str,
    *,
    client: AuthenticatedClient,
    body: DateControllerCalculateQuantityBody,
) -> Optional[Union[Any, DateControllerCalculateQuantityResponse200]]:
    """Calculate quantity

    Args:
        date_id (str):
        body (DateControllerCalculateQuantityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DateControllerCalculateQuantityResponse200]
    """

    return sync_detailed(
        date_id=date_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    date_id: str,
    *,
    client: AuthenticatedClient,
    body: DateControllerCalculateQuantityBody,
) -> Response[Union[Any, DateControllerCalculateQuantityResponse200]]:
    """Calculate quantity

    Args:
        date_id (str):
        body (DateControllerCalculateQuantityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DateControllerCalculateQuantityResponse200]]
    """

    kwargs = _get_kwargs(
        date_id=date_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    date_id: str,
    *,
    client: AuthenticatedClient,
    body: DateControllerCalculateQuantityBody,
) -> Optional[Union[Any, DateControllerCalculateQuantityResponse200]]:
    """Calculate quantity

    Args:
        date_id (str):
        body (DateControllerCalculateQuantityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DateControllerCalculateQuantityResponse200]
    """

    return (
        await asyncio_detailed(
            date_id=date_id,
            client=client,
            body=body,
        )
    ).parsed
