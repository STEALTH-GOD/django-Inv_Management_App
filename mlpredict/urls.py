from django.urls import path
from . import views

app_name = 'mlpredict'

urlpatterns = [
    path('predict/', views.predict, name='predict'),
]