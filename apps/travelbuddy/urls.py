from django.conf.urls import url
from . import views       
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_trip_page$', views.create_trip_page, name='create_trip'),
    url(r'^add_trip$', views.add_trip, name='add_trip'),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip, name='join_trip'),
    url(r'^show_trip/(?P<id>\d+)$', views.show_trip, name='show_trip'),      
]