from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="KeyPhraseInputDto")


@_attrs_define
class KeyPhraseInputDto:
    """
    Attributes:
        key_label (str):
        phrase (str):
        country_code (str):
    """

    key_label: str
    phrase: str
    country_code: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key_label = self.key_label

        phrase = self.phrase

        country_code = self.country_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keyLabel": key_label,
                "phrase": phrase,
                "countryCode": country_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_label = d.pop("keyLabel")

        phrase = d.pop("phrase")

        country_code = d.pop("countryCode")

        key_phrase_input_dto = cls(
            key_label=key_label,
            phrase=phrase,
            country_code=country_code,
        )

        key_phrase_input_dto.additional_properties = d
        return key_phrase_input_dto

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
