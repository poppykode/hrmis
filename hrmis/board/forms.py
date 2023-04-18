from django import forms
from . import models

class BoardForm(forms.ModelForm):
    class Meta:
        model = models.Board
        labels = {
            'title': 'Board Title',
        }

        fields = ('title','description',)