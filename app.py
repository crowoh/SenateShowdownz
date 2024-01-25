from flask import Flask, render_template, request
import api_handler
import data_processor

app = Flask(__name__)

# Set load_all_data to True to load all available data, even if some data is missing.
# Set it to False to skip legislators with missing data.
load_all_data = False  # Toggle this variable as needed

@app.route('/')
def index():
    state_to_process = request.args.get('state', 'CA')
    legislators_data = {}
    legislators_xml = api_handler.get_legislators(state_to_process)
    
    if legislators_xml:
        legislators = legislators_xml.findall(".//legislator")[:10]
        for legislator in legislators:
            cid = legislator.get('cid')
            if not cid:
                continue  # Skip if cid is not available

            senator_name = legislator.get('firstlast')
            party = legislator.get('party', 'N/A')
            congress_office = legislator.get('congress_office', 'N/A')
            first_elected = legislator.get('firstelectoff', 'N/A')
            phone = legislator.get('phone', 'N/A')
            website = legislator.get('website', 'N/A')
            webform = legislator.get('webform', 'N/A')

            industry_xml_data = api_handler.get_opensecrets_data(cid, "2020")
            if not load_all_data and not industry_xml_data:
                continue  # Skip this legislator if essential data is missing and load_all_data is False

            formatted_contributions = "No industry data available"
            if industry_xml_data:
                formatted_contributions = data_processor.process_opensecrets_data(industry_xml_data)

            contrib_xml_data = api_handler.get_cand_contrib_data(cid, "2020")
            formatted_contributors = "No contributor data available"
            if contrib_xml_data:
                formatted_contributors = data_processor.format_contributors(contrib_xml_data.findall('.//contributor'))

            legislators_data[senator_name] = {
                "party": party,
                "congress_office": congress_office,
                "first_elected": first_elected,
                "phone": phone,
                "website": website,
                "webform": webform,
                "contributions": formatted_contributions,
                "contributors": formatted_contributors
            }

    return render_template('index.html', legislators=legislators_data)

if __name__ == '__main__':
    app.run(debug=True)
