from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.abridged_food_nutrient_dto import AbridgedFoodNutrientDto


T = TypeVar("T", bound="SearchResultFoodDto")


@_attrs_define
class SearchResultFoodDto:
    """
    Attributes:
        fdc_id (float): Unique ID of the food. Example: 45001529.
        description (str): The description of the food. Example: BROCCOLI.
        data_type (Union[Unset, str]): The type of the food data. Example: Branded.
        food_code (Union[Unset, str]): Any A unique ID identifying the food within FNDDS.
        food_nutrients (Union[Unset, list['AbridgedFoodNutrientDto']]): List of nutrients for the food.
        publication_date (Union[Unset, str]): Date the item was published to FDC. Example: 4/1/2019.
        scientific_name (Union[Unset, str]): The scientific name of the food.
        brand_owner (Union[Unset, str]): Brand owner for the food. Only applies to Branded Foods. Example: Supervalu,
            Inc..
        gtin_upc (Union[Unset, str]): GTIN or UPC code identifying the food. Only applies to Branded Foods. Example:
            041303020937.
        ingredients (Union[Unset, str]): The list of ingredients (as it appears on the product label). Only applies to
            Branded Foods.
        ndb_number (Union[Unset, float]): Unique number assigned for foundation foods. Only applies to Foundation and
            SRLegacy Foods.
        additional_descriptions (Union[Unset, str]): Any additional descriptions of the food. Example: Coon; sharp
            cheese; Tillamook; Hoop; Pioneer; New York; Wisconsin; Longhorn.
        all_highlight_fields (Union[Unset, str]): allHighlightFields
        score (Union[Unset, float]): Relative score indicating how well the food matches the search criteria.
    """

    fdc_id: float
    description: str
    data_type: Union[Unset, str] = UNSET
    food_code: Union[Unset, str] = UNSET
    food_nutrients: Union[Unset, list["AbridgedFoodNutrientDto"]] = UNSET
    publication_date: Union[Unset, str] = UNSET
    scientific_name: Union[Unset, str] = UNSET
    brand_owner: Union[Unset, str] = UNSET
    gtin_upc: Union[Unset, str] = UNSET
    ingredients: Union[Unset, str] = UNSET
    ndb_number: Union[Unset, float] = UNSET
    additional_descriptions: Union[Unset, str] = UNSET
    all_highlight_fields: Union[Unset, str] = UNSET
    score: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fdc_id = self.fdc_id

        description = self.description

        data_type = self.data_type

        food_code = self.food_code

        food_nutrients: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.food_nutrients, Unset):
            food_nutrients = []
            for food_nutrients_item_data in self.food_nutrients:
                food_nutrients_item = food_nutrients_item_data.to_dict()
                food_nutrients.append(food_nutrients_item)

        publication_date = self.publication_date

        scientific_name = self.scientific_name

        brand_owner = self.brand_owner

        gtin_upc = self.gtin_upc

        ingredients = self.ingredients

        ndb_number = self.ndb_number

        additional_descriptions = self.additional_descriptions

        all_highlight_fields = self.all_highlight_fields

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fdcId": fdc_id,
                "description": description,
            }
        )
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if food_code is not UNSET:
            field_dict["foodCode"] = food_code
        if food_nutrients is not UNSET:
            field_dict["foodNutrients"] = food_nutrients
        if publication_date is not UNSET:
            field_dict["publicationDate"] = publication_date
        if scientific_name is not UNSET:
            field_dict["scientificName"] = scientific_name
        if brand_owner is not UNSET:
            field_dict["brandOwner"] = brand_owner
        if gtin_upc is not UNSET:
            field_dict["gtinUpc"] = gtin_upc
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients
        if ndb_number is not UNSET:
            field_dict["ndbNumber"] = ndb_number
        if additional_descriptions is not UNSET:
            field_dict["additionalDescriptions"] = additional_descriptions
        if all_highlight_fields is not UNSET:
            field_dict["allHighlightFields"] = all_highlight_fields
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.abridged_food_nutrient_dto import AbridgedFoodNutrientDto

        d = dict(src_dict)
        fdc_id = d.pop("fdcId")

        description = d.pop("description")

        data_type = d.pop("dataType", UNSET)

        food_code = d.pop("foodCode", UNSET)

        food_nutrients = []
        _food_nutrients = d.pop("foodNutrients", UNSET)
        for food_nutrients_item_data in _food_nutrients or []:
            food_nutrients_item = AbridgedFoodNutrientDto.from_dict(food_nutrients_item_data)

            food_nutrients.append(food_nutrients_item)

        publication_date = d.pop("publicationDate", UNSET)

        scientific_name = d.pop("scientificName", UNSET)

        brand_owner = d.pop("brandOwner", UNSET)

        gtin_upc = d.pop("gtinUpc", UNSET)

        ingredients = d.pop("ingredients", UNSET)

        ndb_number = d.pop("ndbNumber", UNSET)

        additional_descriptions = d.pop("additionalDescriptions", UNSET)

        all_highlight_fields = d.pop("allHighlightFields", UNSET)

        score = d.pop("score", UNSET)

        search_result_food_dto = cls(
            fdc_id=fdc_id,
            description=description,
            data_type=data_type,
            food_code=food_code,
            food_nutrients=food_nutrients,
            publication_date=publication_date,
            scientific_name=scientific_name,
            brand_owner=brand_owner,
            gtin_upc=gtin_upc,
            ingredients=ingredients,
            ndb_number=ndb_number,
            additional_descriptions=additional_descriptions,
            all_highlight_fields=all_highlight_fields,
            score=score,
        )

        search_result_food_dto.additional_properties = d
        return search_result_food_dto

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
