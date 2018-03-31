class AccessCredentials():
    secrets = {
        'client_id': '3sY9VNvXIjyJYd5mmOtOzJLuL1BzJBBp',
        'client_secret': 'lAl4Sj2q4xn7Pekq',
        'grant_type': 'client_credentials'
    }

# Storing local variables
# $AMADEUS_CLIENT_ID = ""
# $AMADEUS_CLIENT_SECRET= ""
# os.environ.get('KEY_THAT_MIGHT_EXIST')

# ### With Docker
# Create .env file
# Add all variables: AMADEUS_CLIENT_SECRET= ""
# In docker-compose file add environment: 
#                               - variable_name=$variable_name
# Use 'ENV variable_name' in Dockerfile to add them to the container
# Access them in the code with os.environ.get("VARIABLE_NAME")
# More info: https://vsupalov.com/docker-arg-env-variable-guide/
