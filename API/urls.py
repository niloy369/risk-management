"""InfoHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import PassportInfoListCreateView, MarkedPlacesListCreateView, DoctorListCreateView, \
    AnnouncementListCreateView, DeviceRegistryCreateView, LocationWiseUpdates, DailyFeedbackCreateView
from django.urls import path

urlpatterns = [
    path('passport_info/', PassportInfoListCreateView.as_view()),
    path('marked_place/', MarkedPlacesListCreateView.as_view()),
    path('doctor/', DoctorListCreateView.as_view()),
    path('announcements/', AnnouncementListCreateView.as_view()),
    path('device_register/', DeviceRegistryCreateView.as_view()),
    path('updates/<str:district_name>', LocationWiseUpdates.as_view()),
    path('daily_feedback/', DailyFeedbackCreateView.as_view()),
]
