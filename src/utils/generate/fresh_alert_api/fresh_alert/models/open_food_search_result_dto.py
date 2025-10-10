from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_food_product_summary_dto import OpenFoodProductSummaryDto


T = TypeVar("T", bound="OpenFoodSearchResultDto")


@_attrs_define
class OpenFoodSearchResultDto:
    """
    Attributes:
        products (list['OpenFoodProductSummaryDto']):
        count (Union[None, Unset, float]):
        page (Union[None, Unset, float]):
        page_count (Union[None, Unset, float]):
        page_size (Union[None, Unset, float]):
        skip (Union[None, Unset, float]):
    """

    products: list["OpenFoodProductSummaryDto"]
    count: Union[None, Unset, float] = UNSET
    page: Union[None, Unset, float] = UNSET
    page_count: Union[None, Unset, float] = UNSET
    page_size: Union[None, Unset, float] = UNSET
    skip: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        products = []
        for products_item_data in self.products:
            products_item = products_item_data.to_dict()
            products.append(products_item)

        count: Union[None, Unset, float]
        if isinstance(self.count, Unset):
            count = UNSET
        else:
            count = self.count

        page: Union[None, Unset, float]
        if isinstance(self.page, Unset):
            page = UNSET
        else:
            page = self.page

        page_count: Union[None, Unset, float]
        if isinstance(self.page_count, Unset):
            page_count = UNSET
        else:
            page_count = self.page_count

        page_size: Union[None, Unset, float]
        if isinstance(self.page_size, Unset):
            page_size = UNSET
        else:
            page_size = self.page_size

        skip: Union[None, Unset, float]
        if isinstance(self.skip, Unset):
            skip = UNSET
        else:
            skip = self.skip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "products": products,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if page is not UNSET:
            field_dict["page"] = page
        if page_count is not UNSET:
            field_dict["page_count"] = page_count
        if page_size is not UNSET:
            field_dict["page_size"] = page_size
        if skip is not UNSET:
            field_dict["skip"] = skip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_food_product_summary_dto import OpenFoodProductSummaryDto

        d = dict(src_dict)
        products = []
        _products = d.pop("products")
        for products_item_data in _products:
            products_item = OpenFoodProductSummaryDto.from_dict(products_item_data)

            products.append(products_item)

        def _parse_count(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        count = _parse_count(d.pop("count", UNSET))

        def _parse_page(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        page = _parse_page(d.pop("page", UNSET))

        def _parse_page_count(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        page_count = _parse_page_count(d.pop("page_count", UNSET))

        def _parse_page_size(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        page_size = _parse_page_size(d.pop("page_size", UNSET))

        def _parse_skip(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        skip = _parse_skip(d.pop("skip", UNSET))

        open_food_search_result_dto = cls(
            products=products,
            count=count,
            page=page,
            page_count=page_count,
            page_size=page_size,
            skip=skip,
        )

        open_food_search_result_dto.additional_properties = d
        return open_food_search_result_dto

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
