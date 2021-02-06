from django import forms
from journal.models import JournalComment,Journal
from django.core.exceptions import ValidationError
import re
def isValid(s):
    Pattern = re.compile("[0-9]+")
    return Pattern.match(s)
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
        model = JournalComment
        fields = ['content']
class DateInput(forms.DateInput):
    input_type = 'date'
class AddJournalForm(forms.ModelForm):
    publication_year = forms.DateField(widget=DateInput)
    journal_title = forms.CharField(label="Journal Title",required=True)
    jornal_author = forms.CharField(label="Author Name",required=True)

    class Meta:
        model=Journal
        fields=['journal_title','journal_details','jornal_author','publication_year','journal_category','document_type',
                'jornal_cover','journal_type','price','journal_file'
                ]
    def clean_journal_title(self,*args,**kwargs):
        journal_title = self.cleaned_data.get("journal_title")
        if len(journal_title) < 10 :
            raise ValidationError("**title length at least 10 character")
        else:
            if isValid(journal_title):
                raise ValidationError("**only digit not allow")
            else:
                return journal_title
    def clean_jornal_author(self,*args,**kwargs):
        jornal_author = self.cleaned_data.get("jornal_author")
        if len(jornal_author) < 5 :
            raise ValidationError("**title length at least 5 character")
        else:
            if isValid(jornal_author):
                raise ValidationError("**only digit not allow")
            else:
                return jornal_author
