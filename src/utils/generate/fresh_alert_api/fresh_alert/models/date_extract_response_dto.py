import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DateExtractResponseDto")


@_attrs_define
class DateExtractResponseDto:
    """
    Attributes:
        date_manufactured (Union[None, Unset, datetime.datetime]): Manufacture date
        date_expired (Union[None, Unset, datetime.datetime]): Manufacture date
        date_best_before (Union[None, Unset, datetime.datetime]): Manufacture date
    """

    date_manufactured: Union[None, Unset, datetime.datetime] = UNSET
    date_expired: Union[None, Unset, datetime.datetime] = UNSET
    date_best_before: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_manufactured: Union[None, Unset, str]
        if isinstance(self.date_manufactured, Unset):
            date_manufactured = UNSET
        elif isinstance(self.date_manufactured, datetime.datetime):
            date_manufactured = self.date_manufactured.isoformat()
        else:
            date_manufactured = self.date_manufactured

        date_expired: Union[None, Unset, str]
        if isinstance(self.date_expired, Unset):
            date_expired = UNSET
        elif isinstance(self.date_expired, datetime.datetime):
            date_expired = self.date_expired.isoformat()
        else:
            date_expired = self.date_expired

        date_best_before: Union[None, Unset, str]
        if isinstance(self.date_best_before, Unset):
            date_best_before = UNSET
        elif isinstance(self.date_best_before, datetime.datetime):
            date_best_before = self.date_best_before.isoformat()
        else:
            date_best_before = self.date_best_before

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date_manufactured is not UNSET:
            field_dict["dateManufactured"] = date_manufactured
        if date_expired is not UNSET:
            field_dict["dateExpired"] = date_expired
        if date_best_before is not UNSET:
            field_dict["dateBestBefore"] = date_best_before

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_date_manufactured(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_manufactured_type_0 = isoparse(data)

                return date_manufactured_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        date_manufactured = _parse_date_manufactured(d.pop("dateManufactured", UNSET))

        def _parse_date_expired(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_expired_type_0 = isoparse(data)

                return date_expired_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        date_expired = _parse_date_expired(d.pop("dateExpired", UNSET))

        def _parse_date_best_before(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_best_before_type_0 = isoparse(data)

                return date_best_before_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        date_best_before = _parse_date_best_before(d.pop("dateBestBefore", UNSET))

        date_extract_response_dto = cls(
            date_manufactured=date_manufactured,
            date_expired=date_expired,
            date_best_before=date_best_before,
        )

        date_extract_response_dto.additional_properties = d
        return date_extract_response_dto

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
