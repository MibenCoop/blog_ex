import os

from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from blog_ex import settings
from blog_ex.settings import STATIC_DIR


class Category(models.Model):
    name = models.CharField(max_length=254,unique=True)
    slug = models.SlugField(unique=True)
    note_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Page(models.Model):
    category = models.ForeignKey(Category)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    date_print = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=5000,)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes',default=0)
    dislikes = models.ManyToManyField(User, related_name='dislikes',default=0)
    favorite = models.ManyToManyField(User, related_name='favorite',default=0)

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()

    @property
    def total_dislikes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.dislikes.count()


class UserProfile(models.Model):
    username = models.OneToOneField(User)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    feed = models.ManyToManyField(Page,related_name='feed',default=0)
    authors = models.ManyToManyField(User,related_name='author',default=0)
    subscribers = models.ManyToManyField(User,related_name='subscriber',default=0)
    pages = models.ManyToManyField(Page,related_name='pages',default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    picture = models.ImageField(upload_to='profile_images',
                                blank=True,default = 'avatar.jpg',)
    @property
    def total_pages(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.pages.count()

class Comment(models.Model):
    owner = models.IntegerField(default=0)
    avatar = models.ImageField(blank=True)
    author = models.CharField(max_length=128)
    date_print = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=5000,)

    def __str__(self):
        return self.author