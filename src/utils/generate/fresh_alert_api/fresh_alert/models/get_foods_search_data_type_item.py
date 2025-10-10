from enum import Enum


class GetFoodsSearchDataTypeItem(str, Enum):
    BRANDED = "Branded"
    FOUNDATION = "Foundation"
    SR_LEGACY = "SR Legacy"
    SURVEY_FNDDS = "Survey (FNDDS)"

    def __str__(self) -> str:
        return str(self.value)
