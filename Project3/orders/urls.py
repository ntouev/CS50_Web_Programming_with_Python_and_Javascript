from django.urls import path

from . import views

app_name = 'orders' #Need for namespacing in reverse()
urlpatterns = [
    path("", views.home, name="home")
]
