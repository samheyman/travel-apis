from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='destinations'),
    url('points-of-interest', views.points_of_interest, name='points-of-interest')

]