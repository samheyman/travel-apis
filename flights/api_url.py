import urllib
#import hidden

def augment(url, parameters):
    secrets = hidden.oauth()
    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    # token = 
    # oauth_request.sign_request()
    # return oauth_request.to_url()