from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from .models import DigitalItem, PhysicalItem


class DigitalItemCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Фотокарточка')

    class Meta:
        model = DigitalItem
        fields = ('image', 'name', 'price', 'promo_codes')
        labels = {
            'name': 'Наименование',
            'price': 'Стоимость',
            'promo_codes': 'Список промокодов'
        }
        help_texts = {
            'name': 'Название будущего товара',
            'price': 'Стоимость в коинах',
            'promo_codes': 'Промокоды',
        }

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Сохранить', css_class='btn-primary'))
    helper.form_method = 'POST'


class PhysicalItemCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Фотокарточка')

    class Meta:
        model = PhysicalItem
        fields = ('image', 'name', 'price', 'count', 'is_infinity')
        labels = {
            'name': 'Наименование',
            'price': 'Стоимость',
            'count': 'Количество',
            'is_infinity': 'Бесконечность - не предел'
        }
        help_texts = {
            'name': 'Название будущего товара',
            'price': 'Стоимость в коинах',
            'count': 'Сколько всего товара',
        }

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Сохранить', css_class='btn-primary'))
    helper.form_method = 'POST'
