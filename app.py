from flask import Flask, render_template
import api_handler
import data_processor

app = Flask(__name__)

@app.route('/')
def index():
    committee_names_data = api_handler.get_committee_names()
    all_senators_data = {}
    if committee_names_data:
        for committee in committee_names_data.get('results', []):
            cid = committee.get('id')
            if cid:
                xml_data = api_handler.get_opensecrets_data(cid, "2020")
                if xml_data:
                    senator_data = data_processor.process_opensecrets_data(xml_data)
                    all_senators_data.update(senator_data)
    return render_template('index.html', data=all_senators_data)

if __name__ == '__main__':
    app.run(debug=True)
