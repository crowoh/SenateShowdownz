from flask import Flask, render_template, request
import api_handler
import data_processor

app = Flask(__name__)

@app.route('/')
def index():
    state_to_process = request.args.get('state', 'CA')
    legislators_data = {}
    legislators_xml = api_handler.get_legislators(state_to_process)
    
    if legislators_xml:
        legislators = legislators_xml.findall(".//legislator")[:10]
        for legislator in legislators:
            cid = legislator.get('cid')
            senator_name = legislator.get('firstlast')
            party = legislator.get('party', 'N/A')
            congress_office = legislator.get('congress_office', 'N/A')
            first_elected = legislator.get('firstelectoff', 'N/A')
            phone = legislator.get('phone', 'N/A')
            website = legislator.get('website', 'N/A')

            if cid:
                industry_xml_data = api_handler.get_opensecrets_data(cid, "2020")
                formatted_contributions = data_processor.process_opensecrets_data(industry_xml_data) if industry_xml_data else "No industry data available"

                contrib_xml_data = api_handler.get_cand_contrib_data(cid, "2020")
                if contrib_xml_data:
                    contributors = contrib_xml_data.findall('.//contributor')
                    formatted_contributors = data_processor.format_contributors(contributors)
                else:
                    formatted_contributors = "No contributor data available"

                legislators_data[senator_name] = {
                    "party": party,
                    "congress_office": congress_office,
                    "first_elected": first_elected,
                    "phone": phone,
                    "website": website,
                    "contributions": formatted_contributions,
                    "contributors": formatted_contributors
                }

    return render_template('index.html', legislators=legislators_data)

if __name__ == '__main__':
    app.run(debug=True)
