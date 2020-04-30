from django import forms
from django.core.validators import FileExtensionValidator

from API.models import PassportInfo, Announcement, MarkedPlaces, Doctor


class PassportInfoForm(forms.ModelForm):
    class Meta:
        model = PassportInfo
        fields = '__all__'


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'


class MarkedPlacesForm(forms.ModelForm):
    class Meta:
        model = MarkedPlaces
        fields = '__all__'


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control form-control-user'}
    ))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control form-control-user'}
    ))


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
