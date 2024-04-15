from django_filters import FilterSet
from .models import ConsumableCategory, ConsumableV2
from  base.filters import BaseFilter

class ConsumableFilter(BaseFilter):

    class Meta:
        model = ConsumableV2
        fields = {
            "id": ["exact"],
            "name": ["exact"],
            "category": ["exact"],
            # "supplier": ["exact"],
        }

class ConsumableCategoryFilter(BaseFilter):

    class Meta:
        model = ConsumableCategory
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }
