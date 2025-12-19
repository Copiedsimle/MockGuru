from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import ExamSitemap, QuestionPaperSitemap, StaticViewSitemap, BlogSitemap

sitemaps = {
    'exams': ExamSitemap,
    'questionpapers': QuestionPaperSitemap,
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('exam/<slug:slug>/', views.exam_detail, name='exam_detail'),
    path('section/<int:pk>/', views.section_detail, name='section_detail'),
    path('subsection/<int:pk>/', views.subsection_detail, name='subsection_detail'),
    path('questionpaper/<slug:slug>/', views.questionpaper_detail, name='questionpaper_detail'),
    path('attempt/<slug:slug>/', views.attempt_paper, name='attempt_paper'),
    path('bulk-upload/', views.bulk_upload_questions, name='bulk_upload_questions'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
