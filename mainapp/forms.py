from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

# __________________________________________Tourist Register Form___________________________________________


class TouristForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.CharField(max_length=4, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    contact_no = forms.CharField(
        max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'age',
                  'contact_no', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tourist = True
        if commit:
            user.save()
        tourist = Tourist.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get(
            'last_name'), age=self.cleaned_data.get('age'), contact_no=self.cleaned_data.get('contact_no'))
        return user

# __________________________________________Main admin Register Form___________________________________________


class adminForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_mainadmin = False
        if commit:
            user.save()
        mainadmin = Mainadmin.objects.create(user=user,)
        return user



# _____________________________________profile form________________________________

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Tourist
        fields = ['email','contact_no','age']
        widgets = {
            "contact_no": forms.NumberInput(attrs={'class': 'form-control'}),
            "age":forms.TextInput(attrs={'class': 'form-control'})

        }




# __________________________________________Login Form___________________________________________

class UserloginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


# __________________________________________Tourplace Form___________________________________________

class tourPlaceForm(forms.ModelForm):
    class Meta:
        model = TourPlaces
        fields = ['state', 'description', 'placeImage']
        labels = {'state': 'State', 'description': 'Description',
                  'placeImage': 'Image'}
        widgets = {
            "state": forms.Select(attrs={'class': 'form-select'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "placeImage": forms.FileInput(attrs={'class': 'form-control'}),
        }





# _________________________________________Carousal Form___________________________________________

class CaroForm(forms.ModelForm):
    class Meta:
        model = CarouselM
        fields = ['t_place',]
        labels = {'t_place': 'Add Place to Carousel', }
        widgets = {
            "t_place": forms.Select(attrs={'class': 'form-select'}),
        }

# _________________________________________state Form___________________________________________

class StateForm(forms.ModelForm):
    class Meta:
        model = States
        fields = ['s_name',]
        labels = {'s_name': 'Add State', }
        widgets = {
            "s_name": forms.TextInput(attrs={'class': 'form-control'}),
        }

# _________________________________________state Form___________________________________________

class QualityForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = ['q_name',]
        labels = {'q_name': 'Add Quality', }
        widgets = {
            "q_name": forms.TextInput(attrs={'class': 'form-control'}),
        }


# ________________________________________TourMoreplaces form_______________________________________

class TourMorePlacesForm(forms.ModelForm):
    class Meta:
        model = TourMorePlaces
        fields = ['place_name','description','placeImage','source_link','category']
        labels = {'place_name': 'Place Name', 'description':'Description','placeImage':'Upload image','source_link':'Embed map link','category':'Select categories'}
        widgets = {
            "place_name": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "placeImage": forms.FileInput(attrs={'class': 'form-control'}),
            "source_link": forms.TextInput(attrs={'class': 'form-control'}),
            "category": forms.CheckboxSelectMultiple(attrs={'class': ''}),
        }





# __________________________________________package Form___________________________________________

class PackageForm(forms.ModelForm):

    class Meta:
        model = Packages
        fields = ['pack_name', 'pack_facility', 'pack_member', 'start_date', 'end_date', 'quality', 'pack_price']
        labels = {
            'pack_name': 'Pack Name', 
            'pack_facility': 'Include Facilities',
            'pack_member': 'Total seats',
            'start_date': 'Starting Date',
            'end_date': 'Ending Date',
            'quality': 'Quality type',
            'pack_price': 'Package Price'
        }
        widgets = {
            "pack_name": forms.TextInput(attrs={'class': 'form-control'}),
            "pack_facility": forms.Textarea(attrs={'class': 'form-control'}),
            "pack_member": forms.NumberInput(attrs={'class': 'form-control'}),
            "start_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            "end_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            "quality": forms.Select(attrs={'class': 'form-select'}),
            "pack_price": forms.NumberInput(attrs={'class': 'form-control'}),
        }






# __________________________________________tour booking Form___________________________________________

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = Tourbooking
        fields = ['contact', 'b_email', 'b_members']
        labels = {
            'contact': 'Contact', 
            'b_email': 'Email',
            'b_members': 'Members',
        }
        widgets = {
            "contact": forms.NumberInput(attrs={'class': 'form-control'}),
            "b_email": forms.EmailInput(attrs={'class': 'form-control'}),
            "b_members": forms.NumberInput(attrs={'class': 'form-control','oninput': 'calculateTotal(this.value)'}),
            
        }




# __________________________________________Review Form___________________________________________

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)], widget=forms.RadioSelect(attrs={"class": "form-control rating"}))

    class Meta:
        model = ReviewPack
        fields = ["r_des", "rating"]
        labels = {
            'r_des': 'Comments', 
        }

        widgets = {
            "r_des": forms.TextInput(attrs={"class": "form-control comment"}),
        }


