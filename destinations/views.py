from django.http import HttpResponse
from django.shortcuts import render
from .forms import LocationSearchForm
import urllib.parse
import urllib.request
import requests
import json
from pprint import pprint
import os
from common import geolocation

def index(request):
    return render(request, 'destinations/index.html')

def points_of_interest(request):
	location = ""
	provider = ""
	points_of_interest = {}
	if 'location' in request.GET:
		form = LocationSearchForm(request.GET)
		if form.is_valid():
			location = form.cleaned_data['location']
			number_of_results = form.cleaned_data['number_of_results']
			provider = form.cleaned_data['provider']
			category = form.cleaned_data['category']
			points_of_interest = getPointsOfInterest(location, provider, number_of_results, category)
	else:
		form = LocationSearchForm()
	
	error_message = 'error' in points_of_interest

	data = {
		'form': form,
		'provider': provider,
		'location': location,
		'result': points_of_interest,
		'error_message': error_message
	}
	# with open('poi.csv', 'w') as file:
	# 	for poi in points_of_interest["points_of_interest"]:
	# 		file.write(str(poi["title"]))
	# 		file.write("\n")
	# with open('poi.csv', 'w') as file:
	# 	for poi in points_of_interest["POIs"]:
	# 		file.write(str(poi["name"]))
	# 		file.write("\n")
	return render(request, 'destinations/points-of-interest.html', data)


def getPointsOfInterest(location, provider, number_results, category):
	if provider == 'yapq':
		api_endpoint = "https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?"
		values = {
			"city_name": location,
			"apikey": os.environ.get("AMADEUS_SANDBOX_KEY"),
			"number_of_results": number_results,
			"size_of_images": 'small'
		}
		api_endpoint = api_endpoint + urllib.parse.urlencode(values)
		req = urllib.request.Request(api_endpoint)
		response = urllib.request.urlopen(req)
		try:
			json_data = json.load(response)
		except:
			print("Error")
			json_data = {
				"error": "Failed to get API data."
			}
			
	elif provider == 'avuxi':
		api_endpoint = "https://data.avuxiapis.com/v1/POI?"
		coordinates = geolocation.getGeoCordinates(location)
		north = coordinates[0]+0.1
		south = coordinates[0]-0.1
		west = coordinates[1]-0.3
		east = coordinates[1]+0.3

		values = {
			"north": north,
			"south": south,
			"west": west,
			"east": east,
			"key": getOAuthToken(),
			"limit": number_results
		}
		api_endpoint = api_endpoint + urllib.parse.urlencode(values)
		print("Calling AVUXI: {}".format(api_endpoint))
		req = urllib.request.Request(api_endpoint)
		response = urllib.request.urlopen(req)
		try:
			json_data = json.load(response)
		except:
			print("Error")
			json_data = {
				"error": "Failed to get API data."
			}

	elif provider == 'foursquare':
		url = 'https://api.foursquare.com/v2/venues/explore?'
		coordinates = geolocation.getGeoCordinates(location)

		params = {
			"client_id": os.environ.get('FOURSQUARE_CLIENT_ID'),
			"client_secret": os.environ.get('FOURSQUARE_CLIENT_SECRET'),
			"v": '20180323',
			"limit": number_results,
			"section": category
		}
		request_url = url + urllib.parse.urlencode(params)
		request_url = request_url +  "&ll=" + str(coordinates[0]) + "," + str(coordinates[1])
		print("Calling FourSquare: {}".format(request_url))
		req = urllib.request.Request(request_url)
		response = urllib.request.urlopen(req)
		try:
			json_data = json.load(response)
			print("Response: ")
			print(json.dumps(json_data))
		except:
			print("Error")
			json_data = {
				"error": "Failed to get API data."
			}

	else:
		print("Error")
		json_data = {
			"error": "Failed to get API data."
		}
	return json_data

def getOAuthToken():
	secrets = {
        "appid": os.environ.get("AVUXI_APP_ID"),
  		"appsecure": os.environ.get("AVUXI_APP_KEY")
    }
	ACCESS_TOKEN_URL = "https://data.avuxiapis.com/v1/SecureGenerateKey"

	authorization_response = (requests.post(
		ACCESS_TOKEN_URL,
		data=secrets
	)).json()
	return authorization_response['Key']