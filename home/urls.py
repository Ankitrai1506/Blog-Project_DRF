from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.BlogView.as_view()),
    path('public/', views.PublicView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('like/', views.LikeView.as_view()),

   
]
