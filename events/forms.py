import re
from django.core.exceptions import ValidationError
from events.models import EventComment,EventManager
from django import forms

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
        model = EventComment
        fields = ['content']
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'
class LInput(forms.DateInput):
    input_type = 'url'
def isValid(s):
    Pattern = re.compile("[a-z A-Z]+")
    return Pattern.match(s)

class EventForm(forms.ModelForm):
    start_date=forms.DateField(widget=DateInput)
    end_date=forms.DateField(widget=DateInput)
    start_time=forms.TimeField(widget=TimeInput)
    end_time=forms.TimeField(widget=TimeInput)
    registration_link=forms.URLField(widget=LInput)
    event_title = forms.CharField(label="Event Title ",required=True,
                                  widget=forms.TextInput(attrs={
                                      'placeholder':"Enter event title"
                                  }))
    class Meta:
        model= EventManager
        fields=['event_title','category','description','start_date','end_date','start_time','end_time','seat_limit','entry_fee',
                'location','registration_link','banner'
                ]
    def clean_event_title(self,*args,**kwargs):
        event_title = self.cleaned_data.get("event_title")
        if isValid(event_title):
            if len(event_title) < 10 :
                raise ValidationError("**** title should be at least 10 character")
            else:
                return event_title
        else:
            raise ValidationError("**Enter a valid title.Digits is not allow ")
    def clean_location(self,*args,**kwargs):
        location = self.cleaned_data.get("location")
        if isValid(location):
            if len(location)<10:
                raise ValidationError("** minimum length 10 character")
            else:
                return location
        else:
            raise ValidationError("** Enter a valid format of address")

