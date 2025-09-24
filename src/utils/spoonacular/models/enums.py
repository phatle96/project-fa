"""
Enum definitions for Spoonacular API parameters.
"""

from enum import Enum


class SortDirection(str, Enum):
    """Sort direction options"""
    ASC = "asc"
    DESC = "desc"


class RecipeSortOption(str, Enum):
    """Recipe sorting options for complex search"""
    POPULARITY = "popularity"
    HEALTHINESS = "healthiness" 
    PRICE = "price"
    TIME = "time"
    RANDOM = "random"
    MAX_USED_INGREDIENTS = "max-used-ingredients"
    MIN_MISSING_INGREDIENTS = "min-missing-ingredients"


class Diet(str, Enum):
    """Diet types supported by Spoonacular"""
    GLUTEN_FREE = "gluten free"
    KETOGENIC = "ketogenic"
    VEGETARIAN = "vegetarian"
    LACTO_VEGETARIAN = "lacto-vegetarian"
    OVO_VEGETARIAN = "ovo-vegetarian"
    VEGAN = "vegan"
    PESCETARIAN = "pescetarian"
    PALEO = "paleo"
    PRIMAL = "primal"
    LOW_FODMAP = "low fodmap"
    WHOLE30 = "whole30"


class Intolerance(str, Enum):
    """Food intolerances supported by Spoonacular"""
    DAIRY = "dairy"
    EGG = "egg"
    GLUTEN = "gluten"
    GRAIN = "grain"
    PEANUT = "peanut"
    SEAFOOD = "seafood"
    SESAME = "sesame"
    SHELLFISH = "shellfish"
    SOY = "soy"
    SULFITE = "sulfite"
    TREE_NUT = "tree nut"
    WHEAT = "wheat"


class MealType(str, Enum):
    """Meal types for recipe classification"""
    MAIN_COURSE = "main course"
    SIDE_DISH = "side dish"
    DESSERT = "dessert"
    APPETIZER = "appetizer"
    SALAD = "salad"
    BREAD = "bread"
    BREAKFAST = "breakfast"
    SOUP = "soup"
    BEVERAGE = "beverage"
    SAUCE = "sauce"
    MARINADE = "marinade"
    FINGERFOOD = "fingerfood"
    SNACK = "snack"
    DRINK = "drink"


class Cuisine(str, Enum):
    """Cuisine types supported by Spoonacular"""
    AFRICAN = "african"
    AMERICAN = "american"
    BRITISH = "british"
    CAJUN = "cajun"
    CARIBBEAN = "caribbean"
    CHINESE = "chinese"
    EASTERN_EUROPEAN = "eastern european"
    EUROPEAN = "european"
    FRENCH = "french"
    GERMAN = "german"
    GREEK = "greek"
    INDIAN = "indian"
    IRISH = "irish"
    ITALIAN = "italian"
    JAPANESE = "japanese"
    JEWISH = "jewish"
    KOREAN = "korean"
    LATIN_AMERICAN = "latin american"
    MEDITERRANEAN = "mediterranean"
    MEXICAN = "mexican"
    MIDDLE_EASTERN = "middle eastern"
    NORDIC = "nordic"
    SOUTHERN = "southern"
    SPANISH = "spanish"
    THAI = "thai"
    VIETNAMESE = "vietnamese"


class EquipmentType(str, Enum):
    """Common cooking equipment types"""
    BLENDER = "blender"
    FOOD_PROCESSOR = "food processor"
    MIXER = "mixer"
    OVEN = "oven"
    STOVE = "stove"
    MICROWAVE = "microwave"
    GRILL = "grill"
    SLOW_COOKER = "slow cooker"
    PRESSURE_COOKER = "pressure cooker"
    STAND_MIXER = "stand mixer"
    IMMERSION_BLENDER = "immersion blender"


class DishType(str, Enum):
    """Dish type classifications"""
    MAIN_COURSE = "main course"
    SIDE_DISH = "side dish"
    DESSERT = "dessert"
    APPETIZER = "appetizer"
    SALAD = "salad"
    BREAD = "bread"
    BREAKFAST = "breakfast"
    SOUP = "soup"
    BEVERAGE = "beverage"
    SAUCE = "sauce"
    DRINK = "drink"