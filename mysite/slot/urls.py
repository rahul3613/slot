from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dist', views.dist, name='dist'),
    path('login', views.login, name='login'),
    path('getdata', views.getdata, name='getdata'),
    path('register', views.register, name='register'),
    path('change', views.change, name='change'),
    path('putdata/<str:email>/<int:day>/<int:id>/', views.putdata, name='putdata')
]
