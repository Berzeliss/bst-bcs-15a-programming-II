from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz_list/<str:category>/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('create', views.create_quiz, name='create_quiz'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
