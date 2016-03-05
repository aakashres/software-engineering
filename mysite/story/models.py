from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from author.models import Author


# Defines upload location to image related to Story
def upload_story_image(instance, filename):
    return "%s/%s/%s" % (instance.author.user.username, instance.story_title, filename)


"""
Defines Story class
Many to One relation with Author
"""


class Story(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    story_title = models.CharField(max_length=100)
    story_description = models.TextField()
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    story_image = models.ImageField(
        upload_to=upload_story_image,
        height_field="height_field",
        width_field="width_field",
        blank=True
    )
    story_slug = models.SlugField(unique=True)
    time_started = models.DateTimeField(auto_now_add=True, auto_now=False)
    time_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    # Object representation in Database
    def __str__(self):
        return self.story_title


# Function to create story slug using story title
def create_story_slug(sender, instance, *args, **kwargs):
    instance.story_slug = slugify(instance.story_title)


# Django signal to save slug right before the Story object is saved
pre_save.connect(create_story_slug, sender=Story)

"""
Defines Chapter class
Many to One relation with Story
"""


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=150)
    chapter_number = models.IntegerField()
    chapter_content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    time_edited = models.DateTimeField(auto_now_add=False, auto_now=True)
    chapter_slug = models.SlugField(unique=True)

    # Object representation in Database
    def __str__(self):
        return self.story.story_title + "--" + self.chapter_title


# Function to create chapter slug using chapter title
def create_chapter_slug(sender, instance, *args, **kwargs):
    instance.chapter_slug = slugify(instance.chapter_title)


# Django signal to save slug right before the Chapter object is saved
pre_save.connect(create_chapter_slug, sender=Chapter)
