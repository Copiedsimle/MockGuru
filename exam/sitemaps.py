from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Exam, QuestionPaper

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['exam_list', 'login', 'signup']

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