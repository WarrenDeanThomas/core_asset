import io
from django.conf import settings

from django.utils import timezone
from django.db import models
from django.db.models.fields.files import ImageField
import qrcode
from io import BytesIO
from django.contrib.auth.models import User
from django.core.files import File
from PIL import Image, ImageDraw

import qrcode

from django.db import models
# from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save, pre_save

import json
import requests


# Create your models here.

TYPE = (
    ('Vehicle', 'Vehicle'),
    ('Power Products', 'Power Products'),
    ('Other', 'Other')
)

PERSONALITY = (
    ('Critical', 'Critical'),
    ('Medium', 'Medium'),
    ('Low', 'Low')
)
# SEX = (
#     ('M', 'M'),
#     ('F', 'F')
# )


class Core(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, null=True, related_name='owner')
    type = models.CharField(max_length=100, choices=TYPE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # sex = models.CharField(max_length=100, choices=SEX, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    asset_number = models.CharField(max_length=100, blank=True, null=True)
    # defining_marks = models.TextField(max_length=250, blank=True, null=True)
    impact = models.CharField(max_length=100, choices=PERSONALITY, blank=True, null=True)
    contact_number1 = models.CharField(max_length=100, blank=True, null=True)
    contact_number2 = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.TextField(max_length=250, blank=True, null=True)
    main_img = models.ImageField(default='images/avatar.png', upload_to='images/', editable=True, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    # image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="300")
    # image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")
    #
    # def __unicode__(self):
    #     return "{0}".format(self.main_img)
    #
    # def save(self):
    #     if not self.main_img:
    #         return
    #
    #     super(Core, self).save()
    #     main_img = Image.open(self.main_img)
    #     (width, height) = main_img.size
    #     size = (100, 100)
    #     main_img = main_img.resize(size, Image.ANTIALIAS)
    #     main_img.save(self.main_img.path)

    class Meta:
        verbose_name_plural = 'Core'  # this is the name that will show in admin, not Products

    def __str__(self):
        return f'{self.name}-{self.owner}'  # {self.id}-  # this is what displays in admin


CATEGORY = (
    ('Maintenance', 'Maintenance'),
    ('Repair', 'Repair'),
    ('Fuel', 'Fuel'),
    ('Other', 'Other')
)


class CoreHistory(models.Model):
    # owner = models.ForeignKey(User, models.CASCADE, null=True)
    core = models.ForeignKey('core.Core', on_delete=models.CASCADE, null=True, blank=True, related_name='core')
    category = models.CharField(max_length=100, choices=CATEGORY, blank=True, null=True)
    event = models.CharField(max_length=50, null=True, blank=True)
    event_desc = models.CharField(max_length=250, null=True, blank=True)
    date_of_event = models.DateField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    km_or_hours = models.IntegerField(blank=True, null=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    # date_of_event = models.DateField(null=True, blank=True, default=timezone.now)

    class Meta:
        verbose_name_plural = 'CoreHistory'  # this is the name that will show in admin, not Products

    def __str__(self):
        return f'{self.core} - {self.event}'


class CoreReminders(models.Model):
    core = models.ForeignKey('core.Core', on_delete=models.CASCADE, null=True, blank=True, related_name='core_reminder')
    activity = models.CharField(max_length=50, null=True, blank=True)
    activity_desc = models.CharField(max_length=250, null=True, blank=True)
    date_of_activity = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'CoreReminder'  # this is the name that will show in admin, not Products

    def __str__(self):
        return f'{self.core} - {self.activity}'


# Create your models here.
class Limits(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    number_of_pets = models.PositiveSmallIntegerField(default=5, editable=True, blank=True, null=True)
    paid = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Limits'  # this is the name that will show in admin, not Products

    def __str__(self):
        return f'{self.owner} - {self.number_of_pets}'


def create_limit(sender, instance, created, **kwargs):

    if created:
        Limits.objects.create(owner=instance)
        print("limit created")


post_save.connect(create_limit, sender=User)


# def update_limit(sender, instance, created, **kwargs):
#
#     if created == False:
#         instance.limit.save()
#         print("limit updated")
#
#
# post_save.connect(update_limit, sender=User)


# Create your models here.
class Location(models.Model):
    core = models.ForeignKey('core.CoreHistory', on_delete=models.CASCADE, null=True, blank=True, related_name='core_location')
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Location'  # this is the name that will show in admin, not Products

    def save(self, *args, **kwargs):
        # Directly access tuple values
        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        res = requests.get('http://ip-api.com/json/'+ip_data['ip'])
        location_data_one = res.text
        location_data = json.loads(location_data_one)
        self.latitude = location_data["lat"]
        self.longitude = location_data["lon"]
        self.city = location_data["city"]
        self.country = location_data["country"]
        # self.latitude = self.location[0]
        # self.longitude = self.location1[1]
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.core}'


def create_location(sender, instance, created, **kwargs):

    if created:
        Location.objects.create(core=instance)
        print("location created")


post_save.connect(create_location, sender=CoreHistory)
