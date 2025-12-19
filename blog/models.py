from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    POST_TYPE_CHOICES = [
        ('blog', 'Blog Post'),
        ('notes', 'Study Notes'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='blog')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_post_type_display()}: {self.title}"

    class Meta:
        ordering = ['-published_date']
