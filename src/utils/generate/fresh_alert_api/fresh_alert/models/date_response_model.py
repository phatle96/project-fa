import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DateResponseModel")


@_attrs_define
class DateResponseModel:
    """
    Attributes:
        id (str):
        product_id (Union[Unset, str]): Product ID (UUID)
        date_manufactured (Union[None, Unset, datetime.datetime]):
        date_best_before (Union[None, Unset, datetime.datetime]):
        date_expired (Union[None, Unset, datetime.datetime]):
        quantity (Union[None, Unset, float]):  Example: 5.
    """

    id: str
    product_id: Union[Unset, str] = UNSET
    date_manufactured: Union[None, Unset, datetime.datetime] = UNSET
    date_best_before: Union[None, Unset, datetime.datetime] = UNSET
    date_expired: Union[None, Unset, datetime.datetime] = UNSET
    quantity: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        product_id = self.product_id

        date_manufactured: Union[None, Unset, str]
        if isinstance(self.date_manufactured, Unset):
            date_manufactured = UNSET
        elif isinstance(self.date_manufactured, datetime.datetime):
            date_manufactured = self.date_manufactured.isoformat()
        else:
            date_manufactured = self.date_manufactured

        date_best_before: Union[None, Unset, str]
        if isinstance(self.date_best_before, Unset):
            date_best_before = UNSET
        elif isinstance(self.date_best_before, datetime.datetime):
            date_best_before = self.date_best_before.isoformat()
        else:
            date_best_before = self.date_best_before

        date_expired: Union[None, Unset, str]
        if isinstance(self.date_expired, Unset):
            date_expired = UNSET
        elif isinstance(self.date_expired, datetime.datetime):
            date_expired = self.date_expired.isoformat()
        else:
            date_expired = self.date_expired

        quantity: Union[None, Unset, float]
        if isinstance(self.quantity, Unset):
            quantity = UNSET
        else:
            quantity = self.quantity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if product_id is not UNSET:
            field_dict["productId"] = product_id
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
        id = d.pop("id")

        product_id = d.pop("productId", UNSET)

        def _parse_date_manufactured(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_manufactured_type_0 = isoparse(data)

                return date_manufactured_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        date_manufactured = _parse_date_manufactured(d.pop("dateManufactured", UNSET))

        def _parse_date_best_before(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_best_before_type_0 = isoparse(data)

                return date_best_before_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        date_best_before = _parse_date_best_before(d.pop("dateBestBefore", UNSET))

        def _parse_date_expired(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_expired_type_0 = isoparse(data)

                return date_expired_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        date_expired = _parse_date_expired(d.pop("dateExpired", UNSET))

        def _parse_quantity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        quantity = _parse_quantity(d.pop("quantity", UNSET))

        date_response_model = cls(
            id=id,
            product_id=product_id,
            date_manufactured=date_manufactured,
            date_best_before=date_best_before,
            date_expired=date_expired,
            quantity=quantity,
        )

        date_response_model.additional_properties = d
        return date_response_model

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
