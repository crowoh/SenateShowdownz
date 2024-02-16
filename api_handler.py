import requests
import xml.etree.ElementTree as ET

# Global API key definition
API_KEY = '584e0b053a1b80a1059d31bc5bd12309'

def get_legislators(state):
    url = f"http://www.opensecrets.org/api/?method=getLegislators&id={state}&apikey={API_KEY}&output=xml"
    return make_request(url)

def get_opensecrets_data(candidate_id, cycle):
    url = f"https://www.opensecrets.org/api/?method=candIndustry&cid={candidate_id}&cycle={cycle}&apikey={API_KEY}&output=xml"
    return make_request(url)

def get_cand_contrib_data(candidate_id, cycle):
    url = f"https://www.opensecrets.org/api/?method=candContrib&cid={candidate_id}&cycle={cycle}&apikey={API_KEY}&output=xml"
    return make_request(url)

def get_independent_expenditures():
    url = f"http://www.opensecrets.org/api/?method=independentExpend&apikey={API_KEY}&output=xml"
    return make_request(url)

def get_cand_summary_data(candidate_id, cycle=''):
    url = f"https://www.opensecrets.org/api/?method=candSummary&cid={candidate_id}&cycle={cycle}&apikey={API_KEY}&output=xml"
    return make_request(url)

def get_cand_sector_data(candidate_id, cycle):
    url = f"https://www.opensecrets.org/api/?method=candSector&cid={candidate_id}&cycle={cycle}&apikey={API_KEY}&output=xml"
    return make_request(url)


def make_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return ET.fromstring(response.content)
        else:
            print(f"Failed to fetch data: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None