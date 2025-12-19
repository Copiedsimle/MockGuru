from django.urls import path
from . import views

urlpatterns = [
    path('notes/<slug:slug>/', views.notes_detail, name='notes_detail'),
    path('notes/', views.notes_list, name='notes_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('', views.blog_list, name='blog_list'),
]