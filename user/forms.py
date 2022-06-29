from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms

from user.models import User


class UserCreateForm(UserCreationForm):
    service_percent = forms.FloatField(label='Пацент услуги достовшика',
                                       min_value=0, max_value=100)

    class Meta:
        model = User
        fields = 'username', 'fullname', 'user_region', 'user_type'


class UserUpdateForm(forms.ModelForm):
    service_percent = forms.FloatField(label='Пацент услуги достовшика',
                                       min_value=0, max_value=100)

    class Meta:
        model = User
        fields = 'username', 'fullname', 'user_region', 'user_type', 'is_active'
