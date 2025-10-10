from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.price_dto import PriceDTO


T = TypeVar("T", bound="ReverseImageElementResult")


@_attrs_define
class ReverseImageElementResult:
    """
    Attributes:
        position (Union[None, float]):
        title (Union[None, str]):
        thumbnail (Union[None, str]):
        thumbnail_width (Union[None, float]):
        thumbnail_height (Union[None, float]):
        link (Union[None, str]):
        image (Union[None, str]):
        image_width (Union[None, float]):
        image_height (Union[None, float]):
        source (Union[None, str]):
        date (Union[None, str]):
        page_url (Union[None, str]):
        redirect_link (Union[None, str]):
        displayed_link (Union[None, str]):
        snippet (Union[None, str]):
        snippet_highlighted_words (Union[None, str]):
        favicon (Union[None, str]):
        source_icon (Union[None, str]):
        rating (Union[None, float]):
        reviews (Union[None, float]):
        in_stock (bool):  Default: True. Example: True.
        condition (Union[None, str]):
        price (Union[Unset, PriceDTO]):
    """

    position: Union[None, float]
    title: Union[None, str]
    thumbnail: Union[None, str]
    thumbnail_width: Union[None, float]
    thumbnail_height: Union[None, float]
    link: Union[None, str]
    image: Union[None, str]
    image_width: Union[None, float]
    image_height: Union[None, float]
    source: Union[None, str]
    date: Union[None, str]
    page_url: Union[None, str]
    redirect_link: Union[None, str]
    displayed_link: Union[None, str]
    snippet: Union[None, str]
    snippet_highlighted_words: Union[None, str]
    favicon: Union[None, str]
    source_icon: Union[None, str]
    rating: Union[None, float]
    reviews: Union[None, float]
    condition: Union[None, str]
    in_stock: bool = True
    price: Union[Unset, "PriceDTO"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        position: Union[None, float]
        position = self.position

        title: Union[None, str]
        title = self.title

        thumbnail: Union[None, str]
        thumbnail = self.thumbnail

        thumbnail_width: Union[None, float]
        thumbnail_width = self.thumbnail_width

        thumbnail_height: Union[None, float]
        thumbnail_height = self.thumbnail_height

        link: Union[None, str]
        link = self.link

        image: Union[None, str]
        image = self.image

        image_width: Union[None, float]
        image_width = self.image_width

        image_height: Union[None, float]
        image_height = self.image_height

        source: Union[None, str]
        source = self.source

        date: Union[None, str]
        date = self.date

        page_url: Union[None, str]
        page_url = self.page_url

        redirect_link: Union[None, str]
        redirect_link = self.redirect_link

        displayed_link: Union[None, str]
        displayed_link = self.displayed_link

        snippet: Union[None, str]
        snippet = self.snippet

        snippet_highlighted_words: Union[None, str]
        snippet_highlighted_words = self.snippet_highlighted_words

        favicon: Union[None, str]
        favicon = self.favicon

        source_icon: Union[None, str]
        source_icon = self.source_icon

        rating: Union[None, float]
        rating = self.rating

        reviews: Union[None, float]
        reviews = self.reviews

        in_stock = self.in_stock

        condition: Union[None, str]
        condition = self.condition

        price: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "position": position,
                "title": title,
                "thumbnail": thumbnail,
                "thumbnail_width": thumbnail_width,
                "thumbnail_height": thumbnail_height,
                "link": link,
                "image": image,
                "image_width": image_width,
                "image_height": image_height,
                "source": source,
                "date": date,
                "pageUrl": page_url,
                "redirect_link": redirect_link,
                "displayed_link": displayed_link,
                "snippet": snippet,
                "snippet_highlighted_words": snippet_highlighted_words,
                "favicon": favicon,
                "source_icon": source_icon,
                "rating": rating,
                "reviews": reviews,
                "in_stock": in_stock,
                "condition": condition,
            }
        )
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.price_dto import PriceDTO

        d = dict(src_dict)

        def _parse_position(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        position = _parse_position(d.pop("position"))

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        def _parse_thumbnail(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail"))

        def _parse_thumbnail_width(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        thumbnail_width = _parse_thumbnail_width(d.pop("thumbnail_width"))

        def _parse_thumbnail_height(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        thumbnail_height = _parse_thumbnail_height(d.pop("thumbnail_height"))

        def _parse_link(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        link = _parse_link(d.pop("link"))

        def _parse_image(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image = _parse_image(d.pop("image"))

        def _parse_image_width(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        image_width = _parse_image_width(d.pop("image_width"))

        def _parse_image_height(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        image_height = _parse_image_height(d.pop("image_height"))

        def _parse_source(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source = _parse_source(d.pop("source"))

        def _parse_date(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        date = _parse_date(d.pop("date"))

        def _parse_page_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        page_url = _parse_page_url(d.pop("pageUrl"))

        def _parse_redirect_link(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        redirect_link = _parse_redirect_link(d.pop("redirect_link"))

        def _parse_displayed_link(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        displayed_link = _parse_displayed_link(d.pop("displayed_link"))

        def _parse_snippet(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        snippet = _parse_snippet(d.pop("snippet"))

        def _parse_snippet_highlighted_words(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        snippet_highlighted_words = _parse_snippet_highlighted_words(d.pop("snippet_highlighted_words"))

        def _parse_favicon(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        favicon = _parse_favicon(d.pop("favicon"))

        def _parse_source_icon(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_icon = _parse_source_icon(d.pop("source_icon"))

        def _parse_rating(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        rating = _parse_rating(d.pop("rating"))

        def _parse_reviews(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        reviews = _parse_reviews(d.pop("reviews"))

        in_stock = d.pop("in_stock")

        def _parse_condition(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        condition = _parse_condition(d.pop("condition"))

        _price = d.pop("price", UNSET)
        price: Union[Unset, PriceDTO]
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = PriceDTO.from_dict(_price)

        reverse_image_element_result = cls(
            position=position,
            title=title,
            thumbnail=thumbnail,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
            link=link,
            image=image,
            image_width=image_width,
            image_height=image_height,
            source=source,
            date=date,
            page_url=page_url,
            redirect_link=redirect_link,
            displayed_link=displayed_link,
            snippet=snippet,
            snippet_highlighted_words=snippet_highlighted_words,
            favicon=favicon,
            source_icon=source_icon,
            rating=rating,
            reviews=reviews,
            in_stock=in_stock,
            condition=condition,
            price=price,
        )

        reverse_image_element_result.additional_properties = d
        return reverse_image_element_result

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
