from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils import timezone
from django.db import models
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'blog'

class Rate(models.Model):
    rate = models.IntegerField()
    id_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    cmt = models.TextField()
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    avatar_user = models.ImageField(upload_to='avatars/', blank=True, null=True)
    name_user = models.TextField()
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)