from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('api/hello/', views.HelloWorldAPIView.as_view(), name='hello_api'),
]
