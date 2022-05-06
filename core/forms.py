from django import forms
from .models import Core, CoreHistory


class CoreForm(forms.ModelForm):
    class Meta:
        model = Core
        # fields = ['type', 'name', 'description', 'main_img']
        fields = '__all__'
        exclude = ['owner']
            # '__all__'


class CoreHistoryForm(forms.ModelForm):
    class Meta:
        model = CoreHistory
        # fields = '__all__'
        fields = ['event', 'event_desc', 'file']
