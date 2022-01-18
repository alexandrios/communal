from datetime import datetime
from django import forms
from django.conf import settings
from django.forms import DateInput, modelform_factory, SelectDateWidget
from .models import Counters, Tariffs


class CountersForm(forms.ModelForm):
    # input_formats=settings.DATE_INPUT_FORMATS
    date_get = forms.DateField(label='Дата снятия показаний',
                               widget=DateInput(attrs={'type': 'date'}),
                               initial=datetime.today(), localize=True)
    notes = forms.CharField(label='Примечание', required=False,
                            widget=forms.widgets.Textarea(attrs={'rows': 3}))
    cw_kitchen = forms.IntegerField(label='Холодная вода: Кухня (234)')

    # date_get = forms.DateField(label='Дата снятия показаний',
    #                            widget=SelectDateWidget(empty_label=('Год', "Месяц", "Число")), localize=True)

    class Meta:
        model = Counters
        fields = ('date_get', 'month', 'year',
                  'cw_kitchen', 'cw_bathroom', 'hw_kitchen', 'hw_bathroom',
                  'el_1', 'el_2', 'notes')


class TariffsForm(forms.ModelForm):
    date_start = forms.DateField(label='Начало действия тарифа',
                                 widget=DateInput(attrs={'type': 'date'}),
                                 initial=datetime.today(), localize=True)
    water_supply = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.01,
                                      label='Водоснабжение')
    water_drainage = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, initial=0.01,
                                        label='Водоотведение')
    heating_water = forms.DecimalField(decimal_places=2, label='Подогрев воды')
    el_day = forms.DecimalField(decimal_places=2, label='Электричество: день')
    el_night = forms.DecimalField(decimal_places=2, label='Электричество: ночь')

    class Meta:
        model = Tariffs
        fields = ('date_start', 'water_supply', 'water_drainage', 'heating_water', 'el_day', 'el_night')
