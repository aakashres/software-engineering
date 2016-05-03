from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify


# Defines upload location of Authors profile image
def upload_user_image(instance, filename):
    return "%s/%s" %(instance.user.username, filename)

"""
Defines Author class
One to One relation with User
"""


class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    author_image = models.ImageField(upload_to=upload_user_image, height_field="height_field", width_field="width_field", null=True)
    author_bio = models.TextField(null=True)
    author_slug = models.SlugField(unique=True)

    # Object representation in Database
    def __str__(self):
        return self.user.username


# Function for creating slug using username
def create_user_slug(sender, instance, *args, **kwargs):
    instance.author_slug = slugify(instance.user.username)


# Django signal to save slug right before the Author object is saved
pre_save.connect(create_user_slug, sender=Author)


# Function to create Authors profile if not created or load if created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Author.objects.get_or_create(user=instance)

# Django signal to create Author profile(object) right after the User is created
post_save.connect(create_user_profile, sender=User)
