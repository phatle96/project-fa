from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DateControllerCalculateQuantityBody")


@_attrs_define
class DateControllerCalculateQuantityBody:
    """
    Attributes:
        calculus (Union[Unset, str]):
    """

    calculus: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        calculus = self.calculus

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if calculus is not UNSET:
            field_dict["calculus"] = calculus

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        calculus = d.pop("calculus", UNSET)

        date_controller_calculate_quantity_body = cls(
            calculus=calculus,
        )

        date_controller_calculate_quantity_body.additional_properties = d
        return date_controller_calculate_quantity_body

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
