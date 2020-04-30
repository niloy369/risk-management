from django.db import models

# Create your models here.
from InfoHub.constants import GENDER_CHOICES, PLACE_MARKING_CATEGORY, RISK_FACTOR


class PassportInfo(models.Model):
    passport_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255)
    mothers_name = models.CharField(max_length=255)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone_number = models.CharField(max_length=11)
    emergency_contact_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_gender_text(self):
        for gender in GENDER_CHOICES:
            if gender[0] == self.gender:
                return gender[1]


class MarkedPlaces(models.Model):
    title = models.CharField(max_length=100)
    latitude = models.FloatField(max_length=10)
    longitude = models.FloatField(max_length=10)
    radius = models.IntegerField()
    marked_as = models.CharField(choices=PLACE_MARKING_CATEGORY, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=255)
    working_place = models.TextField()
    specialized_in = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    location_want_to_serve_in = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class DeviceRegistry(models.Model):
    imei = models.CharField(max_length=255, unique=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(max_length=30)
    longitude = models.FloatField(max_length=30)


class DistrictWiseUpdates(models.Model):
    district_name = models.CharField(max_length=100)
    total_infected_count = models.IntegerField(default=0)
    new_infected_count = models.IntegerField(default=0)
    total_death_count = models.IntegerField(default=0)
    new_death_count = models.IntegerField(default=0)
    total_recover_count = models.IntegerField(default=0)
    new_recover_count = models.IntegerField(default=0)
    total_test_count = models.IntegerField(default=0)
    new_test_count = models.IntegerField(default=0)
    date = models.DateField()
    division = models.CharField(max_length=50)

    class Meta:
        unique_together = ['district_name', 'date']

    def as_json(self):
        return dict(
            district_name=self.district_name,
            total_infected_count=self.total_infected_count,
            new_infected_count=self.new_infected_count,
            total_death_count=self.total_death_count,
            new_death_count=self.new_death_count,
            total_recover_count=self.total_recover_count,
            new_recover_count=self.new_recover_count,
            total_test_count=self.total_test_count,
            new_test_count=self.new_test_count,
            date=self.date,
            division=self.division,
        )


class UpdateSummary(models.Model):
    total_infected_count = models.IntegerField(default=0)
    new_infected_count = models.IntegerField(default=0)
    total_death_count = models.IntegerField(default=0)
    new_death_count = models.IntegerField(default=0)
    total_recover_count = models.IntegerField(default=0)
    new_recover_count = models.IntegerField(default=0)
    total_test_count = models.IntegerField(default=0)
    new_test_count = models.IntegerField(default=0)
    date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date.strftime('%d/%m/%Y')

    def as_json(self):
        return dict(
            total_infected_count=self.total_infected_count,
            new_infected_count=self.new_infected_count,
            total_death_count=self.total_death_count,
            new_death_count=self.new_death_count,
            total_recover_count=self.total_recover_count,
            new_recover_count=self.new_recover_count,
            total_test_count=self.total_test_count,
            new_test_count=self.new_test_count,
            date=self.date,
        )


class DailyFeedback(models.Model):
    age = models.CharField(max_length=20)
    has_fever = models.BooleanField()
    cough_throat_pain = models.BooleanField()
    has_breathing_problems = models.BooleanField()
    recent_foreign_return = models.BooleanField()
    in_contact_with_infected_people_recently = models.BooleanField()
    in_contact_with_covid19_positive_people_recently = models.BooleanField()
    taking_treatment_for_other_disease = models.BooleanField()
    result = models.IntegerField(choices=RISK_FACTOR)
    device = models.ForeignKey('DeviceRegistry', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
