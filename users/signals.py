from django.contrib.auth.models import User
from .models import Profile

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings


#############################################################################

# def profileUpdated(sender, instance, created, **kwargs):
#     print('profile Saved!')
#     print('sender:',sender) # sender: <class 'users.models.Profile'>
#     print('instance:',instance) # instance: ahmed
#     print('created:',created) # created: False

def createProfile(sender, instance, created, **kwargs):
    print("Profile signal triggered")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        
        subject = 'Welcome to Dev Search'
        message = 'we are glad you are here!'
        
        send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
                )
        
        
    
def deleteUser(sender, instance, **kwargs):
    try:
        print('deleting user....')
        user = instance.user
        user.delete()
    except:
        pass
    


def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# post_save.connect(profileUpdated, sender=Profile)
post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)
post_save.connect(updateProfile, sender=Profile)


# @receiver(post_save, sender=Profile)
# def createProfile(sender, instance, created, **kwargs):
#     print('profile Saved!')
#     print('sender:',sender) # sender: <class 'users.models.Profile'>
#     print('instance:',instance) # instance: ahmed
#     print('created:',created) # created: False


#############################################################################