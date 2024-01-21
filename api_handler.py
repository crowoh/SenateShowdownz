import requests

API_KEY = "cb6e1661d5eeb1c5fd8a1dcfa2c23cc74bc9a157"

def get_lobbying_data(endpoint):
    headers = {'Authorization': f'Token {API_KEY}'}
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data: {response.status_code}')
        return None