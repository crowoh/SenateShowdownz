from flask import Flask, render_template, request
import api_handler
import data_processor

app = Flask(__name__)

@app.route('/')
def index():
    state_to_process = request.args.get('state', 'CA')
    legislators_data = {}
    legislators_xml = api_handler.get_legislators(state_to_process)
    independent_expenditures = data_processor.process_independent_expenditures_data()

    if legislators_xml:
        legislators = legislators_xml.findall(".//legislator")[:10]
        for legislator in legislators:
            cid = legislator.get('cid')
            if not cid:
                continue  # Skip if cid is not available

            # Fetch and process candSummary data
            cand_summary_xml_data = api_handler.get_cand_summary_data(cid)
            formatted_cand_summary = {"error": "No summary data available"}  # Default value as a dictionary
            if cand_summary_xml_data is not None:
                formatted_cand_summary = data_processor.process_cand_summary_data(cand_summary_xml_data)
                # Ensure the formatted_cand_summary is a dictionary or convert it if necessary

            senator_name = legislator.get('firstlast')
            party = legislator.get('party', 'N/A')
            congress_office = legislator.get('congress_office', 'N/A')
            first_elected = legislator.get('firstelectoff', 'N/A')
            phone = legislator.get('phone', 'N/A')
            website = legislator.get('website', 'N/A')
            webform = legislator.get('webform', 'N/A')

            industry_xml_data = api_handler.get_opensecrets_data(cid, "2020")
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
                "contributors": formatted_contributors,
                "cand_summary": formatted_cand_summary  # Ensure this key is always present
            }

    return render_template('index.html', legislators=legislators_data, independent_expenditures=independent_expenditures)

if __name__ == '__main__':
    app.run(debug=True)
