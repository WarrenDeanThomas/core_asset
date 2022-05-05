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

# Create your models here.

TYPE = (
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
    ('Other', 'Other')
)


class Core(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_name='owners')
    type = models.CharField(max_length=100, choices=TYPE, null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=250, null=True)
    main_img = models.ImageField(default='images/dog.png', upload_to='images/', blank=True, null=True)
    # created_date = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = 'Core'  # this is the name that will show in admin, not Products

    def __str__(self):
        return f'{self.name}-{self.owner}' # {self.id}-  # this is what displays in admin


class CoreHistory(models.Model):
    # owner = models.ForeignKey(User, models.CASCADE, null=True)
    core = models.ForeignKey('core.Core', on_delete=models.CASCADE, related_name='core')
    event = models.CharField(max_length=50, null=True)
    event_desc = models.CharField(max_length=250, null=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'CoreHistory'  # this is the name that will show in admin, not Products

    def __str__(self):
        return f'{self.core} - {self.event}'
