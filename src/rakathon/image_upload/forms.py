from django import forms
from .models import QueryImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = QueryImage
        fields = ['image_file']
