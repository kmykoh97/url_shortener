from django.urls import path
from django.urls import re_path
from . import views
from .views import url_detail_view, url_set, url_get, url_redirect, geo_info, view_analytics



urlpatterns = [
    path('', views.index, name='index'), # mainpage with ui for all endpoints below integrated
    path('<hashcode>/', url_redirect, name='url_redirect'), # redirection
    path('<hashcode>/a/', view_analytics, name='url_analytics'), # short url's analytics
    # endpoint test
    re_path(r'^set/(.+)', url_set, name='url_set'), # unit test endpoint for original url => short url
    path('<hashcode>/g', url_get, name='url_get'), # unit test endpoint for short url => original url
    path('geo_info/', geo_info, name='geo_info'), # unit test endpoint for location
]
