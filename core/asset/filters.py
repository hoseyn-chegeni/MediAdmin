from django_filters import FilterSet
from .models import Consumable, ConsumableCategory


class ConsumableFilter(FilterSet):

    class Meta:
        model = Consumable
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }

class ConsumableCategoryFilter(FilterSet):

    class Meta:
        model = ConsumableCategory
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }
