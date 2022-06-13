from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Common(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users/", default='default.jpg')
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Common, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Author(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    data_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=250)
    text = models.CharField(max_length=20000)
    in_favorite = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return f'{self.heading}'


class FavoritesPost(models.Model):

    common = models.ForeignKey(Common, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.post.heading}" в избранном у "{self.common.user.username}"'


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} = {self.category}'


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    data_time = models.DateTimeField(auto_now_add=True)
    common = models.ForeignKey(Common, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.common} - '{self.text}' к посту '{self.post}'"

    def get_absolute_url(self):
        return f'/news/{self.post.id}'
