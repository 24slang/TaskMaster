from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from taskmanager.models import NotificationSettings


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/about-me.html"


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy("taskmanager:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )

        NotificationSettings.objects.create(user=user)

        login(request=self.request, user=user)

        return redirect(self.get_success_url())


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("accounts:login"))


@login_required
def profile(request):
    """
    Отображает страницу профиля пользователя.
    """
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})
