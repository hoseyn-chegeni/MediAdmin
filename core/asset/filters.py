from django_filters import FilterSet
from .models import Consumable, ConsumableCategory, Supplier


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


class SupplierFilter(FilterSet):

    class Meta:
        model = Supplier
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }
