from django import forms
from users.models import CustomUser


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("full_name", "phone_number", "email", "avatar")
