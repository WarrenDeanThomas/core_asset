# from django.contrib.auth.models import User
# from .models import Limits
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
#
# def create_limit(sender, instance, created, **kwargs):
#
#     if created:
#         Limits.objects.create(owner=instance)
#         print("limit created")
#
#
# post_save.connect(create_limit, sender=User)
#
#
# def update_limit(sender, instance, created, **kwargs):
#
#     if created == False:
#         instance.limit.save()
#         print("limit updated")
#
#
# post_save.connect(update_limit, sender=User)

