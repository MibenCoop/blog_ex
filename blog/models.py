from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=256,unique=True)
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
    date_print = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=5000,)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    favorite = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #sex = models.Field
    picture = models.ImageField(upload_to='profile_images',blank=True)
    def __str__(self):
        return self.user.username