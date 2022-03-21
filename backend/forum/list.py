import requests

auth_endpoint = 'http://localhost:1337/api/auth-token/'
endpoint = 'http://localhost:1337/api/messages/create/'

token = requests.post(auth_endpoint, data={'username': 'jeyde', 'email': 'jeyde@gmail.com', 'password': '123'})

auth_header = 'Token {}'.format(token.json()['token'])
print(auth_header)
response = requests.post(endpoint, data={'room': 1, 'body': 'aaaa'}, headers={'Authorization': auth_header})
print(response.json())
