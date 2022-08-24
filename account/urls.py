from django.urls import path

from .import views

urlpatterns = [
    
# ..........admin User URL.......................
    path('login/', views.LoginPage, name='user_login'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('search-city/', views.SearchCity, name='search-city'),
    path('get-weather-info/', views.GetWeatherInfo, name='get-weather-info'),
    path('get-all-weather-details/', views.AllWeatherDetails, name='all-weather-details'),
    path('logout/', views.logoutUser, name="logout"),
]
