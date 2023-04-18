from django import forms
from . import models

class BlockedSiteForm(forms.ModelForm):
    class Meta:
        model = models.BlockedSite
        labels = {
            'link': 'site URL',
        }

        fields = ('name','link',)