from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.barcode_controller_find_barcode_by_off_response_200 import BarcodeControllerFindBarcodeByOffResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    code: str,
    *,
    code_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["codeType"] = code_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/product-code/{code}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]:
    if response.status_code == 200:
        response_200 = BarcodeControllerFindBarcodeByOffResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    code: str,
    *,
    client: AuthenticatedClient,
    code_type: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]:
    """Get product by Barcode

    Args:
        code (str):
        code_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]
    """

    kwargs = _get_kwargs(
        code=code,
        code_type=code_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    code: str,
    *,
    client: AuthenticatedClient,
    code_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]:
    """Get product by Barcode

    Args:
        code (str):
        code_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BarcodeControllerFindBarcodeByOffResponse200]
    """

    return sync_detailed(
        code=code,
        client=client,
        code_type=code_type,
    ).parsed


async def asyncio_detailed(
    code: str,
    *,
    client: AuthenticatedClient,
    code_type: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]:
    """Get product by Barcode

    Args:
        code (str):
        code_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]
    """

    kwargs = _get_kwargs(
        code=code,
        code_type=code_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    code: str,
    *,
    client: AuthenticatedClient,
    code_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BarcodeControllerFindBarcodeByOffResponse200]]:
    """Get product by Barcode

    Args:
        code (str):
        code_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BarcodeControllerFindBarcodeByOffResponse200]
    """

    return (
        await asyncio_detailed(
            code=code,
            client=client,
            code_type=code_type,
        )
    ).parsed
