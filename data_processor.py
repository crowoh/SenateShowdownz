import xml.etree.ElementTree as ET

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

    # Extract total contributions from all contributors
    total_contributions = 0
    for contrib in xml_data.findall('.//contributor'):
        total_tag = contrib.find('total')
        if total_tag is not None and total_tag.text:
            total_contributions += int(total_tag.text)

    contributors = []

    # Process each contributor
    for contrib in xml_data.findall('.//contributor'):
        org_name_element = contrib.find('org_name')
        total_element = contrib.find('total')

        org_name = org_name_element.text if org_name_element is not None and org_name_element.text else "Unknown"
        total = int(total_element.text) if total_element is not None and total_element.text else 0

        percentage = (total / total_contributions) * 100 if total_contributions > 0 else 0
        contributors.append(f"{org_name}: ${total} ({round(percentage, 2)}%)")

    formatted_contributors = '\n'.join(contributors) if contributors else "No contributor data available"
    return formatted_contributors, total_contributions

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
