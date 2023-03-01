"""
Import required libraries for views
"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, DetailView, UpdateView, ListView

from shop.models import Purchase
from users.forms import UserLoginForm, UserRegisterForm, ProfileForm, EmailForm
from users.serices import get_user_profile, get_user, get_user_purchases


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    """
    Base class for views which handles updating the user data.
    This view requires user authentication.
    """
    template_name = 'user/change_user_data.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные успешно изменены')
        return super().form_valid(form)


class SignUp(CreateView):
    """
    View for handling user sign up
    """
    form_class = UserRegisterForm
    template_name = 'user/auth.html'

    def get_success_url(self):
        user = self.get_form_kwargs()['instance']
        login(self.request, user)
        next_page = self.request.POST.get('next', '/')
        return next_page


class SignIn(FormView):
    """
    View for handling user sign in
    """
    form_class = UserLoginForm
    template_name = 'user/auth.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Wrong email or password')
        return super().form_invalid(form)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        next_page = self.request.POST.get('next', '/')
        return next_page


class ProfileView(LoginRequiredMixin, DetailView):
    """
    View for displaying user's profile.
    This view requires user authentication
    """
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user.pk)


class ChangeEmailView(BaseUpdateView):
    """
    View for changing the user's email
    """
    form_class = EmailForm

    def get_object(self, queryset=None):
        return get_user(self.request.user.id)


class ChangeDataView(BaseUpdateView):
    """
    View for changing the user's profile data
    """
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user.pk)


class PurchaseView(LoginRequiredMixin, ListView):
    """
    View displays the items in the user's purchases
    """
    model = Purchase
    template_name = 'user/history_purchases.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        return get_user_purchases(self.request.user.pk)


@login_required
def logout_view(request):
    """
    View function that logs the user out of the current session
    """
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
