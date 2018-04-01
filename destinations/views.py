from django.http import HttpResponse
from django.shortcuts import render
from .forms import LocationSearchForm
import urllib.parse
import urllib.request
import requests
import json
from pprint import pprint
import os

def index(request):
    return render(request, 'destinations/index.html')

def points_of_interest(request):
	location = ""
	points_of_interest = {}
	if 'location' in request.GET:
		form = LocationSearchForm(request.GET)
		if form.is_valid():
			location = form.cleaned_data['location']
			number_of_results = form.cleaned_data['number_of_results']
			provider = form.cleaned_data['provider']
			points_of_interest = getPointsOfInterest(location, provider, number_of_results)
	else:
		form = LocationSearchForm()
		location = ""
	return render(request, 'destinations/points-of-interest.html', {'form': form, 'result': points_of_interest, 'location': location})


def getPointsOfInterest(location, provider, number_results):
	if provider == 'yapq':
		api_endpoint = "https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?"
		values = {
			"city_name": location,
			"apikey": os.environ.get("AMADEUS_SANDBOX_KEY"),
			"number_of_results": number_results
		}
		api_endpoint = api_endpoint + urllib.parse.urlencode(values)
		req = urllib.request.Request(api_endpoint)
		response = urllib.request.urlopen(req)
		try:
			json_data = json.load(response)
		except:
			json_data = None
			
	elif provider == 'avuxi':
		api_endpoint = "https://data.avuxiapis.com/v1/POI?"
		values = {
			"north": 40.516775,
			"south": 40.3000,
			"west": -4.0000,
			"east": -3.403790,
			"key": getOAuthToken(),
			"limit": number_results
		}
		api_endpoint = api_endpoint + urllib.parse.urlencode(values)
		req = urllib.request.Request(api_endpoint)
		response = urllib.request.urlopen(req)
		try:
			json_data = json.load(response)
		except:
			json_data = None
	else:
		print("nope")
		json_data = None
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