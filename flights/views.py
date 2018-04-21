import os
from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
from .forms import AirportSearchForm
from .forms import LocationSearchForm
from skyscanner.skyscanner import Flights, FlightsCache
import json
from pprint import pprint
#from django.contrib.staticfiles.templatetags.staticfiles import staticfiles
from django.contrib.staticfiles.storage import staticfiles_storage
import urllib.parse
import urllib.request
import requests
import sys
from common import geolocation

skyscanner_key = os.environ.get("SKYSCANNER_KEY")
#flights_cache_service = FlightsCache(skyscanner_key)
#flights_service = Flights(skyscanner_key)

def index(request):
	# country = flights_cache_service.get_cheapest_quotes(
	# 		    market='UK',
	# 		    currency='GBP',
	# 		    locale='en-GB',
	# 		    originplace= 'UK',
	# 		    destinationplace= 'AE-sky',
	# 		    outbounddate='anytime',
	# 		    inbounddate='anytime').parsed
	if 'origin_field' in request.GET:
		market='UK'
		currency='GBP'
		locale='en-GB'

		# create a form instance and populate it with data from the request:
		form = SearchForm(request.GET)
		# check whether it's valid:
		if form.is_valid():
			origin = form.cleaned_data['origin_field']
			destination = form.cleaned_data['destination_field']
			outbounddate=form.cleaned_data['from_date_field']
			inbounddate=form.cleaned_data['to_date_field']
			api_service=form.cleaned_data['service_field']
			# Make query to the live prices API
			#flights = flights

			if api_service=='browsequotes':
			# Make query to Flights Browse Cache API
				response = flights_cache_service.get_cheapest_quotes(
					market=market,
					currency=currency,
					locale=locale,
					originplace= origin,
					destinationplace= destination,
					outbounddate=outbounddate,
					inbounddate=inbounddate).parsed
				quotes = response['Quotes']
				print("Date format: " + str(type(response['Quotes'][0]['OutboundLeg']['DepartureDate'])))
				routes = []
				dates = []
				outboundDates = []
				inboundDates = []

			elif api_service=='browseroutes':
				response = flights_cache_service.get_cheapest_price_by_route(
					market=market,
					currency=currency,
					locale=locale,
					originplace= origin,
					destinationplace= destination,
					outbounddate=outbounddate,
					inbounddate=inbounddate).parsed
				quotes = response['Quotes']
				routes = response['Routes']
				dates = []
				outboundDates = []
				inboundDates = []

			elif api_service=='browsedates':
				response = flights_cache_service.get_cheapest_price_by_date(
					market=market,
					currency=currency,
					locale=locale,
					originplace= origin,
					destinationplace= destination,
					outbounddate=outbounddate,
					inbounddate=inbounddate).parsed
				quotes = response['Quotes']
				dates = response['Dates']
				outboundDates = sorted(dates["OutboundDates"], key=lambda x:x['PartialDate'])
				inboundDates = sorted(dates["InboundDates"], key=lambda x:x['PartialDate'])
				routes = []

			elif api_service=='browsegrid':
				response = flights_cache_service.get_grid_prices_by_date(
					market=market,
					currency=currency,
					locale=locale,
					originplace= origin,
					destinationplace= destination,
					outbounddate=outbounddate,
					inbounddate=inbounddate).parsed
				dates = response['Dates']
				routes = []
				quotes = []


			context = {
				"api_service": api_service,
				"form": form,
				"from": origin,
				"to": destination,
				"quotes": sorted(quotes, key=lambda x:x['MinPrice']),
				"routes": routes,
				"outboundDates": outboundDates,
				"inboundDates": inboundDates,
				"response": response,
				"repro_url": "http://partners.api.skyscanner.net/apiservices/"
					+ api_service + "/v1.0/" + market + "/" + currency + "/" + locale
					+ "/" + origin + "/" + destination + "/" + outbounddate + "/"
					+ inbounddate + "?apikey=xxxxxxxx"
			}



		else:
			context = {
				"form": form,
				"from": "",
				"to": "",
				"flights": "no flights",
			}
		return render(request, 'flights/results.html', context)

	# if a GET (or any other method) we'll create a blank form
	else:
		form = SearchForm()
		context = {
		"form": form,
		"flights": "please search",
		#"country": country
		}

	return render(request, 'flights/index.html', context)

def search_results(request):
	return render(request, 'flights/results.html', {})

def live_prices(request):
	with open('/Users/sheyman/Documents/Code/API_test_harnesses/static/response.json','r') as flights_file:
			flights = json.load(flights_file)

	#flights = pprint(flights_data)
	return render(request, 'flights/live_prices.html', {"flights":flights})

def travel_insights(request):

	#flights = pprint(flights_data)
	return render(request, 'flights/travel_insights.html', {})

def routes(request):
	airport = "SFO"
	market = "US"
	period = "2017-05"

	if 'airport' in request.GET:
		form = AirportSearchForm(request.GET)
		if form.is_valid():
			airport = form.cleaned_data['airport']

	else:
		form = AirportSearchForm()
		airport = "MAD"

	most_searched_data = getMostSearchedData(airport, period, market)
	most_travelled_data = getMostTraveledData(airport, period, market)

	data = {
			"form": form,
			"airport": airport,
			"market": market,
			"most_searched_data": most_searched_data,
			"most_travelled_data": most_travelled_data,
		}
	return render(request, 'flights/routes.html', data)

def airports(request):
	lat,lng = (0,0)
	airport_results = {}
	if 'location' in request.GET:
		form = LocationSearchForm(request.GET)
		if form.is_valid():
			location = form.cleaned_data['location']
			lat,lng = geolocation.getGeoCordinates(location)
			airport_results = getAirports(lat,lng,10)

	else:
		form = LocationSearchForm()
		location = "London"
		lat,lng = geolocation.getGeoCordinates(location)
		airport_results = getAirports(lat,lng,10)

	return render(request, 'flights/airports.html', {'form': form, 'lat':lat,'lng':lng, 'result': airport_results, 'location': location, 'area':location})

def sandbox_low_fare_search(request):
	origin = "NYC"
	destination = "WAS"
	currency = "EUR"
	json_data = getLowFareFlights(origin, destination,'2018-08-01','2018-08-10', 'sandbox', currency)
	quotes = json_data["results"]
	return render(request, 'flights/flight-low-fare-search.html', {"service": "Innovation Sandbox", "currency": currency, "quotes":quotes, "from": origin, "to":destination})

def flight_low_fare_search(request):
	origin = "CDG"
	destination = "YVR"
	currency="EUR"
	json_data = getLowFareFlights(origin, destination,'2018-08-01','2018-08-10', 'ama4dev', currency)
	quotes = json_data["data"]
	return render(request, 'flights/flight-low-fare-search.html', {"service": "Amadeus for Developers", "currency": currency,"quotes":quotes, "from": origin, "to":destination})

def getLowFareFlights(origin, destination, departure_date, return_date, service, currency):
	if service == 'sandbox':
		api_endpoint = "https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?"
		headers = {}
		values = {	
			"origin": origin,
			"destination": destination,
			"apikey": os.environ.get("AMADEUS_SANDBOX_KEY"),
			"departure_date": departure_date,
			"return_date": return_date
		}
	else:
		api_endpoint = "https://test.api.amadeus.com/v1/shopping/flight-offers?"
		headers = {
			'Authorization': 'Bearer ' + getOAuthToken()
		}
		values = {
			"origin": origin,
			"destination": destination,
			# Different date format to Sandbox!
			"departureDate": departure_date,
			"returnDate": return_date,
			"adults": 1,
			"currency": currency
		}
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	req = urllib.request.Request(api_endpoint, headers= headers)
	response = urllib.request.urlopen(req)
	try:
		json_data = json.load(response)
	except:
		json_data = None
		return({'error': "Failed to parse the response."})

	return json_data

def getAirports(lat,lng,limit):
	api_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/airports?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"latitude": lat,
		"longitude": lng,
		"sort": "relevance",
		"page[limit]": limit
	}
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	req = urllib.request.Request(api_endpoint, headers= headers)
	response = urllib.request.urlopen(req)
	try:
		json_data = json.load(response)
	except:
		json_data = None
		return({'error': "Failed to parse the response."})

	return json_data

def getOAuthToken():
	secrets = {
        'client_id': os.environ.get("AMADEUS_CLIENT_ID"),
        'client_secret': os.environ.get("AMADEUS_CLIENT_SECRET"),
        'grant_type': 'client_credentials'
    }
	ACCESS_TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

	authorization_response = (requests.post(
		ACCESS_TOKEN_URL,
		data=secrets
	)).json()
	return authorization_response['access_token']

def getMostSearchedData(airport_code, time_period, market):
	# Most searched data
	# ------------------
	searches_xs=['x']
	searches = ['searches']

	api_endpoint = "https://test.api.amadeus.com/v1/travel/analytics/fare-searches?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"origin": airport_code,
		"sourceCountry": market,
		"period": time_period,
		"maxDestinations": 5
	}
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	print("Endpoint: "+api_endpoint)
	req = urllib.request.Request(api_endpoint, headers= headers)
	response = urllib.request.urlopen(req)
	try:
		json_data = json.load(response)
		
	except:
		json_data = None
		most_searched_destinations = {'error': "Failed to get API data."}
	

	if json_data:
		for data_entry in json_data["data"][0]["numberOfSearches"]["perDestination"].items():
			searches_xs.append(data_entry[0])
			searches.append(data_entry[1])
		most_searched_destinations = {
				"xs": json.dumps(searches_xs),
				"searches": json.dumps(searches)
			}
	else: 
		most_searched_destinations = {
			"xs": 0,
			"searches": 0
		}
	return most_searched_destinations

def getMostTraveledData(airport_code, time_period, market):
	# Most booked data
	# ----------------
	travels_xs = ['x']
	travels = ['travels']

	api_endpoint = "https://test.api.amadeus.com/v1/travel/analytics/air-traffic/traveled?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"origin": airport_code,
		"period": time_period,
		"sort": "analytics.travellers.score",
		"max": 10,
		"page[limit]": 5,
	}

	# origin=MAD&period=2015-09&sort=analytics.travellers.score&max=10&page[limit]=5
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	print("Endpoint: " + api_endpoint)
	req = urllib.request.Request(api_endpoint, headers= headers)
	response = urllib.request.urlopen(req)
	try:
		json_data = json.load(response)
		
	except:
		json_data = None
		most_searched_destinations = {'error': "Failed to get API data."}

	# with open('bookings.json','r') as content:
	# 	bookings_values = json.load(content)
	if len(json_data['data']) > 0:
		for data_entry in json_data["data"]:
			travels_xs.append(data_entry["destination"])
			travels.append(data_entry["analytics"]["travellers"]["score"])

	most_travelled_data = {
		"xs": json.dumps(travels_xs),
		"travels": json.dumps(travels)
	}
	return most_travelled_data
