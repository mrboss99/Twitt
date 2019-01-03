from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Post(models.Model):
    body = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    slug = models.SlugField(max_length=200, blank=True)
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_like',
                                        blank=True)

    def get_absolute_url(self):
        return reverse('Posts:post_detail',
                       args=[self.date.year,
                             self.date.month,
                             self.date.day])

    class Meta:
        ordering = ('-date',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='coments')
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
