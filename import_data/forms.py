
from django import forms
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

from pydantic import ValidationError as PydanticValidationError

from . import tasks
from . import data_validators
from . import redis


class LoadData(forms.Form):
    """Класс формы загрузки данных в формате json"""
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    @classmethod
    def check_file(cls, file):
        file_type = file.name.split('.')[-1]
        return file_type

    @classmethod
    def methods(cls, key):
        methods_dict = {
            'json': data_validators.ProductShopData.parse_raw,
        }
        return methods_dict.get(key)

    def clean_file(self):
        if redis.connection.get('import_data') == b'1':
            raise ValidationError(_('Идет импорт'))

        if self.check_file(self.cleaned_data['file']) != 'json':
            raise ValidationError(_('Файл должен быть формата json'))

        try:
            self.data = self.import_data()
            self.methods(self.check_file(self.cleaned_data['file']))(self.data)
        except PydanticValidationError as e:
            raise ValidationError(_('Неверно составлен файл.') + '\n{}'.format(e))

        return self.cleaned_data['file']

    def import_data(self):
        file = self.cleaned_data.get('file')
        with file.open() as f:
            data = f.read()
        return data

    def load(self, request):
        data = self.data.decode('utf-8')
        tasks.import_data_to_db.delay(data, request.user.email)
