from django.urls import path
from .views import ContactView, HealthView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('health/',  HealthView.as_view(),  name='health'),
]
