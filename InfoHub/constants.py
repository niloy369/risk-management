# development

DB_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'InfoHub',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '/opt/lampp/var/mysql/mysql.sock',
        'PORT': 3306
    }
}

GENDER_CHOICES = [
    (1, 'Male'),
    (2, 'Female'),
]

PLACE_MARKING_CATEGORY = [
    ('INFECTED', 'Infected'),
    ('COMMUNITY_TRANSMISSION', 'Community Transmission'),
    ('LOCAL_GATHERING', 'Local Gathering'),
]

MARKER_COLOR_TYPE = {
    'INFECTED': '#F00',
    'COMMUNITY_TRANSMISSION': '#FF8C00',
    'LOCAL_GATHERING': '#0000ff'
}

RISK_FACTOR = [
    (1, 'No risk'),
    (2, 'Moderate risk'),
    (3, 'High risk')
]
