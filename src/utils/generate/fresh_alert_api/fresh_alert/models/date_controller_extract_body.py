from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DateControllerExtractBody")


@_attrs_define
class DateControllerExtractBody:
    """
    Attributes:
        text_ocr (Union[Unset, str]):
        zone (Union[Unset, str]):
        country_code (Union[Unset, str]):
    """

    text_ocr: Union[Unset, str] = UNSET
    zone: Union[Unset, str] = UNSET
    country_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text_ocr = self.text_ocr

        zone = self.zone

        country_code = self.country_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text_ocr is not UNSET:
            field_dict["textOCR"] = text_ocr
        if zone is not UNSET:
            field_dict["zone"] = zone
        if country_code is not UNSET:
            field_dict["country_code"] = country_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text_ocr = d.pop("textOCR", UNSET)

        zone = d.pop("zone", UNSET)

        country_code = d.pop("country_code", UNSET)

        date_controller_extract_body = cls(
            text_ocr=text_ocr,
            zone=zone,
            country_code=country_code,
        )

        date_controller_extract_body.additional_properties = d
        return date_controller_extract_body

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
