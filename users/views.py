from django.contrib.auth import login
from django.views.generic import CreateView, FormView

from users.forms import UserLoginForm, UserRegisterForm


class SignUp(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/auth.html'
    success_url = '/'


class SignIn(FormView):
    form_class = UserLoginForm
    template_name = 'user/auth.html'
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
