from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.food_search_criteria_dto_data_type_item import FoodSearchCriteriaDtoDataTypeItem
from ..models.food_search_criteria_dto_sort_by import FoodSearchCriteriaDtoSortBy
from ..models.food_search_criteria_dto_sort_order import FoodSearchCriteriaDtoSortOrder
from ..models.food_search_criteria_dto_trade_channel_item import FoodSearchCriteriaDtoTradeChannelItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="FoodSearchCriteriaDto")


@_attrs_define
class FoodSearchCriteriaDto:
    """
    Attributes:
        query (str): Search terms to use in the search. Example: Cheddar cheese.
        data_type (Union[Unset, list[FoodSearchCriteriaDtoDataTypeItem]]): Filter on a specific data type. Example:
            ['Foundation', 'SR Legacy'].
        page_size (Union[Unset, float]): Maximum number of results to return. Default is 50. Example: 25.
        page_number (Union[Unset, float]): Page number to retrieve. Example: 2.
        sort_by (Union[Unset, FoodSearchCriteriaDtoSortBy]): Field to sort the results by. Example:
            lowercaseDescription.keyword.
        sort_order (Union[Unset, FoodSearchCriteriaDtoSortOrder]): The sort direction for the results. Example: asc.
        brand_owner (Union[Unset, str]): Filter results based on the brand owner. Example: Kar Nut Products Company.
        trade_channel (Union[Unset, list[FoodSearchCriteriaDtoTradeChannelItem]]): Filter foods containing any of the
            specified trade channels. Example: ['CHILD_NUTRITION_FOOD_PROGRAMS', 'GROCERY'].
        start_date (Union[Unset, str]): Filter foods published on or after this date. Format: YYYY-MM-DD Example:
            2021-01-01.
        end_date (Union[Unset, str]): Filter foods published on or before this date. Format: YYYY-MM-DD Example:
            2021-12-30.
    """

    query: str
    data_type: Union[Unset, list[FoodSearchCriteriaDtoDataTypeItem]] = UNSET
    page_size: Union[Unset, float] = UNSET
    page_number: Union[Unset, float] = UNSET
    sort_by: Union[Unset, FoodSearchCriteriaDtoSortBy] = UNSET
    sort_order: Union[Unset, FoodSearchCriteriaDtoSortOrder] = UNSET
    brand_owner: Union[Unset, str] = UNSET
    trade_channel: Union[Unset, list[FoodSearchCriteriaDtoTradeChannelItem]] = UNSET
    start_date: Union[Unset, str] = UNSET
    end_date: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        data_type: Union[Unset, list[str]] = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = []
            for data_type_item_data in self.data_type:
                data_type_item = data_type_item_data.value
                data_type.append(data_type_item)

        page_size = self.page_size

        page_number = self.page_number

        sort_by: Union[Unset, str] = UNSET
        if not isinstance(self.sort_by, Unset):
            sort_by = self.sort_by.value

        sort_order: Union[Unset, str] = UNSET
        if not isinstance(self.sort_order, Unset):
            sort_order = self.sort_order.value

        brand_owner = self.brand_owner

        trade_channel: Union[Unset, list[str]] = UNSET
        if not isinstance(self.trade_channel, Unset):
            trade_channel = []
            for trade_channel_item_data in self.trade_channel:
                trade_channel_item = trade_channel_item_data.value
                trade_channel.append(trade_channel_item)

        start_date = self.start_date

        end_date = self.end_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size
        if page_number is not UNSET:
            field_dict["pageNumber"] = page_number
        if sort_by is not UNSET:
            field_dict["sortBy"] = sort_by
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order
        if brand_owner is not UNSET:
            field_dict["brandOwner"] = brand_owner
        if trade_channel is not UNSET:
            field_dict["tradeChannel"] = trade_channel
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        data_type = []
        _data_type = d.pop("dataType", UNSET)
        for data_type_item_data in _data_type or []:
            data_type_item = FoodSearchCriteriaDtoDataTypeItem(data_type_item_data)

            data_type.append(data_type_item)

        page_size = d.pop("pageSize", UNSET)

        page_number = d.pop("pageNumber", UNSET)

        _sort_by = d.pop("sortBy", UNSET)
        sort_by: Union[Unset, FoodSearchCriteriaDtoSortBy]
        if isinstance(_sort_by, Unset):
            sort_by = UNSET
        else:
            sort_by = FoodSearchCriteriaDtoSortBy(_sort_by)

        _sort_order = d.pop("sortOrder", UNSET)
        sort_order: Union[Unset, FoodSearchCriteriaDtoSortOrder]
        if isinstance(_sort_order, Unset):
            sort_order = UNSET
        else:
            sort_order = FoodSearchCriteriaDtoSortOrder(_sort_order)

        brand_owner = d.pop("brandOwner", UNSET)

        trade_channel = []
        _trade_channel = d.pop("tradeChannel", UNSET)
        for trade_channel_item_data in _trade_channel or []:
            trade_channel_item = FoodSearchCriteriaDtoTradeChannelItem(trade_channel_item_data)

            trade_channel.append(trade_channel_item)

        start_date = d.pop("startDate", UNSET)

        end_date = d.pop("endDate", UNSET)

        food_search_criteria_dto = cls(
            query=query,
            data_type=data_type,
            page_size=page_size,
            page_number=page_number,
            sort_by=sort_by,
            sort_order=sort_order,
            brand_owner=brand_owner,
            trade_channel=trade_channel,
            start_date=start_date,
            end_date=end_date,
        )

        food_search_criteria_dto.additional_properties = d
        return food_search_criteria_dto

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
