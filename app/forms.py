from django import forms
from .models import MasterData

class MasterForm(forms.ModelForm):
    class Meta:
        model = MasterData
        fields = ['project_name', 'project_number', 'phase_number', 'search_text', 'inhouse_work_flag']
        widgets = {
            'inhouse_work_flag': forms.Select(choices=[(1, '社内作業'), (0, '社外作業')])
        }
