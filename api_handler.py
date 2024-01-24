import requests
import xml.etree.ElementTree as ET

API_KEY = '584e0b053a1b80a1059d31bc5bd12309'  # Replace with your valid API key

def get_legislators(state):
    url = f"http://www.opensecrets.org/api/?method=getLegislators&id={state}&apikey={API_KEY}&output=xml"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return ET.fromstring(response.content)
        except ET.ParseError:
            print("Failed to parse XML")
            return None
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def get_opensecrets_data(candidate_id, cycle):
    url = f"https://www.opensecrets.org/api/?method=candIndustry&cid={candidate_id}&cycle={cycle}&apikey={API_KEY}&output=xml"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return ET.fromstring(response.content)
        except ET.ParseError:
            print("Failed to parse XML")
            return None
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def get_cand_contrib_data(candidate_id, cycle='2020'):
    url = f"https://www.opensecrets.org/api/?method=candContrib&cid={candidate_id}&cycle={cycle}&apikey={API_KEY}&output=xml"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            #print(response.content)  # Print the raw XML response for debugging
            try:
                return ET.fromstring(response.content)
            except ET.ParseError:
                print("Failed to parse XML")
                return None
        else:
            print(f"Failed to fetch data: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
