from django.urls import path, include
from frontview import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('home_page', views.home_page, name="home_page"),
    path('category', views.category, name='category'),
    path('single', views.single, name="single"),
    path('contact', views.contact, name="contact"),

]
