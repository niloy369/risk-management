from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import exceptions
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .filterset import PassportInfoFilterset, DoctorFilterset
from .models import PassportInfo, MarkedPlaces, Doctor, Announcement, DeviceRegistry, DistrictWiseUpdates, \
    UpdateSummary, DailyFeedback
from .serializers import PassportInfoSerializer, DoctorSerializer, MarkedPlacesSerializer, \
    AnnouncementListSerializer, DeviceRegistrySerializer, DistrictWiseUpdateSerializer, DailyFeedbackSerializer


# Create your views here.


class PassportInfoListCreateView(ListCreateAPIView):
    serializer_class = PassportInfoSerializer
    queryset = PassportInfo.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PassportInfoFilterset


class MarkedPlacesListCreateView(ListCreateAPIView):
    serializer_class = MarkedPlacesSerializer
    queryset = MarkedPlaces.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = PassportInfoFilterset


class DoctorListCreateView(ListCreateAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DoctorFilterset


class AnnouncementListCreateView(ListAPIView):
    serializer_class = AnnouncementListSerializer
    queryset = Announcement.objects.all()
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = PassportInfoFilterset

    def get_queryset(self):
        queryset = self.queryset

        # a = queryset.annotate(day=TruncDay('created_at')).values('created_at').annotate(c=Count('id')).order_by('-created_at')
        a = queryset.extra(select={'created_at': 'date( created_at )'}).values('created_at') \
            .annotate(available=Count('created_at')).order_by('-created_at')
        return a


class DeviceRegistryCreateView(CreateAPIView):
    serializer_class = DeviceRegistrySerializer
    queryset = DeviceRegistry.objects.all()


class LocationWiseUpdates(RetrieveAPIView):
    serializer_class = DistrictWiseUpdateSerializer
    queryset = DistrictWiseUpdates.objects.all()
    lookup_field = 'district_name'

    def get(self, request, *args, **kwargs):
        district_name = self.kwargs.get('district_name')
        if district_name == 'bangladesh':
            all = UpdateSummary.objects.order_by('-date').first()
            if all is not None:
                return Response(all.as_json())
            return Response(dict(
                total_infected_count=0,
                new_infected_count=0,
                total_death_count=0,
                new_death_count=0,
                total_recover_count=0,
                new_recover_count=0,
                total_test_count=0,
                new_test_count=0,
                date='',
            ))
        queryset = self.queryset.filter(district_name__icontains=district_name).order_by('-date').first()
        if queryset is not None:
            return Response(queryset.as_json())
        raise exceptions.NotFound


class DailyFeedbackCreateView(CreateAPIView):
    serializer_class = DailyFeedbackSerializer
    queryset = DailyFeedback.objects.all()
