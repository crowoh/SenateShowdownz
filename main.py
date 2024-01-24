import api_handler
import data_processor

def format_contributors(contributors, max_contributors=5): #max_contributors = amount of contributors shown
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
    formatted_list.insert(0, total_contributions)  # Insert Total Contributions line

    contributors_list = formatted_list[1:]  # Exclude the Total Contributions line
    top_contributors = "\n".join(contributors_list)  # Join the contributors with newlines

    return top_contributors

def main():
    max_legislators_to_process = 20  # Set this to the desired number of legislators to process
    processed_legislators_count = 0

    try:
        legislators_xml = api_handler.get_legislators()
        if legislators_xml:
            legislators = legislators_xml.findall(".//legislator")
            for legislator in legislators:
                if processed_legislators_count >= max_legislators_to_process:
                    break

                cid = legislator.get('cid')
                if cid:
                    try:
                        senator_name = legislator.get('firstlast')
                        print(f"Processing: {senator_name}")

                        industry_xml_data = api_handler.get_opensecrets_data(cid, "2020")
                        formatted_contributions = data_processor.process_opensecrets_data(industry_xml_data) if industry_xml_data else "No industry data available"

                        contrib_xml_data = api_handler.get_cand_contrib_data(cid, "2020")
                        if contrib_xml_data:
                            contributors = contrib_xml_data.findall('.//contributor')
                            formatted_contributors = format_contributors(contributors)
                        else:
                            formatted_contributors = "No contributor data available"

                        print(f"{senator_name}: {formatted_contributions}. \n\u001b[1mTop Contributors:\u001b[0m\n{formatted_contributors}")
                        processed_legislators_count += 1
                    except Exception as e:
                        print(f"An error occurred while processing {senator_name}: {e}")
                else:
                    print("CID not found in legislator element")

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    main()