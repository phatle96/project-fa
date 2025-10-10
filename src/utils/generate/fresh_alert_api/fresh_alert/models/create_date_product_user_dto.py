import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDateProductUserDto")


@_attrs_define
class CreateDateProductUserDto:
    """
    Attributes:
        product_id (str): Product ID (UUID)
        date_manufactured (Union[Unset, datetime.datetime]):
        date_best_before (Union[Unset, datetime.datetime]):
        date_expired (Union[Unset, datetime.datetime]):
        quantity (Union[Unset, float]):  Default: 1.0.
    """

    product_id: str
    date_manufactured: Union[Unset, datetime.datetime] = UNSET
    date_best_before: Union[Unset, datetime.datetime] = UNSET
    date_expired: Union[Unset, datetime.datetime] = UNSET
    quantity: Union[Unset, float] = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        product_id = self.product_id

        date_manufactured: Union[Unset, str] = UNSET
        if not isinstance(self.date_manufactured, Unset):
            date_manufactured = self.date_manufactured.isoformat()

        date_best_before: Union[Unset, str] = UNSET
        if not isinstance(self.date_best_before, Unset):
            date_best_before = self.date_best_before.isoformat()

        date_expired: Union[Unset, str] = UNSET
        if not isinstance(self.date_expired, Unset):
            date_expired = self.date_expired.isoformat()

        quantity = self.quantity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "productId": product_id,
            }
        )
        if date_manufactured is not UNSET:
            field_dict["dateManufactured"] = date_manufactured
        if date_best_before is not UNSET:
            field_dict["dateBestBefore"] = date_best_before
        if date_expired is not UNSET:
            field_dict["dateExpired"] = date_expired
        if quantity is not UNSET:
            field_dict["quantity"] = quantity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        product_id = d.pop("productId")

        _date_manufactured = d.pop("dateManufactured", UNSET)
        date_manufactured: Union[Unset, datetime.datetime]
        if isinstance(_date_manufactured, Unset):
            date_manufactured = UNSET
        else:
            date_manufactured = isoparse(_date_manufactured)

        _date_best_before = d.pop("dateBestBefore", UNSET)
        date_best_before: Union[Unset, datetime.datetime]
        if isinstance(_date_best_before, Unset):
            date_best_before = UNSET
        else:
            date_best_before = isoparse(_date_best_before)

        _date_expired = d.pop("dateExpired", UNSET)
        date_expired: Union[Unset, datetime.datetime]
        if isinstance(_date_expired, Unset):
            date_expired = UNSET
        else:
            date_expired = isoparse(_date_expired)

        quantity = d.pop("quantity", UNSET)

        create_date_product_user_dto = cls(
            product_id=product_id,
            date_manufactured=date_manufactured,
            date_best_before=date_best_before,
            date_expired=date_expired,
            quantity=quantity,
        )

        create_date_product_user_dto.additional_properties = d
        return create_date_product_user_dto

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
