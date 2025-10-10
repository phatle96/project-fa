from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.food_search_criteria_dto import FoodSearchCriteriaDto
    from ..models.search_result_food_dto import SearchResultFoodDto


T = TypeVar("T", bound="SearchResultDto")


@_attrs_define
class SearchResultDto:
    """
    Attributes:
        food_search_criteria (FoodSearchCriteriaDto):
        total_hits (float): The total number of foods found matching the search criteria. Example: 1034.
        current_page (float): The current page of results being returned. Example: 1.
        total_pages (float): The total number of pages found matching the search criteria. Example: 21.
        foods (list['SearchResultFoodDto']): The list of foods found matching the search criteria.
    """

    food_search_criteria: "FoodSearchCriteriaDto"
    total_hits: float
    current_page: float
    total_pages: float
    foods: list["SearchResultFoodDto"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        food_search_criteria = self.food_search_criteria.to_dict()

        total_hits = self.total_hits

        current_page = self.current_page

        total_pages = self.total_pages

        foods = []
        for foods_item_data in self.foods:
            foods_item = foods_item_data.to_dict()
            foods.append(foods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "foodSearchCriteria": food_search_criteria,
                "totalHits": total_hits,
                "currentPage": current_page,
                "totalPages": total_pages,
                "foods": foods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.food_search_criteria_dto import FoodSearchCriteriaDto
        from ..models.search_result_food_dto import SearchResultFoodDto

        d = dict(src_dict)
        food_search_criteria = FoodSearchCriteriaDto.from_dict(d.pop("foodSearchCriteria"))

        total_hits = d.pop("totalHits")

        current_page = d.pop("currentPage")

        total_pages = d.pop("totalPages")

        foods = []
        _foods = d.pop("foods")
        for foods_item_data in _foods:
            foods_item = SearchResultFoodDto.from_dict(foods_item_data)

            foods.append(foods_item)

        search_result_dto = cls(
            food_search_criteria=food_search_criteria,
            total_hits=total_hits,
            current_page=current_page,
            total_pages=total_pages,
            foods=foods,
        )

        search_result_dto.additional_properties = d
        return search_result_dto

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
