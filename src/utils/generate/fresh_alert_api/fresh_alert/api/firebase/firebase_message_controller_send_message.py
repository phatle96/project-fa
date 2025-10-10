from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_model import ResponseModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    code: Union[Unset, float] = UNSET,
    days: Union[Unset, float] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["code"] = code

    params["days"] = days

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/firebase-messages/private/CloudMessaging",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseModel]]:
    if response.status_code == 201:
        response_201 = ResponseModel.from_dict(response.json())

        return response_201

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
) -> Response[Union[Any, ResponseModel]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, float] = UNSET,
    days: Union[Unset, float] = UNSET,
) -> Response[Union[Any, ResponseModel]]:
    """Send message user with code = 1: toOne, code = 2: ToMany, code = 3: ToAll (default), This api just
    use for BACK-END, for get access token of api Firebase

    Args:
        code (Union[Unset, float]):
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseModel]]
    """

    kwargs = _get_kwargs(
        code=code,
        days=days,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, float] = UNSET,
    days: Union[Unset, float] = UNSET,
) -> Optional[Union[Any, ResponseModel]]:
    """Send message user with code = 1: toOne, code = 2: ToMany, code = 3: ToAll (default), This api just
    use for BACK-END, for get access token of api Firebase

    Args:
        code (Union[Unset, float]):
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseModel]
    """

    return sync_detailed(
        client=client,
        code=code,
        days=days,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, float] = UNSET,
    days: Union[Unset, float] = UNSET,
) -> Response[Union[Any, ResponseModel]]:
    """Send message user with code = 1: toOne, code = 2: ToMany, code = 3: ToAll (default), This api just
    use for BACK-END, for get access token of api Firebase

    Args:
        code (Union[Unset, float]):
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseModel]]
    """

    kwargs = _get_kwargs(
        code=code,
        days=days,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, float] = UNSET,
    days: Union[Unset, float] = UNSET,
) -> Optional[Union[Any, ResponseModel]]:
    """Send message user with code = 1: toOne, code = 2: ToMany, code = 3: ToAll (default), This api just
    use for BACK-END, for get access token of api Firebase

    Args:
        code (Union[Unset, float]):
        days (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseModel]
    """

    return (
        await asyncio_detailed(
            client=client,
            code=code,
            days=days,
        )
    ).parsed
