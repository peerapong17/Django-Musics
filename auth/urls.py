
from django.urls import path
from auth import views


urlpatterns = [
    path('create', views.signUpUser, name="signUpUser"),
    path('login', views.signInUser, name="signInUser"),
    path('logout', views.signOutUser, name="signOutUser"),
]
