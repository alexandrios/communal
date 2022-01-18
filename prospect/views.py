from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from prospect.models import Counters, Tariffs
from .forms import CountersForm, TariffsForm


def index(request):
    # counters = Counters.objects.all()
    # context = {'counters': counters}
    return render(request, 'prospect/index.html', None)


def counters(request):
    objs = Counters.objects.all()
    context = {'counters': objs}
    return render(request, 'prospect/counters.html', context)


def tariffs(request):
    objs = Tariffs.objects.all()
    context = {'tariffs': objs}
    return render(request, 'prospect/tariffs.html', context)


class CounterCreateView(CreateView):
    template_name = 'prospect/add_counter.html'
    form_class = CountersForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def edit_counter(request, pk):
    bb = get_object_or_404(Counters, pk=pk)
    if request.method == 'POST':
        bbf = CountersForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
            return counters(request)
        else:
            context = {'form': bbf}
            return render(request, 'prospect/edit_counter.html', context)
    else:
        bbf = CountersForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'prospect/edit_counter.html', context)


class TariffCreateView(CreateView):
    template_name = 'prospect/add_tariff.html'
    form_class = TariffsForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def edit_tariff(request, pk):
    bb = get_object_or_404(Tariffs, pk=pk)
    if request.method == 'POST':
        bbf = TariffsForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
            return tariffs(request)
        else:
            context = {'form': bbf}
            return render(request, 'prospect/edit_tariff.html', context)
    else:
        bbf = TariffsForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'prospect/edit_tariff.html', context)


def do_counter(request, pk):
    counter = get_object_or_404(Counters, pk=pk)
    prev_counter = get_object_or_404(Counters, pk=pk - 1)
    tariff = Tariffs.objects.last()

    res = algo(counter, prev_counter, tariff)

    context = {'result': res}
    return render(request, 'prospect/do_counter.html', context)


def algo(counter, prev_counter, tariff):
    res = []
    res.append("ЭЛЕКТРОЭНЕРГИЯ")
    res.append(f"Расход день: {counter.el_1 - prev_counter.el_1}")
    res.append(f"Тариф день: {tariff.el_day}")
    sum_e1 = (counter.el_1 - prev_counter.el_1) * tariff.el_day
    res.append(f"Сумма по э/э (день): {sum_e1}")

    res.append(f"Расход ночь: {counter.el_2 - prev_counter.el_2}")
    res.append(f"Тариф ночь: {tariff.el_night}")
    sum_e2 = (counter.el_2 - prev_counter.el_2) * tariff.el_night
    res.append(f"Сумма по э/э (ночь): {sum_e2}")

    sum_e = sum_e1 + sum_e2
    res.append(f"Итого сумма по э/э: {sum_e}")

    res.append("НАГРЕВ ВОДЫ")
    res.append(f"Расход: {counter.hw_kitchen - prev_counter.hw_kitchen + counter.hw_bathroom - prev_counter.hw_bathroom}")
    res.append(f"Тариф: {tariff.heating_water}")
    rashod = counter.hw_kitchen - prev_counter.hw_kitchen + counter.hw_bathroom - prev_counter.hw_bathroom
    sum_hw = rashod * tariff.heating_water
    res.append(f"Итого сумма по горячей воде: {sum_hw}")

    res.append("ВОДОСНАБЖЕНИЕ")
    rashod = counter.hw_kitchen - prev_counter.hw_kitchen + counter.hw_bathroom - prev_counter.hw_bathroom + \
             counter.cw_kitchen - prev_counter.cw_kitchen + counter.cw_bathroom - prev_counter.cw_bathroom
    res.append(f"Расход: {rashod}")
    res.append(f"Тариф: {tariff.water_supply}")
    sum_cw = rashod * tariff.water_supply
    res.append(f"Итого сумма по холодной воде: {sum_cw}")

    res.append("ВОДООТВЕДЕНИЕ")
    rashod = counter.hw_kitchen - prev_counter.hw_kitchen + counter.hw_bathroom - prev_counter.hw_bathroom + \
             counter.cw_kitchen - prev_counter.cw_kitchen + counter.cw_bathroom - prev_counter.cw_bathroom
    res.append(f"Расход: {rashod}")
    res.append(f"Тариф: {tariff.water_drainage}")
    sum_vo = rashod * tariff.water_drainage
    res.append(f"Итого сумма по водоотведению: {sum_vo}")

    itogo = sum_e + sum_hw + sum_cw + sum_vo
    res.append(f"ВСЕГО: {itogo}")

    return res
