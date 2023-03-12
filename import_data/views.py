from . import forms
from . import services


class ImportDataView(services.ImportDataService):
    """Вьюха страница импорта данных в БД"""
    template_name = 'import_data/import_data.html'
    form = forms.LoadData
