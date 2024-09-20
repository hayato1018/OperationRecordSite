from django import forms
from .models import MasterData

class MasterForm(forms.ModelForm):
    class Meta:
        model = MasterData
        fields = ['project_name', 'project_number', 'phase_number', 'search_text']
