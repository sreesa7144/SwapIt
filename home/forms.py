from django import forms
from . models import UserBooks,Images
from django.contrib.auth.models import User
class BookForm(forms.ModelForm):
    class Meta:
        model = UserBooks
        fields=['book_name','book_author','book_ISBN','book_genre','book_url']

class ImageUploadForm(forms.ModelForm):
     class Meta:
         model=Images
         fields=['image']