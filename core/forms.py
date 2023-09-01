from django import forms
from core.models import Url
from django.core.exceptions import ValidationError

class UrlForm(forms.Form):
    url = forms.URLField(required=True, max_length=255)
    hashed_url = forms.CharField(max_length=10)
    
    def clean_hashed_url(self):
        # Ensures if a custom hashed_url is provided, it is unique in our db
        hashed_url = self.cleaned_data["hashed_url"]
        if hashed_url and Url.objects.filter(hashed_url=hashed_url).exists():
            raise ValidationError("The custom hashed url already exists.")
        return hashed_url
        
