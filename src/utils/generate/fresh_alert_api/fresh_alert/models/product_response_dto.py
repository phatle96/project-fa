from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.date_response_model import DateResponseModel


T = TypeVar("T", bound="ProductResponseDto")


@_attrs_define
class ProductResponseDto:
    """
    Attributes:
        id (str):
        code_number (Union[None, str]):
        code_type (Union[None, str]):
        product_name (Union[None, str]):
        brand (Union[None, str]):
        manufacturer (Union[None, str]):
        description (Union[None, str]):
        image_url (Union[None, list[str]]):
        usage_instruction (Union[None, str]):
        storage_instruction (Union[None, str]):
        country_of_origin (Union[None, str]):
        category (Union[None, str]):
        nutrition_fact (Union[None, str]):
        label_key (Union[None, str]):
        phrase (Union[None, str]):
        date_product_users (Union[None, list['DateResponseModel']]):
    """

    id: str
    code_number: Union[None, str]
    code_type: Union[None, str]
    product_name: Union[None, str]
    brand: Union[None, str]
    manufacturer: Union[None, str]
    description: Union[None, str]
    image_url: Union[None, list[str]]
    usage_instruction: Union[None, str]
    storage_instruction: Union[None, str]
    country_of_origin: Union[None, str]
    category: Union[None, str]
    nutrition_fact: Union[None, str]
    label_key: Union[None, str]
    phrase: Union[None, str]
    date_product_users: Union[None, list["DateResponseModel"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        code_number: Union[None, str]
        code_number = self.code_number

        code_type: Union[None, str]
        code_type = self.code_type

        product_name: Union[None, str]
        product_name = self.product_name

        brand: Union[None, str]
        brand = self.brand

        manufacturer: Union[None, str]
        manufacturer = self.manufacturer

        description: Union[None, str]
        description = self.description

        image_url: Union[None, list[str]]
        if isinstance(self.image_url, list):
            image_url = self.image_url

        else:
            image_url = self.image_url

        usage_instruction: Union[None, str]
        usage_instruction = self.usage_instruction

        storage_instruction: Union[None, str]
        storage_instruction = self.storage_instruction

        country_of_origin: Union[None, str]
        country_of_origin = self.country_of_origin

        category: Union[None, str]
        category = self.category

        nutrition_fact: Union[None, str]
        nutrition_fact = self.nutrition_fact

        label_key: Union[None, str]
        label_key = self.label_key

        phrase: Union[None, str]
        phrase = self.phrase

        date_product_users: Union[None, list[dict[str, Any]]]
        if isinstance(self.date_product_users, list):
            date_product_users = []
            for date_product_users_type_0_item_data in self.date_product_users:
                date_product_users_type_0_item = date_product_users_type_0_item_data.to_dict()
                date_product_users.append(date_product_users_type_0_item)

        else:
            date_product_users = self.date_product_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "codeNumber": code_number,
                "codeType": code_type,
                "productName": product_name,
                "brand": brand,
                "manufacturer": manufacturer,
                "description": description,
                "imageUrl": image_url,
                "usageInstruction": usage_instruction,
                "storageInstruction": storage_instruction,
                "countryOfOrigin": country_of_origin,
                "category": category,
                "nutritionFact": nutrition_fact,
                "labelKey": label_key,
                "phrase": phrase,
                "dateProductUsers": date_product_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.date_response_model import DateResponseModel

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_code_number(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        code_number = _parse_code_number(d.pop("codeNumber"))

        def _parse_code_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        code_type = _parse_code_type(d.pop("codeType"))

        def _parse_product_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        product_name = _parse_product_name(d.pop("productName"))

        def _parse_brand(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        brand = _parse_brand(d.pop("brand"))

        def _parse_manufacturer(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        manufacturer = _parse_manufacturer(d.pop("manufacturer"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        def _parse_image_url(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                image_url_type_0 = cast(list[str], data)

                return image_url_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        image_url = _parse_image_url(d.pop("imageUrl"))

        def _parse_usage_instruction(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        usage_instruction = _parse_usage_instruction(d.pop("usageInstruction"))

        def _parse_storage_instruction(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        storage_instruction = _parse_storage_instruction(d.pop("storageInstruction"))

        def _parse_country_of_origin(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        country_of_origin = _parse_country_of_origin(d.pop("countryOfOrigin"))

        def _parse_category(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category = _parse_category(d.pop("category"))

        def _parse_nutrition_fact(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        nutrition_fact = _parse_nutrition_fact(d.pop("nutritionFact"))

        def _parse_label_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        label_key = _parse_label_key(d.pop("labelKey"))

        def _parse_phrase(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        phrase = _parse_phrase(d.pop("phrase"))

        def _parse_date_product_users(data: object) -> Union[None, list["DateResponseModel"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                date_product_users_type_0 = []
                _date_product_users_type_0 = data
                for date_product_users_type_0_item_data in _date_product_users_type_0:
                    date_product_users_type_0_item = DateResponseModel.from_dict(date_product_users_type_0_item_data)

                    date_product_users_type_0.append(date_product_users_type_0_item)

                return date_product_users_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["DateResponseModel"]], data)

        date_product_users = _parse_date_product_users(d.pop("dateProductUsers"))

        product_response_dto = cls(
            id=id,
            code_number=code_number,
            code_type=code_type,
            product_name=product_name,
            brand=brand,
            manufacturer=manufacturer,
            description=description,
            image_url=image_url,
            usage_instruction=usage_instruction,
            storage_instruction=storage_instruction,
            country_of_origin=country_of_origin,
            category=category,
            nutrition_fact=nutrition_fact,
            label_key=label_key,
            phrase=phrase,
            date_product_users=date_product_users,
        )

        product_response_dto.additional_properties = d
        return product_response_dto

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
