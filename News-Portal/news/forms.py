from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.conf import settings


class TimezoneForm(forms.ModelForm):
    """Форма для выбора часового пояса пользователя"""
    
    class Meta:
        model = UserProfile
        fields = ['timezone']
        widgets = {
            'timezone': forms.Select(attrs={
                'class': 'form-control',
                'id': 'timezone-select'
            })
        }
        labels = {
            'timezone': 'Выберите ваш часовой пояс:'
        }


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )
    
    class Meta:
        model = UserProfile
        fields = ['timezone']
        widgets = {
            'timezone': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'timezone': 'Часовой пояс'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
    
    def save(self, commit=True):
        """Сохраняем как профиль, так и данные пользователя"""
        profile = super().save(commit=False)
        
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            
            if commit:
                self.user.save()
        
        if commit:
            profile.save()
        
        return profile 