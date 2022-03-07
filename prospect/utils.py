from datetime import datetime
from os.path import splitext

from django.forms import ClearableFileInput


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


class MyClearableFileInput(ClearableFileInput):
    clear_checkbox_label = 'Очистить'
    initial_text = 'Текущий'
    input_text = 'Изменить'
