import os

from django.http import JsonResponse
from lxml import etree

import requests
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from API.models import PassportInfo, Announcement, Doctor, MarkedPlaces, DistrictWiseUpdates, UpdateSummary
# Create your views here.
from frontend.forms import PassportInfoForm, AnnouncementForm, DoctorForm, MarkedPlacesForm, LoginForm, CsvUploadForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from InfoHub.constants import MARKER_COLOR_TYPE
from InfoHub.settings import MEDIA_ROOT
import pandas as pd

from frontend.functions import handle_uploaded_file
import datetime


def login_user(request):
    arg = dict()
    arg['form'] = LoginForm
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST or None)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.data.get('username'),
                                password=login_form.data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('frontend:dashboard')
            messages.add_message(request, messages.ERROR, 'Wrong username or password')
            return redirect('frontend:login')
        messages.add_message(request, messages.ERROR, 'Wrong username or password')
        return redirect('frontend:login')
    return render(request, 'login.html', arg)


def logout_user(request):
    logout(request)
    return redirect('frontend:login')


@login_required(login_url='/')
def dashboard(request):
    arg = dict()
    arg['page_title'] = 'Dashboard'
    arg['dashboard'] = 'active'
    arg['passport_infos'] = PassportInfo.objects.all().order_by('-id')
    arg['announcements'] = Announcement.objects.all().order_by('-id')
    arg['doctors'] = Doctor.objects.all().order_by('-id')
    arg['marked_places'] = MarkedPlaces.objects.values('marked_as').annotate(total=Count('marked_as'))
    try:
        arg['infected_marked_places_count'] = next(
            x['total'] for x in arg['marked_places'] if x['marked_as'] == 'INFECTED')
    except Exception as e:
        arg['infected_marked_places_count'] = 0

    try:
        arg['community_transmission_marked_places_count'] = next(
            x['total'] for x in arg['marked_places'] if x['marked_as'] == 'COMMUNITY_TRANSMISSION')
    except Exception as e:
        arg['community_transmission_marked_places_count'] = 0

    try:
        arg['local_gathering_marked_places_count'] = next(
            x['total'] for x in arg['marked_places'] if x['marked_as'] == 'LOCAL_GATHERING')
    except Exception as e:
        arg['local_gathering_marked_places_count'] = 0

    arg['map_info'] = MarkedPlaces.objects.all()
    arg['marker_circle_color'] = MARKER_COLOR_TYPE
    return render(request, 'frontend/dashboard.html', arg)


@login_required(login_url='/')
def passport_list(request):
    arg = dict()
    arg['page_title'] = 'Passport Info List'
    arg['passport_list'] = 'active'
    arg['passport_infos'] = PassportInfo.objects.all().order_by('-id')

    return render(request, 'frontend/passport_info_list.html', arg)


@login_required(login_url='/')
def add_passport_view(request):
    arg = dict()
    arg['page_title'] = 'Passport Info'
    arg['passport_list'] = 'active'
    arg['form'] = PassportInfoForm
    if request.method == 'POST':
        form = PassportInfoForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information added.')
            return redirect('frontend:passport_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def edit_passport_view(request, passport_id):
    arg = dict()
    try:
        passport_info = PassportInfo.objects.get(id=passport_id)
    except PassportInfo.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
        return redirect('frontend:passport_list')
    arg['page_title'] = 'Passport Info'
    arg['passport_list'] = 'active'
    arg['form'] = PassportInfoForm(instance=passport_info)
    if request.method == 'POST':
        form = PassportInfoForm(data=request.POST or None, instance=passport_info)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information updated.')
            return redirect('frontend:passport_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def delete_passport_view(request, passport_id):
    try:
        PassportInfo.objects.get(id=passport_id).delete()
        messages.add_message(request, messages.SUCCESS, 'Information deleted.')
    except PassportInfo.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
    return redirect('frontend:passport_list')


@login_required(login_url='/')
def announcement_list(request):
    arg = dict()
    arg['page_title'] = 'Announcement List'
    arg['announcement_list'] = 'active'
    arg['announcements'] = Announcement.objects.all().order_by('-id')

    return render(request, 'frontend/announcement_list.html', arg)


@login_required(login_url='/')
def add_announcement_view(request):
    arg = dict()
    arg['page_title'] = 'Announcement Info'
    arg['announcement_list'] = 'active'
    arg['form'] = AnnouncementForm
    if request.method == 'POST':
        form = AnnouncementForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information added.')
            return redirect('frontend:announcement_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def edit_announcement_view(request, announcement_id):
    arg = dict()
    try:
        announcement = Announcement.objects.get(id=announcement_id)
    except Announcement.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
        return redirect('frontend:announcement_list')
    arg['page_title'] = 'Passport Info'
    arg['announcement_list'] = 'active'
    arg['form'] = AnnouncementForm(instance=announcement)
    if request.method == 'POST':
        form = AnnouncementForm(data=request.POST or None, instance=announcement)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information updated.')
            return redirect('frontend:announcement_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def delete_announcement_view(request, announcement_id):
    try:
        Announcement.objects.get(id=announcement_id).delete()
        messages.add_message(request, messages.SUCCESS, 'Information deleted.')
    except Announcement.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
    return redirect('frontend:announcement_list')


@login_required(login_url='/')
def doctors_list(request):
    arg = dict()
    arg['page_title'] = 'Doctor List'
    arg['doctors_list'] = 'active'
    arg['doctors'] = Doctor.objects.all().order_by('-id')

    return render(request, 'frontend/doctors_list.html', arg)


@login_required(login_url='/')
def add_doctor_view(request):
    arg = dict()
    arg['page_title'] = 'Doctor Info'
    arg['doctors_list'] = 'active'
    arg['form'] = DoctorForm
    if request.method == 'POST':
        form = DoctorForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information added.')
            return redirect('frontend:doctors_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def edit_doctor_view(request, doctor_id):
    arg = dict()
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
        return redirect('frontend:doctors_list')
    arg['page_title'] = 'Doctor Info'
    arg['doctors_list'] = 'active'
    arg['form'] = DoctorForm(instance=doctor)
    if request.method == 'POST':
        form = DoctorForm(data=request.POST or None, instance=doctor)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information updated.')
            return redirect('frontend:doctors_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def delete_doctor_view(request, doctor_id):
    try:
        Doctor.objects.get(id=doctor_id).delete()
        messages.add_message(request, messages.SUCCESS, 'Information deleted.')
    except Doctor.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
    return redirect('frontend:doctors_list')


@login_required(login_url='/')
def marked_places_list(request):
    arg = dict()
    arg['page_title'] = 'Marked places list'
    arg['marked_places_list'] = 'active'
    arg['marked_places'] = MarkedPlaces.objects.all().order_by('-id')

    return render(request, 'frontend/infected_area_list.html', arg)


@login_required(login_url='/')
def add_marked_place_view(request):
    arg = dict()
    arg['page_title'] = 'Marked places Info'
    arg['marked_places_list'] = 'active'
    arg['form'] = MarkedPlacesForm
    if request.method == 'POST':
        form = MarkedPlacesForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information added.')
            return redirect('frontend:marked_places_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def edit_marked_place_view(request, marked_place_id):
    arg = dict()
    try:
        marked_place = MarkedPlaces.objects.get(id=marked_place_id)
    except MarkedPlaces.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
        return redirect('frontend:marked_places_list')
    arg['page_title'] = 'Marked places Info'
    arg['marked_places_list'] = 'active'
    arg['form'] = MarkedPlacesForm(instance=marked_place)
    if request.method == 'POST':
        form = MarkedPlacesForm(data=request.POST or None, instance=marked_place)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Information updated.')
            return redirect('frontend:marked_places_list')
        arg['form'] = form

    return render(request, 'form_body.html', arg)


@login_required(login_url='/')
def delete_marked_place_view(request, marked_place_id):
    try:
        MarkedPlaces.objects.get(id=marked_place_id).delete()
        messages.add_message(request, messages.SUCCESS, 'Information deleted.')
    except MarkedPlaces.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Information not found.')
    return redirect('frontend:marked_places_list')


@login_required(login_url='/')
def read_csv(request):
    arg = dict()
    arg['form'] = CsvUploadForm
    arg['page_title'] = 'Read CSV'
    arg['read_csv'] = 'active'
    if request.method == 'POST':
        form = CsvUploadForm(data=request.POST or None, files=request.FILES)
        print()
        if form.is_valid():
            file_to_upload = request.FILES['csv_file']
            upload_path = os.path.join(MEDIA_ROOT, 'uploaded_csv')
            handle_uploaded_file(request.FILES['csv_file'], upload_path)
            # with open(request.FILES['csv_file'].file.read()) as csvfile:
            file = pd.read_csv(filepath_or_buffer='{directory}/{file_name}'.format(directory=upload_path,
                                                                                   file_name=file_to_upload.name))
            object_list = []
            for index, row in file.iterrows():
                try:
                    previous_date_info = DistrictWiseUpdates.objects.get(
                        district_name=row['district_name'],
                        date=datetime.datetime.strptime(row['period_date'], '%m/%d/%Y') - datetime.timedelta(days=1),
                    )
                    new_infected_count = row['iedcr_conrifmed'] - previous_date_info.total_infected_count
                    new_recover = 0
                    total_recover = 0
                    if new_infected_count < 0:
                        new_recover = abs(new_infected_count)
                        new_infected_count = 0
                        total_recover = DistrictWiseUpdates.objects.filter(district_name=row['district_name']) \
                            .values('district_name') \
                            .annotate(total_recover=Sum('total_recover_count'))[0]['total_recover']
                except DistrictWiseUpdates.DoesNotExist:
                    new_infected_count = 0
                    new_recover = 0
                    total_recover = 0

                object_list.append(
                    DistrictWiseUpdates(
                        district_name=row['district_name'],
                        total_infected_count=row['iedcr_conrifmed'],
                        new_infected_count=new_infected_count,
                        new_recover_count=new_recover,
                        total_recover_count=total_recover,
                        date=datetime.datetime.strptime(row['period_date'], '%m/%d/%Y'),
                        division=row['Division']
                    )
                )

            DistrictWiseUpdates.objects.bulk_create(object_list, ignore_conflicts=True)
            messages.add_message(request=request, level=messages.SUCCESS, message='Operation Successful')
            return redirect('frontend:dashboard')
        arg['form'] = form
        return render(request, 'form_body.html', arg)

    return render(request, 'form_body.html', arg)


def parse_html(request):
    url = 'https://www.iedcr.gov.bd/'
    response = requests.get(url)

    dom = etree.HTML(response.text)
    last_update_date = dom.xpath('/html/body/div/div[4]/table/thead/tr/th[1]/text()')[0].split(' ')[-1]
    recovered_in_last_24_hours = dom.xpath('/html/body/div/div[5]/div[1]/center[2]/h3/text()')[0]
    total_recovered = dom.xpath('/html/body/div/div[5]/div[2]/center[2]/h3/text()')[0]
    death_in_last_24_hours = dom.xpath('/html/body/div/div[5]/div[3]/center[2]/h3/text()')[0]
    total_death = dom.xpath('/html/body/div/div[5]/div[4]/center[2]/h3/text()')[0]
    test_in_last_24_hours = dom.xpath('/html/body/div/div[4]/table/tbody/tr[1]/td[4]/text()')[0]
    total_test = dom.xpath('/html/body/div/div[4]/table/tbody/tr[2]/td[4]/text()')[0]
    positive_cases_in_last_24_hours = dom.xpath('/html/body/div/div[4]/table/tbody/tr[3]/td[4]/text()')[0]
    total_positive_cases = dom.xpath('/html/body/div/div[4]/table/tbody/tr[4]/td[4]/text()')[0]

    update = UpdateSummary.objects.get_or_create(
        date=datetime.datetime.strptime(last_update_date, '%d-%m-%Y').date(),
        defaults=dict(
            total_infected_count=total_positive_cases,
            new_infected_count=positive_cases_in_last_24_hours,
            total_death_count=total_death,
            new_death_count=death_in_last_24_hours,
            total_recover_count=total_recovered,
            new_recover_count=recovered_in_last_24_hours,
            total_test_count=total_test,
            new_test_count=test_in_last_24_hours,
        )
    )
    return JsonResponse({'status': 'success'})
