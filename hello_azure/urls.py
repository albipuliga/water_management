from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.login_view, name="login_view"),
    path("valve/", views.valve, name="valve"),
]
