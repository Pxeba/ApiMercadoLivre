import requests
def get_refresh_token(refresh_token):
    url = 'https://api.mercadolibre.com/oauth/token'
    payload = {
        'grant_type': 'refresh_token',
        'client_id': '<client_id>',
        'client_secret': '<client_secret>',
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    return None

if __name__ == '__main__':
    refresh_token = '<refresh_token>'
    get_refresh_token(refresh_token)