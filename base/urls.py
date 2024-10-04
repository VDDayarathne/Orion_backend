from django.urls import path
from . import views
from .views import home


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', home, name='home'),
]
