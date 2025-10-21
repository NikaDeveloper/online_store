from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserRegisterForm, UserProfileForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')  # Перенаправляем на страницу входа

    def form_valid(self, form):
        # Сохраняем пользователя
        self.object = form.save()

        # ОТПРАВКА ПРИВЕТСТВЕННОГО ПИСЬМА
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message='Вы успешно зарегистрировались. Теперь вы можете войти.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile_update')

    def get_object(self, queryset=None):
        # Возвращаем объект текущего пользователя
        return self.request.user
