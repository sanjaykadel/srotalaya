from django import forms
from .models import InfoSource

class InfoSourceForm(forms.ModelForm):
    class Meta:
        model = InfoSource
        fields = ['title', 'url', 'image', 'category', 'tags', 'prompts', 'rating', 'subscribers_count']
