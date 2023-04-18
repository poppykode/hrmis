from django import forms
from . import models
from accounts.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        labels = {
            'resource': 'Assign Resource',
        }
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'class': 'datepicker', 'data-date-format': 'YYYY-MM-DD', 'type': 'date'}),
            'end_date':  forms.widgets.DateInput(attrs={'class': 'datepicker', 'data-date-format': 'YYYY-MM-DD', 'type': 'date'})
        }

        fields = ('resource','title','status','percentage_complition','priority','start_date','end_date')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['resource'].queryset = User.objects.filter(
            designation="employee")
        
class TaskUpdateForEmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Task
        labels = {
            'percentage_complition': 'Percentage Completion',
        }
        fields = ('status','percentage_complition',)