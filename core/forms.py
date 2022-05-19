from django import forms
from .models import Core, CoreHistory, CoreReminders


class DateInput(forms.DateInput):
    input_type = 'date'


class CoreForm(forms.ModelForm):
    class Meta:
        model = Core
        # fields = ['type', 'name', 'description', 'main_img']
        fields = '__all__'
        exclude = ['owner']
        widgets = {'date_of_birth': DateInput()}
            # '__all__'


class CoreHistoryForm(forms.ModelForm):
    class Meta:
        model = CoreHistory
        # fields = '__all__'
        fields = ['event', 'event_desc', 'file', 'date_of_event']
        widgets = {'date_of_event': DateInput()}


class CoreReminderForm(forms.ModelForm):
    class Meta:
        model = CoreReminders
        # fields = '__all__'
        fields = ['activity', 'activity_desc', 'date_of_activity']
        # date_of_activity = forms.DateTimeField(input_formats=['%d/%m/%Y'])
        widgets = {'date_of_activity': DateInput()}




