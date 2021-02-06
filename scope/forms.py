from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.admin import widgets
from django.forms import SelectDateWidget
from django.forms.fields import DateField
import datetime
from datetime import date
import re
from Skillshare import settings
from scope.models import ScopeManage
from django.core.exceptions import ValidationError
class DateInput(forms.DateInput):
    input_type = 'date'
def isValid(s):
    Pattern = re.compile("[a-zA-Z]+")
    return Pattern.match(s)
class AddScopeForm(forms.ModelForm):
    scope_title = forms.CharField(
        label="Scope Title",
        max_length=100,
        widget=forms.TextInput()
    )
    url = forms.URLField(label="Register Url",widget=forms.URLInput(),required=True)
    end_date = forms.CharField(widget=DateInput)
    details = forms.CharField(label="Description",widget=CKEditorWidget(),required=True)
    cover_image = forms.FileField(label="Banner")
    class Meta:
        model=ScopeManage

        fields=['scope_title','category','end_date','details','url','cover_image']
    def clean_scope_title(self,*args,**kwargs):
        scope_title = self.cleaned_data.get("scope_title")
        if len(scope_title) > 10:
            if isValid(scope_title):
                return scope_title
            else:
                raise ValidationError("**enter a valid title")

        else:
            raise ValidationError("** Title  length at lest 10 character")


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={
        'class':'form-control',
        'id':'comm',
        'rows':3,
        'cols':40,
        'padding':'10px',
        'placeholder':"Enter  your Text here",
    }))
    class Meta:
        model = ScopeManage
        fields = ['content']
