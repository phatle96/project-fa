import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="IngredientDto")


@_attrs_define
class IngredientDto:
    """
    Attributes:
        id (Union[None, str]):
        off_id (Union[None, str]):
        name (Union[None, str]):
        description (Union[None, str]):
        origin_country (Union[None, str]):
        is_allergen (Union[None, bool]):
        date_created (Union[None, datetime.datetime]):
    """

    id: Union[None, str]
    off_id: Union[None, str]
    name: Union[None, str]
    description: Union[None, str]
    origin_country: Union[None, str]
    is_allergen: Union[None, bool]
    date_created: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[None, str]
        id = self.id

        off_id: Union[None, str]
        off_id = self.off_id

        name: Union[None, str]
        name = self.name

        description: Union[None, str]
        description = self.description

        origin_country: Union[None, str]
        origin_country = self.origin_country

        is_allergen: Union[None, bool]
        is_allergen = self.is_allergen

        date_created: Union[None, str]
        if isinstance(self.date_created, datetime.datetime):
            date_created = self.date_created.isoformat()
        else:
            date_created = self.date_created

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "offId": off_id,
                "name": name,
                "description": description,
                "originCountry": origin_country,
                "isAllergen": is_allergen,
                "dateCreated": date_created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        id = _parse_id(d.pop("id"))

        def _parse_off_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        off_id = _parse_off_id(d.pop("offId"))

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        def _parse_origin_country(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        origin_country = _parse_origin_country(d.pop("originCountry"))

        def _parse_is_allergen(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        is_allergen = _parse_is_allergen(d.pop("isAllergen"))

        def _parse_date_created(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_created_type_0 = isoparse(data)

                return date_created_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        date_created = _parse_date_created(d.pop("dateCreated"))

        ingredient_dto = cls(
            id=id,
            off_id=off_id,
            name=name,
            description=description,
            origin_country=origin_country,
            is_allergen=is_allergen,
            date_created=date_created,
        )

        ingredient_dto.additional_properties = d
        return ingredient_dto

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
