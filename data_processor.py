import xml.etree.ElementTree as ET

def process_opensecrets_data(xml_data):
    # Debugging: Print the structure of the XML data
    print("XML Data Structure:")
    ET.dump(xml_data)

    senator_contributions = {}
    cand_name_element = xml_data.find('.//cand_name')
    if cand_name_element is not None:
        senator_name = cand_name_element.text
        for industry in xml_data.findall('.//industry'):
            industry_name = industry.get('industry_name')
            total = int(industry.get('total', 0))
            if senator_name not in senator_contributions:
                senator_contributions[senator_name] = {}
            senator_contributions[senator_name][industry_name] = total
    else:
        print("cand_name element not found in XML")
        return
