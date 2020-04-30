import django_filters
from .models import PassportInfo, Doctor


class PassportInfoFilterset(django_filters.FilterSet):
    class Meta:
        model = PassportInfo
        fields = {
            'passport_number': ['icontains'],
            'name': ['icontains'],
            'address': ['icontains'],
        }


class DoctorFilterset(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'location_want_to_serve_in': ['icontains'],
            'specialized_in': ['icontains'],
        }
