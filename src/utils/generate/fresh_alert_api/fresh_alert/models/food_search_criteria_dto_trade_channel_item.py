from enum import Enum


class FoodSearchCriteriaDtoTradeChannelItem(str, Enum):
    CHILD_NUTRITION_FOOD_PROGRAMS = "CHILD_NUTRITION_FOOD_PROGRAMS"
    DRUG = "DRUG"
    FOOD_SERVICE = "FOOD_SERVICE"
    GROCERY = "GROCERY"
    MASS_MERCHANDISING = "MASS_MERCHANDISING"
    MILITARY = "MILITARY"
    ONLINE = "ONLINE"
    VENDING = "VENDING"

    def __str__(self) -> str:
        return str(self.value)
