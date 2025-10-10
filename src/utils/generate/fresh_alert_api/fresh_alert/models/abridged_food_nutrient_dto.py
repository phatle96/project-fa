from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AbridgedFoodNutrientDto")


@_attrs_define
class AbridgedFoodNutrientDto:
    """
    Attributes:
        nutrient_id (float): The ID of the nutrient. Example: 1008.
        nutrient_name (str): The name of the nutrient. Example: Protein.
        unit_name (str): The unit of the nutrient measurement. Example: g.
        value (float): The value of the nutrient. Example: 25.
    """

    nutrient_id: float
    nutrient_name: str
    unit_name: str
    value: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nutrient_id = self.nutrient_id

        nutrient_name = self.nutrient_name

        unit_name = self.unit_name

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nutrientId": nutrient_id,
                "nutrientName": nutrient_name,
                "unitName": unit_name,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        nutrient_id = d.pop("nutrientId")

        nutrient_name = d.pop("nutrientName")

        unit_name = d.pop("unitName")

        value = d.pop("value")

        abridged_food_nutrient_dto = cls(
            nutrient_id=nutrient_id,
            nutrient_name=nutrient_name,
            unit_name=unit_name,
            value=value,
        )

        abridged_food_nutrient_dto.additional_properties = d
        return abridged_food_nutrient_dto

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
