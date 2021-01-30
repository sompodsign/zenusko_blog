from django.contrib.auth.models import User
from django import forms


# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label=False, widget=forms.PasswordInput(
#                             attrs={'placeholder': 'Password'}))
#     password2 = forms.CharField(label=False, widget=forms.PasswordInput(
#                             attrs={'placeholder': 'Confirm Password'}))
#
#     class Meta:
#         model = User
#         help_texts = {
#             'username': None,
#         }
#         fields = ('username', 'first_name', 'last_name', 'email')
#
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('passwords don\'t match.')
#         return cd['password2']
