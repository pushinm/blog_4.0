from .models import Profile, Author
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


new_group, created = Group.objects.get_or_create(name='new_group')

ct = ContentType.objects.get_for_model(Author)


my_signal = Signal()



@receiver(post_save, sender=Author)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print('hello')
    if created:
        Profile.objects.create(author=instance)
    if not created:
        instance.author_profile.save()




my_signal.connect(create_or_update_user_profile)