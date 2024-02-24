from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse

from .forms import DigitalItemCreateForm, PhysicalItemCreateForm
from .models import DigitalItem, PhysicalItem, SaleItem
from .tools import get_form_by_item_id


def index(request):
    for image in DigitalItem.objects.all():
        print('image', image.image)
    data = {'items': [*DigitalItem.objects.all(), *PhysicalItem.objects.all()]}
    return render(request, 'shop/shop.html', data)


def buy_item(request, item_id):
    print(item_id)
    data = {'item': SaleItem.objects.filter(id=item_id).first()}
    return render(request, 'shop/buy_item.html', data)


def items_view(request):
    data = {'items': [*DigitalItem.objects.all(), *PhysicalItem.objects.all()]}
    return render(request, 'shop/item_admin_view.html', data)


def digital_item_create(request):
    if request.method == "POST":
        digital_form = DigitalItemCreateForm(request.POST, request.FILES)
        digital_form.save()
        return HttpResponseRedirect(reverse('items_view'))
    else:
        digital_form = DigitalItemCreateForm()
        return render(request, 'shop/item_manager/digital_item_creation.html', {'form': digital_form})


def physical_item_create(request):
    if request.method == "POST":
        physical_form = PhysicalItemCreateForm(request.POST, request.FILES)
        if physical_form.is_valid():
            physical_form.save()
            return HttpResponseRedirect(reverse('items_view'))
    else:
        physical_form = PhysicalItemCreateForm()
        return render(request, 'shop/item_manager/physical_item_creation.html', {'form': physical_form})


def edit_item(request, item_id):
    form = get_form_by_item_id(item_id)

    if form.get('form_type') == 1:
        if request.method == 'GET':
            return render(request, 'shop/item_manager/digital_item_creation.html', {'form': form.get('form'), 'is_edit': 1, 'item': form.get('item')})
        if request.method == 'POST':
            item = form.get('item')
            if item is not None:
                form = DigitalItemCreateForm(request.POST, request.FILES, instance=form.get('item'))
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse('items_view'))
    else:
        if request.method == 'GET':
            return render(request, 'shop/item_manager/physical_item_creation.html', {'form': form.get('form'), 'is_edit': 1, 'item': form.get('item')})
        if request.method == 'POST':
            item = form.get('form_type')
            if item is not None:
                form = PhysicalItemCreateForm(request.POST, request.FILES, instance=form.get('item'))
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse('items_view'))


def delete_item(request, item_id):
    form = get_form_by_item_id(item_id)
    item = form.get('item')
    if item is not None:
        item.delete()
    return HttpResponseRedirect(reverse('items_view'))
