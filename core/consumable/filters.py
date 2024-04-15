from .models import ConsumableCategory, ConsumableV2,  Supplier
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


class SupplierFilter(BaseFilter):

    class Meta:
        model = Supplier
        fields = {
            "id": ["exact"],
            "name": ["exact"],
            "contact_person": ["exact"],
            "email": ["exact"],
            "phone_number": ["exact"],
            "city": ["exact", "icontains"],
        }