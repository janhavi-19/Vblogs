from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,date
from django.urls import reverse
from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Post(models.Model):
    title = models.CharField(max_length=255)
    Poster = models.ImageField( upload_to="Posters/",default="/Posters/intro-1.jpeg")
    # title_tag = models.CharField(max_length=255,default="vBlogs")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # body = models.TextField()
    body = RichTextField(blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    Categories = models.CharField(max_length=255, default="['uncategorised']")
    snippet=models.CharField(max_length=255)
    # Categories = MultiSelectField(choices = choice_list, default='Uncategorised')
    # views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        # return reverse('blog-detail', args=(str(self.id)))
        return reverse('home')


class Categories(models.Model):
    title = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,null = True,related_name="created_by",on_delete=models.CASCADE)
    Meta_Titles = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return reverse('blog-detail', args=(str(self.id)))
        return reverse('home')

class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    bio = models.TextField()
    Profile_pic = models.ImageField( upload_to="Profiles/",default="/Posters/intro-1.jpeg")
    personal_website_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        # return reverse('blog-detail', args=(str(self.id)))
        return reverse('home')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

class Thoughts(models.Model):
    post = models.ForeignKey(Post, related_name="thoughts", on_delete=models.CASCADE)
    user = models.ForeignKey(User,null = True,related_name="user",on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    thoughts = models.TextField()
    
    def __str__(self):
        return '%s' % (self.post.title)

class TrendingEmailNotification(models.Model):
    user = models.ForeignKey(User, related_name="thoughts", on_delete = models.CASCADE)
    date_last_sent = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

