from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_reg$', views.login_reg, name='login_reg'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^success$', views.success, name='success'), # Destroy after linking to main app
]
