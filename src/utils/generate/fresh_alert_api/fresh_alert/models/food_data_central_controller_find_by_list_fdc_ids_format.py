from enum import Enum


class FoodDataCentralControllerFindByListFdcIdsFormat(str, Enum):
    ABRIDGED = "abridged"
    FULL = "full"

    def __str__(self) -> str:
        return str(self.value)
