# myapp/urls.py
from django.urls import path
from . import views
# from .views import youtube_search_view

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    # path('', youtube_search_view, name='youtube_search'),
    # path('scrape-nepal-news/', views.scrape_nepal_news, name='scrape_nepal_news'),

]
