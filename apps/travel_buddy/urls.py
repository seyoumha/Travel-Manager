from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^main$', views.login),
    url(r'^create_user$', views.create_user),
    url(r'^signin$', views.signin),
    url(r'^travel$', views.travel),
    url(r'^logout$', views.logout),
    url(r'^process_travel/(?P<id>\d+)$', views.process_travel),
    url(r'^travel/add$', views.add_travel),
    url(r'^join_travel$', views.join_travel),
    url(r'^travels/destination/(?P<id>\d+)$', views.show_travel)


]
