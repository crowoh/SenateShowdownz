import api_handler
import data_processor
import time

# Add a variable to specify the state
state_to_process = "CA"  # Change this to the state abbreviation you want to process

def main():
    max_legislators_to_process = 20  # Max Legislators to process
    processed_legislators_count = 0

    try:
        print("Fetching legislators...")
        legislators_xml = api_handler.get_legislators(state_to_process)
        if legislators_xml:
            legislators = legislators_xml.findall(".//legislator")
            print(f"Total Legislators Found: {len(legislators)}")

            for legislator in legislators:
                if processed_legislators_count >= max_legislators_to_process:
                    print("Reached max legislators to process.")
                    break

                cid = legislator.get('cid')
                senator_name = legislator.get('firstlast')

                if cid:
                    print(f"Starting to process: {senator_name} (CID: {cid})")
                    time.sleep(1)  # Pause to prevent possible rate limiting

                    try:
                        industry_xml_data = api_handler.get_opensecrets_data(cid, "2020")
                        formatted_contributions = data_processor.process_opensecrets_data(industry_xml_data) if industry_xml_data else "No industry data available"

                        contrib_xml_data = api_handler.get_cand_contrib_data(cid, "2020")
                        if contrib_xml_data:
                            contributors = contrib_xml_data.findall('.//contributor')
                            formatted_contributors = data_processor.format_contributors(contributors)
                            print(f"{senator_name}: {formatted_contributions}. \n\u001b[1mTop Contributors:\u001b[0m\n{formatted_contributors}")
                        else:
                            print(f"{senator_name}: No contributor data available")

                        processed_legislators_count += 1
                    except Exception as e:
                        print(f"An error occurred while processing {senator_name} (CID: {cid}): {e}")

                else:
                    print(f"CID not found for legislator: {senator_name}")

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    main()
