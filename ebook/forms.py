import re

from django import forms
from django.core.exceptions import ValidationError

from ebook.models import *
class DateInput(forms.DateInput):
    input_type = 'date'
def isValid(s):
    Pattern = re.compile("[0-9]+")
    return Pattern.match(s)
class AddBookForm(forms.ModelForm):
    book_name   = forms.CharField(required=True,min_length=5,label='Book Name')
    book_author = forms.CharField(required=True,min_length=5,label='Book Author')
    book_edition = forms.IntegerField(label='Book Edition')
    book_publish = forms.DateField(widget=DateInput)

    class Meta:
        model =Ebook
        fields=['book_name','book_author','book_edition','book_publish','category','book_type','cover_pic','book']

    def clean_book_name(self,*args,**kwargs):
        book_name = self.cleaned_data.get('book_name')
        if len(book_name)< 5:
            raise ValidationError("**title length at least 5 character")
        elif isValid(book_name):
            raise ValidationError("**only digit not allow")
        else:
            return book_name

    def clean_book_author(self,*args,**kwargs):
        book_author =self.cleaned_data.get("book_author")
        if len(book_author) < 5 :
            raise ValidationError("**title length at least 5 character")
        else:
            if isValid(book_author):
                raise ValidationError("**only digit not allow")
            else:
                return book_author

    def clean_book_edition(self,*args,**kwargs):
        book_edition =self.cleaned_data.get("book_edition")
        if book_edition>0 and book_edition <20:
            return book_edition
        else:
            raise ValidationError("Edition should be between 1-20 edition")


