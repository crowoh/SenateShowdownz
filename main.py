import api_handler
import data_processor

def main():
    legislators_xml = api_handler.get_legislators()
    if legislators_xml:
        legislators = legislators_xml.findall(".//legislator")
        for legislator in legislators[:10]:  # Process only the first 10 legislators
            cid = legislator.get('cid')
            if cid:
                xml_data = api_handler.get_opensecrets_data(cid, "2020")
                if xml_data:
                    senator_data = data_processor.process_opensecrets_data(xml_data)
                    senator_name = legislator.get('firstlast')
                    print(f"{senator_name}: {senator_data}")
            else:
                print("CID not found in legislator element")

if __name__ == "__main__":
    main()
