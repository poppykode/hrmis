from django import forms
from . import models

class ProjectForm (forms.ModelForm):
    class Meta:
        model = models.Project
        labels = {
            'name': 'Project Name',
        }
        fields = ('name',)