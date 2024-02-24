from .forms import DigitalItemCreateForm, PhysicalItemCreateForm
from .models import DigitalItem, PhysicalItem, SaleItem


def get_form_by_item_id(item_id):
    item = DigitalItem.objects.filter(id=item_id).first()
    if item is None:
        item = PhysicalItem.objects.filter(id=item_id).first()
        form = {"form": PhysicalItemCreateForm(instance=item), "form_type": 0, 'item': item}
        return form
    else:
        item = DigitalItem.objects.filter(id=item_id).first()
        form = {"form": DigitalItemCreateForm(instance=item), "form_type": 1, 'item': item}
        return form
