import xml.etree.ElementTree as ET
from api_handler import get_independent_expenditures   # Ensure api_handler.py is in the same directory or adjust the import path

def process_opensecrets_data(xml_data):
    total_contributions = sum(int(industry.get('total', 0)) for industry in xml_data.findall('.//industry'))
    if total_contributions == 0:
        return "No contribution data available"

    senator_contributions = []
    for industry in xml_data.findall('.//industry'):
        industry_name = industry.get('industry_name')
        total = int(industry.get('total', 0))
        percentage = (total / total_contributions) * 100 if total_contributions > 0 else 0
        senator_contributions.append(f"{industry_name}: {round(percentage, 2)}%")

    formatted_contributions = ', '.join(senator_contributions) + f". Total Contributions: ${total_contributions}"
    return formatted_contributions

def process_cand_contrib_data(xml_data):
    if xml_data is None:
        return "No contributor data available", 0

    total_contributions = 0
    for contrib in xml_data.findall('.//contributor'):
        total = contrib.find('total').text if contrib.find('total') is not None else 0
        total_contributions += int(total)

    contributors = []
    for contrib in xml_data.findall('.//contributor'):
        org_id = contrib.find('org_name').text  # Assuming org_id is directly available or needs parsing
        total = contrib.find('total').text if contrib.find('total') is not None else 0
        if org_id:
            org_name = get_orgs(org_id)  # Fetching org name using org_id
            percentage = (int(total) / total_contributions) * 100 if total_contributions > 0 else 0
            contributors.append(f"{org_name}: ${total} ({round(percentage, 2)}%)")
        else:
            contributors.append("Unknown Contributor")

    formatted_contributors = '\n'.join(contributors) if contributors else "No contributor data available"
    return formatted_contributors

def format_contributors(contributors, max_contributors=5):
    formatted_list = []
    count = 0
    index = 0

    while count < max_contributors and index < len(contributors):
        contributor = contributors[index]
        index += 1

        org_name = contributor.get('org_name')
        total = contributor.get('total')
        if org_name and total:
            formatted_list.append(f"{org_name}: ${total}")
            count += 1

    total_contributions = "Total Contributions: $" + contributors[0].get('total') if contributors else "No contributor data available"
    formatted_list.insert(0, total_contributions)

    contributors_list = formatted_list[1:]
    top_contributors = "\n".join(contributors_list)

    return top_contributors


def process_independent_expenditures_data():
    xml_data = get_independent_expenditures()
    if xml_data is None:
        return "No independent expenditure data available"

    # Initialize a list to store expenditure transactions
    expenditures_list = []

    # Iterate over each 'indexp' element in the XML
    for indexp in xml_data.findall('.//indexp'):
        expenditure = {
            'cmteid': indexp.get('cmteid'),
            'pacshort': indexp.get('pacshort'),
            'suppopp': indexp.get('suppopp'),
            'candname': indexp.get('candname'),
            'district': indexp.get('district'),
            'amount': indexp.get('amount'),
            'note': indexp.get('note'),
            'party': indexp.get('party'),
            'payee': indexp.get('payee'),
            'date': indexp.get('date'),
            'origin': indexp.get('origin'),
            'source': indexp.get('source')
        }
        expenditures_list.append(expenditure)

    return expenditures_list

def process_cand_summary_data(xml_data):
    if xml_data is None:
        return {"error": "No summary data available"}

    # Assuming xml_data is the <response> element,
    # and the data you need is stored in attributes of the <summary> element.
    summary_element = xml_data.find('.//summary')
    
    if summary_element is None:
        return {"error": "Summary data not found"}

    # Extracting data directly from attributes
    cand_summary = {
        'cand_name': summary_element.get('cand_name', 'N/A'),
        'cid': summary_element.get('cid', 'N/A'),
        'cycle': summary_element.get('cycle', 'N/A'),
        'state': summary_element.get('state', 'N/A'),
        'party': summary_element.get('party', 'N/A'),
        'chamber': summary_element.get('chamber', 'N/A'),
        'first_elected': summary_element.get('first_elected', 'N/A'),
        'next_election': summary_element.get('next_election', 'N/A'),
        'total': summary_element.get('total', 'N/A'),
        'spent': summary_element.get('spent', 'N/A'),
        'cash_on_hand': summary_element.get('cash_on_hand', 'N/A'),
        'debt': summary_element.get('debt', 'N/A'),
        'origin': summary_element.get('origin', 'N/A'),
        'source': summary_element.get('source', 'N/A'),
        'last_updated': summary_element.get('last_updated', 'N/A')
    }

    return cand_summary

