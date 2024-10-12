import urllib.parse
import requests
import json


def get_config(file_path = 'C:/Users/admin/Facebook bot/config.json'):

    with open(file_path, 'r') as file:
        config = json.load(file)
    
    # Lấy thông tin từ tệp JSON
    app_id = config.get('app_id')
    app_secret = config.get('app_secret')

    return app_id, app_secret

def get_access_token(file_path = 'C:/Users/admin/Facebook bot/access_token_info.json'):

    with open(file_path, 'r') as file:
        access_token_info = json.load(file)

    access_token = access_token_info['access_token']

    return access_token

# -- Only run tthese lines when access token is expired
# def extend_long_lived_token(long_lived_token, app_id, app_secret):

#     # long_lived_token = get_access_token()
#     # app_id, app_secret = get_config()

#     url = 'https://graph.facebook.com/v13.0/oauth/access_token'
#     params = {
#         'grant_type': 'fb_exchange_token',
#         'client_id': app_id,
#         'client_secret': app_secret,
#         'fb_exchange_token': long_lived_token
#     }
#     response = requests.get(url, params=params)

#     return response.json()

# def refresh_access_token(file_path = 'C:/Users/admin/Facebook bot/access_token_info.json'):

#     long_lived_token = get_access_token()
#     app_id, app_secret = get_config()

#     long_lived_token_info = extend_long_lived_token(long_lived_token, app_id, app_secret)

#     with open(file_path, 'w') as file:
#         json.dump(long_lived_token_info, file, indent=4)
    
#     print(long_lived_token_info)

def get_page_access_token(access_token):
    url = f'https://graph.facebook.com/v10.0/me/accounts?access_token={access_token}'
    response = requests.get(url)
    data = response.json().get('data', [])
    
    if response.status_code == 200:
        filtered_data = [item for item in data if item['name'] == 'Netflix otp'][0]
        page_access_token = filtered_data['access_token']
        page_id = filtered_data['id']
        return page_id, page_access_token
    else:
        return data

def send_message(recipient_id, response):

    access_token = get_access_token()
    page_access_token = get_page_access_token(access_token)

    url = 'https://graph.facebook.com/v13.0/me/messages'
    params = {
        'access_token': page_access_token
    }
    payload = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': response
        }
    }
    response = requests.post(url, params=params, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()



