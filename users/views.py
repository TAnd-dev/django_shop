from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView

from users.forms import UserLoginForm, UserRegisterForm


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


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
