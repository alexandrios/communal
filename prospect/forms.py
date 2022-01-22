from datetime import datetime, date
from django import forms
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import DateInput, modelform_factory, SelectDateWidget, NumberInput
from .models import Counters, Tariffs


class CountersForm(forms.ModelForm):
    # input_formats=settings.DATE_INPUT_FORMATS
    month = forms.IntegerField(label='Месяц', initial=date.today().month,
                               max_value=12, min_value=1,
                               validators=[MaxValueValidator(12), MinValueValidator(1)])
    year = forms.IntegerField(label='Год', initial=date.today().year,
                              max_value=2100, min_value=2000,
                              validators=[MaxValueValidator(2100), MinValueValidator(2000)])
    date_get = forms.DateField(label='Дата снятия показаний',
                               widget=DateInput(attrs={'type': 'date'}),
                               initial=datetime.today(), localize=True)
    notes = forms.CharField(label='Примечание', required=False,
                            widget=forms.widgets.Textarea(attrs={'rows': 3}))
    cw_kitchen = forms.IntegerField(label='Холодная вода: Кухня', initial=0)
    #cw_bathroom = forms.IntegerField(initial=0)

    # date_get = forms.DateField(label='Дата снятия показаний',
    #                            widget=SelectDateWidget(empty_label=('Год', "Месяц", "Число")), localize=True)

    class Meta:
        model = Counters
        fields = '__all__'
        # labels = {'cw_bathroom': 'Холодная вода: Серебряный'}


class TariffsForm(forms.ModelForm):
    date_start = forms.DateField(label='Начало действия тарифа',
                                 widget=DateInput(attrs={'type': 'date'}),
                                 initial=date(datetime.today().year, datetime.today().month, 1), localize=True)
    water_supply = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.00,
                                      label='Водоснабжение')
    water_drainage = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.00,
                                        label='Водоотведение')
    heating_water = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.00,
                                       label='Подогрев воды')
    el_day = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.00,
                                label='Электричество: день')
    el_night = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.00,
                                  label='Электричество: ночь')

    class Meta:
        model = Tariffs
        fields = ('date_start', 'water_supply', 'water_drainage', 'heating_water', 'el_day', 'el_night')

    def clean_water_supply(self):
        val = self.cleaned_data['water_supply']
        if val > 100:
            raise ValidationError('Слишком высокий тариф для водоснабжения!')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if self.cleaned_data['water_drainage'] > 100:
            errors['water_drainage'] = ValidationError('Слишком высокий тариф для водоотведения!')
        if errors:
            raise ValidationError(errors)
