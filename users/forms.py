from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm

from users.models import User


class UserCreationForm(DefaultUserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(DefaultUserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')
