from django.urls import path
from django.urls import re_path
from . import views
from .views import url_detail_view, url_set, url_get, url_redirect, test_geo, view_analytics

urlpatterns = [
    path('', views.index, name='index'),
    path('geolocation/', test_geo, name='test_geo'),
    path('url/', url_detail_view, name='url_detail' ),
    re_path(r'^set/(.+)', url_set, name='url_set'),
    path('<hashcode>/', url_get, name='url_get'),
    path('<hashcode>/r/', url_redirect, name='url_redirect'),
    path('<hashcode>/a/', view_analytics, name='url_analytics'),
    # path('test', views.test, name='test'),
    
]
