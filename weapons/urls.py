from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_weapons, name='weapon_search'),  # root of app shows the search form
]
