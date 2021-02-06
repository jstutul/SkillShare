from django import forms
from accounts.models import *
import re
from django.core.exceptions import ValidationError
def isValid(s):
    Pattern = re.compile("[a-z A-Z]+")
    return Pattern.match(s)
def isCity(s):
    Pattern = re.compile("[a-zA-Z]+")
    return Pattern.match(s)
def isPhone(n):
    Pattern = re.compile("[0-9]{11}")
    return Pattern.match(n)

def isAdd(n):
    Pattern =re.compile("^([a-z,0-9,A-Z]+(?:\/[a-z]+)*)$")
    return Pattern.match(n)

class UpdateOrgForm(forms.ModelForm):
    o_name = forms.CharField(label="Organization Name",required=True)
    web =forms.URLField(label="website",required=True)
    phone = forms.CharField(label="Phone",required=True)
    city = forms.CharField(label="City ",required=True)
    photo =forms.ImageField(label="profile Image",required=True)
    address = forms.CharField(label="Address",widget=forms.Textarea())
    purpose = forms.CharField(label="Purpose",widget=forms.Textarea())
    class Meta:
        model = OrganizationUser
        fields =['o_name','web','phone','city','address','purpose','photo']
    def clean_purpose(self,*args,**kwargs):
        purpose = self.cleaned_data.get('purpose')
        if isValid(purpose):
            if len(purpose)<10:
                raise ValidationError("** write something more")
            else:
                return purpose
        else:
            return ValidationError("**enter a valid text")

    def clean_address(self,*args,**kwargs):
        address =self.cleaned_data.get("address")
        if isAdd(address):
            return address
        else:
            raise ValidationError("** address is not valid")
    def clean_city(self,*args,**kwargs):
        city = self.cleaned_data.get('city')
        if isCity(city):
            return city
        else:
            raise ValidationError("**Enter a valid input")
    def clean_phone(self,*args,**kwargs):
        phone = self.cleaned_data.get("phone")
        if isPhone(phone):
            return phone
        else:
            raise ValidationError("** phone no is not valid . must be 11 digit")


    def clean_o_name(self,*args,**kwargs):
        o_name= self.cleaned_data.get("o_name")
        if isValid(o_name):
            if len(o_name) < 5 :
                raise ValidationError("**** title should be at least 5 character")
            else:
                return o_name
        else:
            raise ValidationError("**Enter a valid title.Digits is not allow ")

class UpdateReg(forms.ModelForm):
    phone = forms.CharField(label="Phone No",required=True)
    class Meta:
        model=RegularUser
        fields=['fb','phone','about_you','city','photo']
    def clean_phone(self,*args,**kwargs):
        phone = self.cleaned_data.get("phone")
        if isPhone(phone):
            return phone
        else:
            raise ValidationError("** phone no is not valid . must be 11 digit")

    def clean_city(self, *args, **kwargs):
        city = self.cleaned_data.get('city')
        if isCity(city):
            return city
        else:
            raise ValidationError("**Enter a valid input")
    def clean_fb(self,*args,**kwargs):
        fb = self.cleaned_data.get('fb')
        if 'https://www.facebook.com/' in fb:
            return fb
        else:
            raise ValidationError("** it is not fb link")
    def clean_about_you(self,*args,**kwargs):
        about_you = self.cleaned_data.get('about_you')
        if isValid(about_you):
            if len(about_you)<10:
                raise ValidationError("** write something more")
            else:
                return about_you
        else:
            return ValidationError("**enter a valid text")

class UpdateReg2(forms.ModelForm):
    first_name = forms.CharField(label="FirstName", max_length=20)
    last_name = forms.CharField(label="LastName", max_length=20)
    class Meta:
        model=User
        fields=['first_name','last_name']

    def clean_first_name(self,*args,**kwargs):
        first_name = self.cleaned_data.get('first_name')
        if isCity(first_name):
            return first_name
        else:
            raise ValidationError("** wrong input")
    def clean_last_name(self,*args,**kwargs):
        last_name = self.cleaned_data.get('last_name')
        if isCity(last_name):
            return last_name
        else:
            raise ValidationError("** wrong input")