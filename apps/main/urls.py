
from django.conf.urls import url
from . import views    
app_name = 'main'     
urlpatterns = [
    url(r'^$', views.index, name='index')  ,
    url(r'create_user$', views.create_user, name='create_user')  ,
    url(r'login_user$', views.login_user, name='login_user')  ,
    url(r'travels$', views.travel, name='travel')  ,
    url(r'view/(?P<id>\d+)$', views.view, name='view')  , 
    url(r'join_trip/(?P<id>\d+)$', views.join_trip, name='join_trip')  , 
    url(r'leave_trip/(?P<id>\d+)$', views.leave_trip, name='leave_trip')  , 
    url(r'delete_trip/(?P<id>\d+)$', views.delete_trip, name='delete_trip')  , 
    url(r'create$', views.create, name='create')  ,
    url(r'createTrip$', views.createTrip, name='createTrip')  ,
    url(r'logout$', views.logout, name='logout')  ,
    
]                       