import datetime

from rest_framework import serializers, exceptions
from .models import PassportInfo, MarkedPlaces, Doctor, Announcement, DeviceRegistry, DistrictWiseUpdates, DailyFeedback


class PassportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportInfo
        fields = '__all__'


class MarkedPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkedPlaces
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class DeviceRegistrySerializer(serializers.ModelSerializer):
    imei = serializers.CharField(max_length=255)

    class Meta:
        model = DeviceRegistry
        fields = '__all__'

    def create(self, validated_data):
        obj, created = DeviceRegistry.objects.update_or_create(
            imei=validated_data['imei'],
            defaults=validated_data
        )
        return obj


class DistrictWiseUpdateSerializer(serializers.ModelSerializer):
    # imei = serializers.CharField(max_length=255, default='Dhaka')

    class Meta:
        model = DistrictWiseUpdates
        fields = '__all__'

    def to_representation(self, instance):
        return instance.as_json()


class DailyFeedbackSerializer(serializers.ModelSerializer):
    imei = serializers.ModelField(model_field=DeviceRegistry()._meta.get_field('imei'), write_only=True)

    class Meta:
        model = DailyFeedback
        exclude = ['device', 'created_at']

    def create(self, validated_data):
        imei = validated_data['imei']
        try:
            device = DeviceRegistry.objects.get(imei=imei)
        except DeviceRegistry.DoesNotExist:
            raise exceptions.NotFound(detail='imei not found')

        validated_data['device_id'] = device.id
        del validated_data['imei']
        obj = DailyFeedback.objects.create(**validated_data)
        return obj


class AnnouncementSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField(method_name='get_time')

    class Meta:
        model = Announcement
        fields = ('title', 'details', 'time',)

    def get_time(self, instance):
        org_date = str(instance.created_at)
        time = datetime.datetime.strptime(org_date, "%Y-%m-%d %H:%M:%S.%f").strftime('%I:%M %p')
        return time


class AnnouncementListSerializer(serializers.ModelSerializer):
    announcements = serializers.SerializerMethodField(method_name='get_announcements')
    date = serializers.SerializerMethodField(method_name='get_day_month_year')

    total = serializers.SerializerMethodField(method_name='get_count_events')

    class Meta:
        model = Announcement
        fields = ('date', 'total', 'announcements',)

    def get_count_events(self, instance):
        org_date = str(instance['created_at'])
        date = datetime.datetime.strptime(org_date, "%Y-%m-%d")
        day = date.day
        month = date.month
        year = date.year
        count = Announcement.objects.filter(created_at__day=day, created_at__month=month, created_at__year=year).count()
        return count

    def get_day_month_year(self, instance):
        org_date = str(instance['created_at'])
        date = datetime.datetime.strptime(org_date, "%Y-%m-%d").date()
        month_year = date.strftime('%d %B %Y')
        if datetime.date.today() == date:
            return 'Today'
        return str(month_year)

    def get_announcements(self, instance):
        org_date = str(instance['created_at'])
        date = datetime.datetime.strptime(org_date, "%Y-%m-%d")
        day = date.day
        month = date.month
        year = date.year
        annoucements = Announcement.objects.filter(created_at__day=day, created_at__month=month,
                                                   created_at__year=year).order_by('-created_at')
        event_serializer = AnnouncementSerializer(annoucements, many=True)
        return event_serializer.data
