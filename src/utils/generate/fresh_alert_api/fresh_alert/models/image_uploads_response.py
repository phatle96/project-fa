from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ImageUploadsResponse")


@_attrs_define
class ImageUploadsResponse:
    """
    Attributes:
        id (str):
        success (bool):
        image_path (Union[None, str]):
        message (Union[None, str]):
        product_id (Union[None, str]):
    """

    id: str
    success: bool
    image_path: Union[None, str]
    message: Union[None, str]
    product_id: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        success = self.success

        image_path: Union[None, str]
        image_path = self.image_path

        message: Union[None, str]
        message = self.message

        product_id: Union[None, str]
        product_id = self.product_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "success": success,
                "imagePath": image_path,
                "message": message,
                "productId": product_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        success = d.pop("success")

        def _parse_image_path(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image_path = _parse_image_path(d.pop("imagePath"))

        def _parse_message(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        message = _parse_message(d.pop("message"))

        def _parse_product_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        product_id = _parse_product_id(d.pop("productId"))

        image_uploads_response = cls(
            id=id,
            success=success,
            image_path=image_path,
            message=message,
            product_id=product_id,
        )

        image_uploads_response.additional_properties = d
        return image_uploads_response

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
