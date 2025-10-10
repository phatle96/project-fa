from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FirebaseUserModel")


@_attrs_define
class FirebaseUserModel:
    """
    Attributes:
        bearer_token (Union[None, str]):
        firebase_app_id (Union[None, str]):
        fcm_token (Union[None, str]):
    """

    bearer_token: Union[None, str]
    firebase_app_id: Union[None, str]
    fcm_token: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bearer_token: Union[None, str]
        bearer_token = self.bearer_token

        firebase_app_id: Union[None, str]
        firebase_app_id = self.firebase_app_id

        fcm_token: Union[None, str]
        fcm_token = self.fcm_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bearerToken": bearer_token,
                "firebaseAppId": firebase_app_id,
                "fcmToken": fcm_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_bearer_token(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        bearer_token = _parse_bearer_token(d.pop("bearerToken"))

        def _parse_firebase_app_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        firebase_app_id = _parse_firebase_app_id(d.pop("firebaseAppId"))

        def _parse_fcm_token(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        fcm_token = _parse_fcm_token(d.pop("fcmToken"))

        firebase_user_model = cls(
            bearer_token=bearer_token,
            firebase_app_id=firebase_app_id,
            fcm_token=fcm_token,
        )

        firebase_user_model.additional_properties = d
        return firebase_user_model

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
