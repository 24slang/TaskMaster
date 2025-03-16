from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (
    logout_view,
    AboutMeView,
    RegisterView,
    profile,
)

app_name = 'accounts'

urlpatterns = [
    path("", LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True,
    ), name="login"),


    path("logout/", logout_view, name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path('profile/', profile, name='profile'),
    ]
