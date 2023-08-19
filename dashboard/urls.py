from django.urls import path

from dashboard.views import IndexView, trigger_error

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
