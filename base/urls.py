from django.urls import path
from . import views
from .views import make_image
from .views import make_text
from django.contrib.auth import views as auth_views
from .views import user_logout
from .views import get_user_scores, get_image_scores, get_text_scores



urlpatterns = [
    path('', views.make_image, name='make_image'),
    path('make_image/', make_image, name='make_image'),
    path('make_text/', make_text, name='make_text'),
    path('login/', views.login_view, name='login'),
    path("logout/", user_logout , name="logout"),
    path('register/', views.register, name='register'),
    path('get_user_scores/', get_user_scores, name='get_user_scores'),
    path('get_image_scores/', get_image_scores, name='get_image_scores'),
    path('get_text_scores/', get_text_scores, name='get_text_scores'),
    
]
