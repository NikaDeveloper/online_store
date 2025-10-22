from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Форма для регистрации
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserProfileForm(UserChangeForm):
    # При редактировании профиля не нужно менять пароль
    password = None
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'country', 'avatar', 'email')
