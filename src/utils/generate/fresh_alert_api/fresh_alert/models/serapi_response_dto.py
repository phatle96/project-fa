from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_food_product_summary_dto import OpenFoodProductSummaryDto


T = TypeVar("T", bound="SerapiResponseDto")


@_attrs_define
class SerapiResponseDto:
    """
    Attributes:
        products (Union[None, list['OpenFoodProductSummaryDto']]):
        brand (Union[None, Unset, str]):
        product_name (Union[None, Unset, str]):
        brand_tags (Union[None, Unset, str]):
        search_terms (Union[None, Unset, str]):
        query_nl (Union[None, Unset, str]):
        count (Union[None, Unset, float]):
        page (Union[None, Unset, float]):
        page_count (Union[None, Unset, float]):
        page_size (Union[None, Unset, float]):
        skip (Union[None, Unset, float]):
    """

    products: Union[None, list["OpenFoodProductSummaryDto"]]
    brand: Union[None, Unset, str] = UNSET
    product_name: Union[None, Unset, str] = UNSET
    brand_tags: Union[None, Unset, str] = UNSET
    search_terms: Union[None, Unset, str] = UNSET
    query_nl: Union[None, Unset, str] = UNSET
    count: Union[None, Unset, float] = UNSET
    page: Union[None, Unset, float] = UNSET
    page_count: Union[None, Unset, float] = UNSET
    page_size: Union[None, Unset, float] = UNSET
    skip: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        products: Union[None, list[dict[str, Any]]]
        if isinstance(self.products, list):
            products = []
            for products_type_0_item_data in self.products:
                products_type_0_item = products_type_0_item_data.to_dict()
                products.append(products_type_0_item)

        else:
            products = self.products

        brand: Union[None, Unset, str]
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        product_name: Union[None, Unset, str]
        if isinstance(self.product_name, Unset):
            product_name = UNSET
        else:
            product_name = self.product_name

        brand_tags: Union[None, Unset, str]
        if isinstance(self.brand_tags, Unset):
            brand_tags = UNSET
        else:
            brand_tags = self.brand_tags

        search_terms: Union[None, Unset, str]
        if isinstance(self.search_terms, Unset):
            search_terms = UNSET
        else:
            search_terms = self.search_terms

        query_nl: Union[None, Unset, str]
        if isinstance(self.query_nl, Unset):
            query_nl = UNSET
        else:
            query_nl = self.query_nl

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
        if brand is not UNSET:
            field_dict["brand"] = brand
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if brand_tags is not UNSET:
            field_dict["brand_tags"] = brand_tags
        if search_terms is not UNSET:
            field_dict["search_terms"] = search_terms
        if query_nl is not UNSET:
            field_dict["query_nl"] = query_nl
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

        def _parse_products(data: object) -> Union[None, list["OpenFoodProductSummaryDto"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                products_type_0 = []
                _products_type_0 = data
                for products_type_0_item_data in _products_type_0:
                    products_type_0_item = OpenFoodProductSummaryDto.from_dict(products_type_0_item_data)

                    products_type_0.append(products_type_0_item)

                return products_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["OpenFoodProductSummaryDto"]], data)

        products = _parse_products(d.pop("products"))

        def _parse_brand(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        brand = _parse_brand(d.pop("brand", UNSET))

        def _parse_product_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        product_name = _parse_product_name(d.pop("productName", UNSET))

        def _parse_brand_tags(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        brand_tags = _parse_brand_tags(d.pop("brand_tags", UNSET))

        def _parse_search_terms(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        search_terms = _parse_search_terms(d.pop("search_terms", UNSET))

        def _parse_query_nl(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        query_nl = _parse_query_nl(d.pop("query_nl", UNSET))

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

        serapi_response_dto = cls(
            products=products,
            brand=brand,
            product_name=product_name,
            brand_tags=brand_tags,
            search_terms=search_terms,
            query_nl=query_nl,
            count=count,
            page=page,
            page_count=page_count,
            page_size=page_size,
            skip=skip,
        )

        serapi_response_dto.additional_properties = d
        return serapi_response_dto

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
