# Generated by Django 3.2.13 on 2022-05-10 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Core',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')], max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'M'), ('F', 'F')], max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('chip_number', models.CharField(blank=True, max_length=100, null=True)),
                ('defining_marks', models.TextField(blank=True, max_length=250, null=True)),
                ('personality', models.CharField(blank=True, choices=[('Calm', 'Calm'), ('Mild', 'Mild'), ('Aggressive', 'Aggressive')], max_length=100, null=True)),
                ('contact_number1', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_number2', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, max_length=250, null=True)),
                ('main_img', models.ImageField(blank=True, default='images/dog.png', null=True, upload_to='images/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Core',
            },
        ),
        migrations.CreateModel(
            name='CoreReminders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=50, null=True)),
                ('activity_desc', models.CharField(max_length=250, null=True)),
                ('date_of_activity', models.DateField(blank=True, null=True)),
                ('core', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_reminder', to='core.core')),
            ],
            options={
                'verbose_name_plural': 'CoreReminder',
            },
        ),
        migrations.CreateModel(
            name='CoreHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=50, null=True)),
                ('event_desc', models.CharField(max_length=250, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('core', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core', to='core.core')),
            ],
            options={
                'verbose_name_plural': 'CoreHistory',
            },
        ),
    ]