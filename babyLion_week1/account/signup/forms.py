from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from .models import Guestbook
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=('id','name','email','major','nickname','password','phone_number')
        widgets = {'password': forms.PasswordInput()}
    
    def clean_id(self):
        user_id = self.cleaned_data.get('id')
        if CustomUser.objects.filter(id=user_id).exists():
            raise ValidationError('이미 사용 중인 ID입니다. 다른 ID를 선택해주세요.')
        return user_id

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    
class CustomLoginForm(forms.Form):
    id = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'PW'}))
    
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    def authenticate_user(self):
        user_id = self.cleaned_data.get('id')
        password = self.cleaned_data.get('password')
        return authenticate(request=None, id=user_id, password=password)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'hobbies', 'photo', 'major', 'nickname','phone_number']
        widgets = {
            'photo': forms.FileInput()
        }

class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ['name', 'message']