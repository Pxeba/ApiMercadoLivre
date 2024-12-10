from pprint import pprint
import requests


CODE = 'TG-675848d320a1b4000175c500-180358187'

# https://auth.mercadolibre.com/authorization?response_type=code&client_id=<seu_client_id>&redirect_uri=<seu_redirect_uri>


def get_access_token(auth_code):
    url = 'https://api.mercadolibre.com/oauth/token'
    payload = {
        'grant_type': 'authorization_code',
        'client_id': '<seu_client_id>',
        'client_secret': '<seu_access_token>',
        'code': auth_code,
        'redirect_uri': '<seu_redirect_uri>'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        print(response.json())
        return None



if __name__ == '__main__':
    token_response = get_access_token(CODE)
    pprint(token_response)

    access_token = ''
    if token_response:
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']

    user_response = requests.get(
        f'https://api.mercadolibre.com/users/me?access_token={access_token}')

    if user_response.status_code == 200:
        user_data = user_response.json()
        
    