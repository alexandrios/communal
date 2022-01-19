from django.urls import path
from .views import index, CounterCreateView, TariffCreateView, \
    edit_counter, counters, tariffs, edit_tariff, del_tariff, \
    del_counter, do_counter

urlpatterns = [
    path('', index, name='index'),
    path('counters/', counters, name='counters'),
    path('add_counter/', CounterCreateView.as_view(), name='add_counter'),
    path('edit_counter/<int:pk>/', edit_counter, name='edit_counter'),
    path('del_counter/<int:pk>/', del_counter, name='del_counter'),
    path('tariffs/', tariffs, name='tariffs'),
    path('add_tariff/', TariffCreateView.as_view(), name='add_tariff'),
    path('edit_tariff/<int:pk>/', edit_tariff, name='edit_tariff'),
    path('del_tariff/<int:pk>/', del_tariff, name='del_tariff'),
    path('do_counter/<int:pk>/', do_counter, name='do_counter'),
]