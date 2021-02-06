from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from mediablog.models import MediaBlog,Comment
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField
def isValid(s):
    Pattern = re.compile("[0-9]+")
    return Pattern.match(s)
class MediaForm(forms.ModelForm):
    class Meta:
        model = MediaBlog
        fields = ['title','link','media_description']
    def clean_title(self,*args,**kwargs):
        title = self.cleaned_data.get("title")
        if  len(title)>10:
            if (isValid(title)):
                raise ValidationError("***input type is not valid")

            else:
                return title

        else:
            raise ValidationError("**this is not a valid title.title lenght must be 10 character")
    def clean_link(self,*args,**kwargs):
        link = self.cleaned_data.get("link")
        if "https://www.youtube.com/watch?v=" in link:
            return link
        else:
            return ValidationError("**it is not a valid youtube link")

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
        model = Comment
        fields = ['content']
