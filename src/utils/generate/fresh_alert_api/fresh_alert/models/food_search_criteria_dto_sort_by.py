from enum import Enum


class FoodSearchCriteriaDtoSortBy(str, Enum):
    DATATYPE_KEYWORD = "dataType.keyword"
    FDCID = "fdcId"
    LOWERCASEDESCRIPTION_KEYWORD = "lowercaseDescription.keyword"
    PUBLISHEDDATE = "publishedDate"

    def __str__(self) -> str:
        return str(self.value)
