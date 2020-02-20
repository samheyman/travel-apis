from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='flights'),
    url('live_prices', views.live_prices, name='live_prices'),
    url('travel_insights', views.travel_insights, name='travel_insights'),
    url('search_results', views.search_results, name='search_results'),
    url('routes', views.routes, name='routes'),
    url('airports', views.airports, name='airports'),
    # url('sandbox_low_fare_search', views.sandbox_low_fare_search, name='sandbox_low_fare_search'),
    url('flight_low_fare_search', views.flight_low_fare_search, name='flight_low_fare_search'),
    url('fetch_most_traveled_data', views.fetch_most_traveled_data, name='fetch_most_traveled_data'),
    url('fetch_most_booked_data', views.fetch_most_booked_data, name='fetch_most_booked_data')
]