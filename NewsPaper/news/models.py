from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

news = "NE"
articles = "AR"

POST_TYPES = [
    (news, 'Новость'),
    (articles, 'Статья')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2,
                                 choices=POST_TYPES,
                                 default=news)
    datetime_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='posts_categories')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    datetime_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()