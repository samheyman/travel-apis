import os
import time
import datetime
import csv
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
from collections import OrderedDict

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

def ba(request):
	return render(request, 'flights/ba.html', {})

def routes(request):
	market = "US"
	airport = 'MAD'
	period = '2017-01'

	if 'airport' in request.GET:
		form = AirportSearchForm(request.GET)
		if form.is_valid():
			airport = form.cleaned_data['airport']
			year = form.cleaned_data['year']
			month = form.cleaned_data['month']
			period = "{}-{}".format(year, month)

	else:
		form = AirportSearchForm()
		airport = "MAD"
		month = "01"
		year = "2017"
		period = "2017-01"

	# most_searched_data = getMostSearchedData(airport, period, market)
	most_travelled_data = getMostTraveledData(airport, period, market)
	most_booked_data = getMostBookedData(airport, period, market)
	busiest_period_data = getBusiestPeriodData(airport, year, 'ARRIVING')
	# print("Most Searched Data from {}".format(airport))
	# print(most_searched_data)
	print("Most Traveled Data from {}".format(airport))
	print(most_travelled_data)
	print("Most Booked Data from {}".format(airport))
	print(most_booked_data)
	print("Busiest Period Data from {}".format(airport))
	print(busiest_period_data)

	# error_message = (('error' in most_searched_data) or ('error' in most_travelled_data) or ('error' in most_booked_data) or ('error' in busiest_period_data))

	data = {
			"form": form,
			"airport": airport,
			"year": year,
			"month": month,
			"market": market,
			# "most_searched_data": most_searched_data,
			"most_travelled_data": most_travelled_data,
			"most_booked_data": json.dumps(most_booked_data),
			"busiest_period_data": busiest_period_data,
			# "error_message": error_message
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

def flight_low_fare_search(request):
	origin = "BOS"
	destination = "WAS"
	currency = "EUR"
	departure_date = '2019-10-01',
	return_date = '2019-10-10',
	response_ama4dev = {}

	if 'origin' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			origin = form.cleaned_data['origin']
			destination = form.cleaned_data['destination']
			departure_date = form.cleaned_data['departure_date']
			return_date = form.cleaned_data['return_date']
			response_ama4dev = getLowFareFlights(origin, destination, departure_date, return_date, currency)
			print("THIS IS THE ERROR........ {}".format(response_ama4dev['response_error']))
			if response_ama4dev['response_error'] == "":
				response_ama4dev = convertPriceToNumber(response_ama4dev)
				quotes_ama4dev = response_ama4dev["response"]["data"]
			else:
				quotes_ama4dev = []
			response_time_ama4dev = response_ama4dev["response_time"]
	else:
		form = SearchForm()
		response_ama4dev['response'] = {}
		quotes_ama4dev = []
		response_time_ama4dev = 0
		response_ama4dev['response_error'] = ""

	data = {
		"form": form,
		"origin": origin,
		"destination": destination,
		"departure_date": departure_date,
		"return_date": return_date,
		"currency": currency,
		"response_ama4dev": response_ama4dev['response'],
		"response_time_ama4dev": response_time_ama4dev,
		"quotes_ama4dev": quotes_ama4dev,
		"response_error": response_ama4dev['response_error']
	}
	
	return render(request, 'flights/flight-low-fare-search.html', data)


def getLowFareFlights(origin, destination, departure_date, return_date, currency):
	json_data = {}
	
	api_endpoint = "https://test.api.amadeus.com/v1/shopping/flight-offers?max=300&"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken(),
		'Accept': 'application/vnd.amadeus+json',
	}
	values = {
		"origin": origin,
		"destination": destination,
		"departureDate": departure_date,
		"returnDate": return_date,
		"adults": 1,
		"currency": currency
	}
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	start = time.time()
	print(api_endpoint)
	print("Start time:{}".format(start))
	req = urllib.request.Request(api_endpoint, headers=headers)
	# print("RESPONSE {} >>>>>>>>>".format(response.read()))
	try:
		response = urllib.request.urlopen(req)
		response_data = json.load(response)
		response_error = ""
	except urllib.error.URLError as e:
		response_data = []
		error_message = json.loads(e.read().decode("utf8", 'ignore'))
		print ("REASON: {}".format(error_message['errors'][0]['title']))
		response_error = error_message['errors'][0]['title'] + "\n\n" + error_message['errors'][0]['detail']
	except urllib.error.HTTPError as e:
		response_data = []
		error_message = json.loads(e.read().decode("utf8", 'ignore'))
		print ("REASON: {}".format(error_message['errors'][0]['title']))
		response_error = error_message['errors'][0]['title'] + "\n\n" + error_message['errors'][0]['detail']
	end = time.time()
	print("End time:{}".format(end))
	response_time = (end - start)
	print("API call time: {0:.2f}s".format(response_time))
	json_data['response'] = response_data
	json_data['response_time'] = response_time
	json_data['response_error'] = response_error
	# print("Response format: {}".format(type(json_data['response'])))
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
	print("Fetching access token {}".format(authorization_response['access_token']))
	return authorization_response['access_token']

def getMostSearchedData(airport_code, time_period, market):
	# Most searched data
	# ------------------
	searches_xs=['x']
	searches = ['number of searches']

	api_endpoint = "https://test.api.amadeus.com/v1/travel/analytics/air-traffic/searched?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"originCityCode": airport_code,
		"marketCountryCode": market,
		"searchPeriod": time_period,
		"max": 5
	}
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	print("Endpoint: "+api_endpoint)
	
	try:
		req = urllib.request.Request(api_endpoint, headers= headers)
		response = urllib.request.urlopen(req)
		json_data = json.load(response)
		
	except:
		json_data = None	

	if json_data and json_data["data"]:
		for data_entry in json_data["data"]:
			searches_xs.append(data_entry["destination"])
			searches.append(data_entry["analytics"]["searches"]["score"])
		most_searched_data = {
				"xs": json.dumps(searches_xs),
				"searches": json.dumps(searches)
			}
	else: 
		most_searched_data = {
			"xs": 0,
			"searches": 0,
			"error": "Failed to get API data."

		}
	return most_searched_data

def getMostTraveledData(airport_code, time_period, market):
	# Most Traveled data
	# -------------------

	most_travelled_data = ['destination,travels']
	
	# travels_xs = ['x']
	# travels = ['number of travels']

	api_endpoint = "https://test.api.amadeus.com/v1/travel/analytics/air-traffic/traveled?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"originCityCode": airport_code,
		"period": time_period,
		"sort": "analytics.travelers.score",
		"max": 5,
		# "page[limit]": 5,
	}

	# origin=MAD&period=2015-09&sort=analytics.travellers.score&max=10&page[limit]=5
	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	# print("Endpoint: " + api_endpoint)
	
	try:
		req = urllib.request.Request(api_endpoint, headers= headers)
		response = urllib.request.urlopen(req)
		json_data = json.load(response)
		
	except:
		json_data = None

	# with open('bookings.json','r') as content:
	# 	bookings_values = json.load(content)
	if json_data and json_data["data"]:
		for data_entry in json_data["data"]:
			most_travelled_data.append(data_entry["destination"]+','+str(data_entry["analytics"]["travelers"]["score"]))

	# 	most_travelled_data = {
	# 		"xs": json.dumps(travels_xs),
	# 		"travels": json.dumps(travels),
	# 	}

	# else:
	# 	most_travelled_data = {
	# 		"xs": 0,
	# 		"travels": 0,
	# 		"error": "Failed to get API data."
	# 	}
	with open("static/js/d3/mostTraveled.csv","w") as mycsv:
		# writer = csv.writer(mycsv)
		for row in most_travelled_data:
			mycsv.write(row + '\n')

	return most_travelled_data
	# return ','.join(most_travelled_data) + '\n'

def getMostBookedData(airport_code, time_period, market):
	# Most Booked data
	# -------------------
	most_booked_data = ["destination,travels"]

	# bookings_xs = ['x']
	# bookings = ['number of bookings']

	api_endpoint = "https://test.api.amadeus.com/v1/travel/analytics/air-traffic/booked?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"originCityCode": airport_code,
		"period": time_period,
		"sort": "analytics.travelers.score",
		"max": 5,
	}

	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	# print("Endpoint: " + api_endpoint)
	
	try:
		req = urllib.request.Request(api_endpoint, headers= headers)
		response = urllib.request.urlopen(req)
		json_data = json.load(response)
		
	except:
		json_data = None

	if json_data and json_data["data"]:
		for data_entry in json_data["data"]:
			most_booked_data.append(data_entry["destination"] + ',' + str(data_entry["analytics"]["travelers"]["score"]))

	# 	most_booked_data = {
	# 		"xs": json.dumps(bookings_xs),
	# 		"bookings": json.dumps(bookings),
	# 	}

	# else:
	# 	most_booked_data = {
	# 		"xs": 0,
	# 		"bookings": 0,
	# 		"error": "Failed to get API data."
	# 	}
	with open("static/js/d3/mostBooked.csv","w") as mycsv:
		# writer = csv.writer(mycsv)
		for row in most_booked_data:
			print(row)
			mycsv.write(row + '\n')

	return most_booked_data
	# return '\n'.join(most_booked_data)


def getBusiestPeriodData(city_code, year, direction):
	months = ['x']
	travelers = ['number of travelers']

	api_endpoint = "https://test.api.amadeus.com/v1/travel/analytics/air-traffic/busiest-period?"
	headers = {
		'Authorization': 'Bearer ' + getOAuthToken()
	}
	values = {
		"cityCode": city_code,
		"period": year,
		"direction": direction,
	}

	api_endpoint = api_endpoint + urllib.parse.urlencode(values)
	print("Endpoint: " + api_endpoint)
	
	# try:
	# 	req = urllib.request.Request(api_endpoint, headers= headers)
	# 	response = urllib.request.urlopen(req)
	# 	json_data = json.load(response)
		
	# except:
	# 	json_data = None

	json_data = {
    "meta": {
        "count": 12,
        "links": {
        "self": "https://test.api.amadeus.com/v1/travel/analytics/air-traffic/busiest-period?cityCode=PAR&period=2017&direction=ARRIVING"
        }
    },
    "data": [
        {
            "type": "air-traffic",
            "period": "2017-12",
            "analytics": {
                "travelers": {
                    "score": 20
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-07",
            "analytics": {
                "travelers": {
                    "score": 15
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-08",
            "analytics": {
                "travelers": {
                    "score": 15
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-01",
            "analytics": {
                "travelers": {
                    "score": 10
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-09",
            "analytics": {
                "travelers": {
                    "score": 10
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-02",
            "analytics": {
                "travelers": {
                    "score": 7
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-03",
            "analytics": {
                "travelers": {
                    "score": 6
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-05",
            "analytics": {
                "travelers": {
                    "score": 5
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-06",
            "analytics": {
                "travelers": {
                    "score": 4
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-04",
            "analytics": {
                "travelers": {
                    "score": 3
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-11",
            "analytics": {
                "travelers": {
                    "score": 3
                }
            }
        },
        {
            "type": "air-traffic",
            "period": "2017-10",
            "analytics": {
                "travelers": {
                    "score": 2
                }
            }
        }
    ]
    }

	# with open('bookings.json','r') as content:
	# 	bookings_values = json.load(content)
	if json_data and json_data["data"]:
		for data_entry in json_data["data"]:
			data_entry["period"] = int(data_entry["period"].split('-')[1])
		
		sorted_response = sorted(json_data["data"], key=lambda entry:entry["period"])

		for data_entry in sorted_response:
			months.append(data_entry["period"])
			travelers.append(data_entry["analytics"]["travelers"]["score"])

		busiest_period_data = {
			"months": json.dumps(months),
			"travelers": json.dumps(travelers),
		}

	else:
		busiest_period_data = {
			"months": 0,
			"travelers": 0,
			"error": "Failed to get API data."
		}

	return busiest_period_data



def convertPriceToNumber(data):
	print(json.dumps(data))
	for item in data['response']['data']:
		try:
			item['offerItems'][0]['price']['total'] = float(item['offerItems'][0]['price']['total'])
		except:
			print("Error converting the price to number.")
	return data