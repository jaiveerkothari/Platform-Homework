from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view01/homeTimeline/', views.homeTimeline, name='homeTimeline'),
    url(r'^view02/sendTweet/', views.sendTweet, name='sendTweet'),
    url(r'^view01/', views.view01, name='view01'),
    url(r'^view02/', views.view02, name='view02'),

]
