from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import UserCreationForm, UserChangeForm
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username']
