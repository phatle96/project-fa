from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.product_response_dto import ProductResponseDto


T = TypeVar("T", bound="ProductControllerFindAllResponse200")


@_attrs_define
class ProductControllerFindAllResponse200:
    """
    Attributes:
        res (float):  Example: 1.
        error (Union[None, Unset, str]):
        error_code (Union[None, Unset, str]):
        access_token (Union[None, Unset, str]):
        data (Union[Unset, list['ProductResponseDto']]):
    """

    res: float
    error: Union[None, Unset, str] = UNSET
    error_code: Union[None, Unset, str] = UNSET
    access_token: Union[None, Unset, str] = UNSET
    data: Union[Unset, list["ProductResponseDto"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        res = self.res

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        error_code: Union[None, Unset, str]
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        access_token: Union[None, Unset, str]
        if isinstance(self.access_token, Unset):
            access_token = UNSET
        else:
            access_token = self.access_token

        data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "res": res,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if access_token is not UNSET:
            field_dict["accessToken"] = access_token
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product_response_dto import ProductResponseDto

        d = dict(src_dict)
        res = d.pop("res")

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_error_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_code = _parse_error_code(d.pop("errorCode", UNSET))

        def _parse_access_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        access_token = _parse_access_token(d.pop("accessToken", UNSET))

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = ProductResponseDto.from_dict(data_item_data)

            data.append(data_item)

        product_controller_find_all_response_200 = cls(
            res=res,
            error=error,
            error_code=error_code,
            access_token=access_token,
            data=data,
        )

        product_controller_find_all_response_200.additional_properties = d
        return product_controller_find_all_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
