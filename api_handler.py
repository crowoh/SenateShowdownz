import requests
import xml.etree.ElementTree as ET

API_KEY = '584e0b053a1b80a1059d31bc5bd12309'  # Replace with your valid API key

def get_legislators():
    url = f"http://www.opensecrets.org/api/?method=getLegislators&id=NJ&apikey={API_KEY}&output=xml"
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
