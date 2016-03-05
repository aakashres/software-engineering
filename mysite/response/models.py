from django.db import models
from story.models import Chapter
# Create your models here.


class Response(models.Model):
    commenter = models.CharField(max_length=50)
    like = models.BooleanField(default=False)
    content = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.commenter+"--"+self.chapter.chapter_title
