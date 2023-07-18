from django.urls import path
from django.conf import settings

from randomgen import views


app_name = "randomgen"
urlpatterns = [
    path('', views.IndexView.as_view(), name="home")
]