from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.firebase_message_controller_migrate_current_user_response_200 import (
    FirebaseMessageControllerMigrateCurrentUserResponse200,
)
from ...models.firebase_user_input_model import FirebaseUserInputModel
from ...types import Response


def _get_kwargs(
    *,
    body: FirebaseUserInputModel,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/firebase-messages/private/user",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]:
    if response.status_code == 200:
        response_200 = FirebaseMessageControllerMigrateCurrentUserResponse200.from_dict(response.json())

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
) -> Response[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FirebaseUserInputModel,
) -> Response[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]:
    """Migrate current user

    Args:
        body (FirebaseUserInputModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: FirebaseUserInputModel,
) -> Optional[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]:
    """Migrate current user

    Args:
        body (FirebaseUserInputModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FirebaseUserInputModel,
) -> Response[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]:
    """Migrate current user

    Args:
        body (FirebaseUserInputModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FirebaseUserInputModel,
) -> Optional[Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]]:
    """Migrate current user

    Args:
        body (FirebaseUserInputModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, FirebaseMessageControllerMigrateCurrentUserResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
