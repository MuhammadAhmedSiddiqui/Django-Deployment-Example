from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    path('registration/',views.registration,name='registration'),
    path('index/',views.index,name='index'),
    path('logout/',views.user_logout,name='user_logout'),
]
