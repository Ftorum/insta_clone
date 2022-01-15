from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
# Create your models here.


def user_directory_path(instance, filename):
    # file'll be uploaded to media_root
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField()

    def __str__(self):
        return str(self.posted)
    
    def get_absolute_url(self):
            return reverse('post_detail', args=[str(self.id)])


class Followers(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE, related_name='user_id')
    follower_id = models.ForeignKey(User, models.CASCADE, related_name='follower_id')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caption = models.TextField(max_length=500, verbose_name='Comment')
    posted = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.posted)

class PostFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
	file = models.FileField(upload_to=user_directory_path)


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')





