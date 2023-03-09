from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(
            posts_rating_sum=Sum('post_rating') * 3)
        author_comments_rating = Comment.objects.all().filter(user_id=self.user).aggregate(
            comments_rating_sum=Sum('comment_rating'))

        print(author_posts_rating)
        print(author_comments_rating)

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    ART = 'С'
    NEWS = 'Н'

    TYPES = [(ART, 'Статья'), (NEWS, 'Новссть')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=15, choices=TYPES)
    time_create = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category)
    title = models.CharField(max_length=120)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:125] + '...'


class PostCategory(models.Model):
    category_PostCategory = models.ManyToManyField(Category)
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    created_com = models.DateTimeField(auto_now_add=True)
    rating_com = models.IntegerField(default=0)

    def like(self):
        self.rating_com += 1
        self.save()

    def dislike(self):
        self.rating_com -= 1
        self.save()
