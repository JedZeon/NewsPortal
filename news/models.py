from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

sport = 'SP'
education = 'ED'
policy = 'PO'
economy = 'EC'
zdrav = 'ZD'

TOPICS = [
    (sport, 'Спорт'),
    (policy, 'Политика'),
    (education, 'Образование'),
    (economy, 'Экономика'),
    (zdrav, 'Здравоохранение')
]

news = 'NE'
articles = 'AR'

TYPES = [
    (news, 'Новость'),
    (articles, 'Статья')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)  # рейтинг автора

    def update_rating(self):
        articles_rate = Post.objects.filter(author_id=self.pk).aggregate(Sum('rate'))['rate__sum'] * 3
        comment_rate = Comment.objects.filter(user_id=self.user).aggregate(Sum('rate'))['rate__sum']
        comments_posts_rate = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rate'))['rate__sum']

        self.rate = articles_rate + comment_rate + comments_posts_rate
        self.save()

        return self.rate


class Category(models.Model):
    name = models.CharField(max_length=2, choices=TOPICS, default=zdrav, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_news = models.CharField(max_length=2, choices=TYPES, default=news)
    date_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.date_time.strftime("%d.%m.%Y")}: {self.title.title()} - {self.text[:20]}'

    def preview(self):
        t_ = self.text[0:124]
        return f"{t_}..."

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()
