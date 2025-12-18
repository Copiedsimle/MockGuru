from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('exam/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('section/<int:pk>/', views.section_detail, name='section_detail'),
    path('subsection/<int:pk>/', views.subsection_detail, name='subsection_detail'),
    path('questionpaper/<int:pk>/', views.questionpaper_detail, name='questionpaper_detail'),
    path('attempt/<int:pk>/', views.attempt_paper, name='attempt_paper'),
    path('bulk-upload/', views.bulk_upload_questions, name='bulk_upload_questions'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
