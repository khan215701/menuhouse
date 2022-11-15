from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import profile, User


@receiver(post_save, sender=User)
def post_save_receiver(sender, instance, created, **kwargs):
    if created:
      profile.objects.create(user=instance)
      print('user profile created')
    else:
      try:
        profile_user = profile.objects.get(user=instance) 
        profile_user.save()
        print('user is updated successfully')
      except :
        profile.objects.create(user=instance)
        print('user profile created')
        
@receiver(pre_save, sender=User)
def pre_save_receiver(sender, instance, **kwargs):
  print(instance.username, 'this user has been created')