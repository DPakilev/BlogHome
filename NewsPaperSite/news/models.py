from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Common(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users/", default='default.jpg')
    slug = models.SlugField(null=True,unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Common, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Author(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)



    def save(self, *args, **kwargs):

        sum_post_rating = 0
        sum_comment_rating = 0
        sum_post_comment_rating = 0
        common = Common.objects.get(user=self.user)

        all_post = Post.objects.filter(author=self)
        all_comment = Comment.objects.filter(common=common)
        for post in all_post:
            sum_post_rating += post.rating
        for comment in all_comment:
            sum_comment_rating += comment.rating
        for post in all_post:
            all_post_comment = Comment.objects.filter(post=post)
            for post_comment in all_post_comment:
                sum_post_comment_rating += post_comment.rating

        self.rating = sum_post_comment_rating + sum_comment_rating + sum_post_rating * 3

        super(Author, self).save(*args, **kwargs)

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
    heading = models.CharField(max_length=50)
    text = models.CharField(max_length=20000)
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def __str__(self):
        return f'{self.heading}'


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} = {self.category}'


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    data_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    common = models.ForeignKey(Common, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def __str__(self):
        return f"{self.common} - '{self.text}' к посту '{self.post}'"

    def get_absolute_url(self):
        return f'/news/{self.post.id}'
