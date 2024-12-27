from django.urls import path
from . import views
from .views import make_image


urlpatterns = [
    path('', views.make_image, name='make_image'),
    path('make_image/', make_image, name='make_image'),
]
