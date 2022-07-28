from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Creating custom model manager to retreive all published posts in the db
class PublishedManager(models.Manager):
        def get_queryset(self):
            return super(PublishedManager, self).get_queryset().filter(status='published')
        

# Create your models here.
class Post(models.Model):
        STATUS_CHOICES  = (
                ('draft', 'Draft'),
                ('published', 'Published'),
        )
        title           = models.CharField("Title", max_length=50)
        slug            = models.SlugField(unique_for_date='publish', max_length=200)
        author          = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE, related_name='blog_post')
        body            = models.TextField()
        publish         = models.DateTimeField("Publish", default=timezone.now)
        created         = models.DateTimeField("Created", auto_now=True)
        updated         = models.DateTimeField("Updated", auto_now_add=True)
        status          = models.CharField("Status", max_length=10, default='draft', choices=STATUS_CHOICES)

        tags = TaggableManager()

        # model manager
        objects         = models.Manager() # the default model manager
        published_only  = PublishedManager() # my custom model manager added to it 

        class Meta:
                ordering = ('-publish',)
        
        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('blog:post_details', kwargs={
                'slug':self.slug,
                'year':self.publish.year,
                'month':self.publish.month,
                'day':self.publish.day,
            })
        

class Comment(models.Model):
    post        = models.ForeignKey(Post, related_name="commentx", on_delete=models.CASCADE)
    name        = models.CharField("name", max_length=50)
    email       = models.EmailField('Email', max_length=254)
    body        = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    active      = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return 'Comment by ' + self.name + ' on ' + self.post.title

    