from django.db import models


class Counters(models.Model):
    date_get = models.DateField(verbose_name='Дата снятия показаний')
    month = models.IntegerField(verbose_name='Месяц')
    year = models.IntegerField(verbose_name='Год')
    cw_kitchen = models.IntegerField(verbose_name='Холодная вода: Кухня')
    cw_bathroom = models.IntegerField(verbose_name='Холодная вода: Ванная')
    hw_kitchen = models.IntegerField(verbose_name='Горячая вода: Кухня')
    hw_bathroom = models.IntegerField(verbose_name='Горячая вода: Ванная')
    el_1 = models.IntegerField(verbose_name='Электричество: Тариф 1 (день)')
    el_2 = models.IntegerField(verbose_name='Электричество: Тариф 2 (ночь)')
    notes = models.TextField(verbose_name='Примечание', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Показания счётчиков'
        verbose_name = 'Показания счётчиков'
        unique_together = ('month', 'year')
        ordering = ['-year', '-month']
        get_latest_by = ['-year', '-month']


class Tariffs(models.Model):
    date_start = models.DateField(verbose_name='Начало действия тарифов')
    water_supply = models.DecimalField(verbose_name='Водоснабжение', max_digits=5, decimal_places=2, default=0.00)
    water_drainage = models.DecimalField(verbose_name='Водоотведение', max_digits=5, decimal_places=2, default=0.00)
    heating_water = models.DecimalField(verbose_name='Подогрев воды', max_digits=5, decimal_places=2, default=0.00)
    el_day = models.DecimalField(verbose_name='Электричество: день', max_digits=5, decimal_places=2, default=0.00)
    el_night = models.DecimalField(verbose_name='Электричество: ночь', max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = 'Тарифы'
        verbose_name = 'Тарифы'
        unique_together = ('date_start', )
        ordering = ['-date_start']
