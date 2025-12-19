from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Exam, QuestionPaper
from blog.models import BlogPost

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['exam_list', 'login', 'signup', 'blog_list']

    def location(self, item):
        return reverse(item)

class ExamSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Exam.objects.all()

    def lastmod(self, obj):
        return obj.date if obj.date else None

class QuestionPaperSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return QuestionPaper.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_date