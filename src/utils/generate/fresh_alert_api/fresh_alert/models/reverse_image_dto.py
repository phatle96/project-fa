from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reverse_image_dto_image_sizes_item import ReverseImageDtoImageSizesItem
    from ..models.reverse_image_dto_search_metadata import ReverseImageDtoSearchMetadata
    from ..models.reverse_image_dto_search_parameters import ReverseImageDtoSearchParameters
    from ..models.reverse_image_element_result import ReverseImageElementResult


T = TypeVar("T", bound="ReverseImageDto")


@_attrs_define
class ReverseImageDto:
    """
    Attributes:
        search_metadata (Union[Unset, ReverseImageDtoSearchMetadata]):
        search_parameters (Union[Unset, ReverseImageDtoSearchParameters]):
        image_sizes (Union[Unset, list['ReverseImageDtoImageSizesItem']]):
        image_results (Union[Unset, list['ReverseImageElementResult']]):
        visual_matches (Union[Unset, list['ReverseImageElementResult']]):
        related_content (Union[Unset, list['ReverseImageElementResult']]):
    """

    search_metadata: Union[Unset, "ReverseImageDtoSearchMetadata"] = UNSET
    search_parameters: Union[Unset, "ReverseImageDtoSearchParameters"] = UNSET
    image_sizes: Union[Unset, list["ReverseImageDtoImageSizesItem"]] = UNSET
    image_results: Union[Unset, list["ReverseImageElementResult"]] = UNSET
    visual_matches: Union[Unset, list["ReverseImageElementResult"]] = UNSET
    related_content: Union[Unset, list["ReverseImageElementResult"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        search_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.search_metadata, Unset):
            search_metadata = self.search_metadata.to_dict()

        search_parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.search_parameters, Unset):
            search_parameters = self.search_parameters.to_dict()

        image_sizes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.image_sizes, Unset):
            image_sizes = []
            for image_sizes_item_data in self.image_sizes:
                image_sizes_item = image_sizes_item_data.to_dict()
                image_sizes.append(image_sizes_item)

        image_results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.image_results, Unset):
            image_results = []
            for image_results_item_data in self.image_results:
                image_results_item = image_results_item_data.to_dict()
                image_results.append(image_results_item)

        visual_matches: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.visual_matches, Unset):
            visual_matches = []
            for visual_matches_item_data in self.visual_matches:
                visual_matches_item = visual_matches_item_data.to_dict()
                visual_matches.append(visual_matches_item)

        related_content: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.related_content, Unset):
            related_content = []
            for related_content_item_data in self.related_content:
                related_content_item = related_content_item_data.to_dict()
                related_content.append(related_content_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if search_metadata is not UNSET:
            field_dict["search_metadata"] = search_metadata
        if search_parameters is not UNSET:
            field_dict["search_parameters"] = search_parameters
        if image_sizes is not UNSET:
            field_dict["image_sizes"] = image_sizes
        if image_results is not UNSET:
            field_dict["image_results"] = image_results
        if visual_matches is not UNSET:
            field_dict["visual_matches"] = visual_matches
        if related_content is not UNSET:
            field_dict["related_content"] = related_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reverse_image_dto_image_sizes_item import ReverseImageDtoImageSizesItem
        from ..models.reverse_image_dto_search_metadata import ReverseImageDtoSearchMetadata
        from ..models.reverse_image_dto_search_parameters import ReverseImageDtoSearchParameters
        from ..models.reverse_image_element_result import ReverseImageElementResult

        d = dict(src_dict)
        _search_metadata = d.pop("search_metadata", UNSET)
        search_metadata: Union[Unset, ReverseImageDtoSearchMetadata]
        if isinstance(_search_metadata, Unset):
            search_metadata = UNSET
        else:
            search_metadata = ReverseImageDtoSearchMetadata.from_dict(_search_metadata)

        _search_parameters = d.pop("search_parameters", UNSET)
        search_parameters: Union[Unset, ReverseImageDtoSearchParameters]
        if isinstance(_search_parameters, Unset):
            search_parameters = UNSET
        else:
            search_parameters = ReverseImageDtoSearchParameters.from_dict(_search_parameters)

        image_sizes = []
        _image_sizes = d.pop("image_sizes", UNSET)
        for image_sizes_item_data in _image_sizes or []:
            image_sizes_item = ReverseImageDtoImageSizesItem.from_dict(image_sizes_item_data)

            image_sizes.append(image_sizes_item)

        image_results = []
        _image_results = d.pop("image_results", UNSET)
        for image_results_item_data in _image_results or []:
            image_results_item = ReverseImageElementResult.from_dict(image_results_item_data)

            image_results.append(image_results_item)

        visual_matches = []
        _visual_matches = d.pop("visual_matches", UNSET)
        for visual_matches_item_data in _visual_matches or []:
            visual_matches_item = ReverseImageElementResult.from_dict(visual_matches_item_data)

            visual_matches.append(visual_matches_item)

        related_content = []
        _related_content = d.pop("related_content", UNSET)
        for related_content_item_data in _related_content or []:
            related_content_item = ReverseImageElementResult.from_dict(related_content_item_data)

            related_content.append(related_content_item)

        reverse_image_dto = cls(
            search_metadata=search_metadata,
            search_parameters=search_parameters,
            image_sizes=image_sizes,
            image_results=image_results,
            visual_matches=visual_matches,
            related_content=related_content,
        )

        reverse_image_dto.additional_properties = d
        return reverse_image_dto

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
