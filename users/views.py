from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, DetailView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, ProfileForm, EmailForm
from users.models import UserProfile, CustomUser


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user/change_user_data.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Данные успешно изменены')
        return super().form_valid(form)


class SignUp(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/auth.html'

    def get_success_url(self):
        user = self.get_form_kwargs()['instance']
        login(self.request, user)
        next_page = self.request.POST.get('next', '/')
        return next_page


class SignIn(FormView):
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
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)


class ChangeEmailView(BaseUpdateView):
    form_class = EmailForm

    def get_object(self, queryset=None):
        return CustomUser.objects.get(pk=self.request.user.id)


class ChangeDataView(BaseUpdateView):
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
