from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_dto import IngredientDto


T = TypeVar("T", bound="CreateBarcodeInputDto")


@_attrs_define
class CreateBarcodeInputDto:
    """
    Attributes:
        code_number (str): Code number of the product
        code_type (Union[Unset, str]): Code type (optional)
        product_name (Union[Unset, str]): Product name (optional)
        brand (Union[Unset, str]):
        manufacturer (Union[Unset, str]):
        description (Union[Unset, str]):
        ingredients (Union[Unset, IngredientDto]):
        nutrition_fact (Union[Unset, str]):
        usage_instruction (Union[Unset, str]):
        storage_instruction (Union[Unset, str]):
        country_of_origin (Union[Unset, str]):
        category (Union[Unset, str]):
        label_key (Union[Unset, str]):
        phrase (Union[Unset, str]):
        image_url (Union[None, Unset, list[str]]):
    """

    code_number: str
    code_type: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    brand: Union[Unset, str] = UNSET
    manufacturer: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    ingredients: Union[Unset, "IngredientDto"] = UNSET
    nutrition_fact: Union[Unset, str] = UNSET
    usage_instruction: Union[Unset, str] = UNSET
    storage_instruction: Union[Unset, str] = UNSET
    country_of_origin: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    label_key: Union[Unset, str] = UNSET
    phrase: Union[Unset, str] = UNSET
    image_url: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code_number = self.code_number

        code_type = self.code_type

        product_name = self.product_name

        brand = self.brand

        manufacturer = self.manufacturer

        description = self.description

        ingredients: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.ingredients, Unset):
            ingredients = self.ingredients.to_dict()

        nutrition_fact = self.nutrition_fact

        usage_instruction = self.usage_instruction

        storage_instruction = self.storage_instruction

        country_of_origin = self.country_of_origin

        category = self.category

        label_key = self.label_key

        phrase = self.phrase

        image_url: Union[None, Unset, list[str]]
        if isinstance(self.image_url, Unset):
            image_url = UNSET
        elif isinstance(self.image_url, list):
            image_url = self.image_url

        else:
            image_url = self.image_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "codeNumber": code_number,
            }
        )
        if code_type is not UNSET:
            field_dict["codeType"] = code_type
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if brand is not UNSET:
            field_dict["brand"] = brand
        if manufacturer is not UNSET:
            field_dict["manufacturer"] = manufacturer
        if description is not UNSET:
            field_dict["description"] = description
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients
        if nutrition_fact is not UNSET:
            field_dict["nutritionFact"] = nutrition_fact
        if usage_instruction is not UNSET:
            field_dict["usageInstruction"] = usage_instruction
        if storage_instruction is not UNSET:
            field_dict["storageInstruction"] = storage_instruction
        if country_of_origin is not UNSET:
            field_dict["countryOfOrigin"] = country_of_origin
        if category is not UNSET:
            field_dict["category"] = category
        if label_key is not UNSET:
            field_dict["labelKey"] = label_key
        if phrase is not UNSET:
            field_dict["phrase"] = phrase
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_dto import IngredientDto

        d = dict(src_dict)
        code_number = d.pop("codeNumber")

        code_type = d.pop("codeType", UNSET)

        product_name = d.pop("productName", UNSET)

        brand = d.pop("brand", UNSET)

        manufacturer = d.pop("manufacturer", UNSET)

        description = d.pop("description", UNSET)

        _ingredients = d.pop("ingredients", UNSET)
        ingredients: Union[Unset, IngredientDto]
        if isinstance(_ingredients, Unset):
            ingredients = UNSET
        else:
            ingredients = IngredientDto.from_dict(_ingredients)

        nutrition_fact = d.pop("nutritionFact", UNSET)

        usage_instruction = d.pop("usageInstruction", UNSET)

        storage_instruction = d.pop("storageInstruction", UNSET)

        country_of_origin = d.pop("countryOfOrigin", UNSET)

        category = d.pop("category", UNSET)

        label_key = d.pop("labelKey", UNSET)

        phrase = d.pop("phrase", UNSET)

        def _parse_image_url(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                image_url_type_0 = cast(list[str], data)

                return image_url_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        image_url = _parse_image_url(d.pop("imageUrl", UNSET))

        create_barcode_input_dto = cls(
            code_number=code_number,
            code_type=code_type,
            product_name=product_name,
            brand=brand,
            manufacturer=manufacturer,
            description=description,
            ingredients=ingredients,
            nutrition_fact=nutrition_fact,
            usage_instruction=usage_instruction,
            storage_instruction=storage_instruction,
            country_of_origin=country_of_origin,
            category=category,
            label_key=label_key,
            phrase=phrase,
            image_url=image_url,
        )

        create_barcode_input_dto.additional_properties = d
        return create_barcode_input_dto

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
