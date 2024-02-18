import xml.etree.ElementTree as ET
from api_handler import (
    get_legislators, get_opensecrets_data, get_cand_contrib_data,
    get_independent_expenditures, get_cand_summary_data,
    get_cand_sector_data, get_memPFDprofile
)   # Ensure api_handler.py is in the same directory or adjust the import path

def safe_int(value, default=0):
    """Safely convert the input value to an integer, handling exceptions."""
    try:
        return int(value.replace(',', ''))
    except ValueError:
        return default

def process_opensecrets_data(xml_data):
    if xml_data is None:
        return "No contribution data available"
    
    industries = xml_data.findall('.//industry')
    total_contributions = sum(safe_int(industry.get('total', '0')) for industry in industries)
    if total_contributions == 0:
        return "No contribution data available"
    
    formatted_contributions = ', '.join(
        f"{industry.get('industry_name', 'N/A')}: {round(safe_int(industry.get('total', '0')) * 100 / total_contributions, 2)}%"
        for industry in industries
    ) + f". Total Contributions: ${total_contributions}"
    
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

def format_contributors(contributors, max_contributors=5): # Change this to make more contributors show up for each legislator
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

def process_cand_sector_data(xml_data):
    if xml_data is None:
        return {"error": "No sector data available"}

    sectors_list = []
    for sector in xml_data.findall('.//sector'):
        sector_name = sector.get('sector_name')
        sector_id = sector.get('sectorid')
        indivs = sector.get('indivs')
        pacs = sector.get('pacs')
        total = sector.get('total')
        sectors_list.append({
            'sector_name': sector_name,
            'sector_id': sector_id,
            'indivs': indivs,
            'pacs': pacs,
            'total': total
        })

    return sectors_list


def process_mempfdprofile_data(xml_data):
    if xml_data is None:
        return {"error": "No financial profile data available"}

    profile = xml_data.find('.//member_profile')
    if profile is None:
        return {"error": "Financial profile data not found"}

    # Extracting asset details
    assets = [{
        'name': asset.get('name', 'N/A'),
        'holdings_low': safe_int(asset.get('holdings_low', '0'), 'N/A'),
        'holdings_high': safe_int(asset.get('holdings_high', '0'), 'N/A'),
        'industry': asset.get('industry', 'N/A'),
        'sector': asset.get('sector', 'N/A'),
        'subsidiary_of': asset.get('subsidiary_of', 'N/A')
    } for asset in profile.findall('.//asset')]

    # Extracting transaction details
    transactions = [{
        'asset_name': transaction.get('asset_name', 'N/A'),
        'tx_date': transaction.get('tx_date', 'N/A'),
        'tx_action': transaction.get('tx_action', 'N/A'),
        'value_low': safe_int(transaction.get('value_low', '0'), 'N/A'),
        'value_high': safe_int(transaction.get('value_high', '0'), 'N/A')
    } for transaction in profile.findall('.//transaction')]

    # Extracting position details
    positions = [{
        'title': position.get('title', 'N/A'),
        'organization': position.get('organization', 'N/A')
    } for position in profile.findall('.//position')]

    # Compiling the complete financial profile
    financial_profile = {
        'name': profile.get('name', 'N/A'),
        'member_id': profile.get('member_id', 'N/A'),
        'net_low': safe_int(profile.get('net_low', '0'), 'N/A'),
        'net_high': safe_int(profile.get('net_high', '0'), 'N/A'),
        'positions_held_count': safe_int(profile.get('positions_held_count', '0'), 'N/A'),
        'asset_count': safe_int(profile.get('asset_count', '0'), 'N/A'),
        'asset_low': safe_int(profile.get('asset_low', '0'), 'N/A'),
        'asset_high': safe_int(profile.get('asset_high', '0'), 'N/A'),
        'transaction_count': safe_int(profile.get('transaction_count', '0'), 'N/A'),
        'tx_low': safe_int(profile.get('tx_low', '0'), 'N/A'),
        'tx_high': safe_int(profile.get('tx_high', '0'), 'N/A'),
        'update_timestamp': profile.get('update_timestamp', 'N/A'),
        'assets': assets,
        'transactions': transactions,
        'positions': positions
    }

    return financial_profile