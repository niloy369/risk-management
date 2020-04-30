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
from .views import login_user, logout_user, passport_list, add_passport_view, dashboard, delete_passport_view, \
    edit_passport_view, \
    announcement_list, add_announcement_view, delete_announcement_view,edit_announcement_view, \
    doctors_list, add_doctor_view, edit_doctor_view, delete_doctor_view, \
    marked_places_list, add_marked_place_view, delete_marked_place_view, edit_marked_place_view, read_csv, parse_html
from django.urls import path

app_name = 'frontend'

urlpatterns = [
    path('', login_user, name='login'),
    path('logout/', logout_user, name='logout_user'),
    path('dashboard/', dashboard, name='dashboard'),

    path('passport_info/', passport_list, name='passport_list'),
    path('passport_info/add/', add_passport_view, name='add_passport_view'),
    path('passport_info/edit/<int:passport_id>', edit_passport_view, name='edit_passport_view'),
    path('passport_info/delete/<int:passport_id>', delete_passport_view, name='delete_passport_view'),

    path('announcement/', announcement_list, name='announcement_list'),
    path('announcement/add/', add_announcement_view, name='add_announcement_view'),
    path('announcement/edit/<int:announcement_id>', edit_announcement_view, name='edit_announcement_view'),
    path('announcement/delete/<int:announcement_id>', delete_announcement_view, name='delete_announcement_view'),

    path('doctors/', doctors_list, name='doctors_list'),
    path('doctors/add/', add_doctor_view, name='add_doctor_view'),
    path('doctors/edit/<int:doctor_id>', edit_doctor_view, name='edit_doctor_view'),
    path('doctors/delete/<int:doctor_id>', delete_doctor_view, name='delete_doctor_view'),

    path('marked_places/', marked_places_list, name='marked_places_list'),
    path('marked_places/add/', add_marked_place_view, name='add_marked_place_view'),
    path('marked_places/edit/<int:marked_place_id>', edit_marked_place_view, name='edit_marked_place_view'),
    path('marked_places/delete/<int:marked_place_id>', delete_marked_place_view, name='delete_marked_place_view'),

    path('read_csv/', read_csv, name='read_csv'),
    path('parse_html/', parse_html, name='parse_html'),

]
