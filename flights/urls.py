from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='flights'),
    url('live_prices', views.live_prices, name='live_prices'),
    url('travel_insights', views.travel_insights, name='travel_insights'),
    url('search_results', views.search_results, name='search_results'),
    url('travel-intelligence', views.travel_intelligence, name='travel_intelligence'),
    url('airports', views.airports, name='airports'),
    url('flight_low_fare_search', views.flight_low_fare_search, name='flight_low_fare_search'),
]