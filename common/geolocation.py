import os
import requests
import json
import urllib.parse
import urllib.request

def getGeoCordinates(location):
	url = 'https://maps.googleapis.com/maps/api/geocode/json'
	params = {
		'sensor':'true',
		'apikey': os.environ.get("GOOGLE_MAPS_KEY"),
		'address': location
	}
	query = url+"?sensor="+params['sensor']+"&address="+params['address']+"&key="+params['apikey']
	print("Query: " + query)
	try:
		response = requests.get(query)
		type = response.headers['content-type']
		result = response.json()
		lat = result['results'][0]['geometry']['location']['lat']
		lng = result['results'][0]['geometry']['location']['lng']
	except:
		lat,lng = (0,0)

	return (lat,lng)