import xml.etree.ElementTree as ET

def process_opensecrets_data(xml_data):
    # Calculate the total contributions
    total_contributions = sum(int(industry.get('total', 0)) for industry in xml_data.findall('.//industry'))

    # If no contributions are found, return an appropriate message
    if total_contributions == 0:
        return "No contribution data available"

    # Constructing the contribution percentages
    senator_contributions = []
    for industry in xml_data.findall('.//industry'):
        industry_name = industry.get('industry_name')
        total = int(industry.get('total', 0))
        percentage = (total / total_contributions) * 100 if total_contributions > 0 else 0
        senator_contributions.append(f"{industry_name}: {round(percentage, 2)}%")

    # Append the total contributions to the output
    formatted_contributions = ', '.join(senator_contributions) + f". Total Contributions: ${total_contributions}"
    return formatted_contributions
