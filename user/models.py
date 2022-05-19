from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'{self.staff.username}--Profile'

