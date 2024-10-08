import json
from flask import request, Flask, render_template, jsonify
from CollegexTinder.CollegeTinder import CollegeTinder
import csv
CT = CollegeTinder(0.01)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/main_form')
def main_form():
    return render_template('main_form.html')

@app.route('/WRITE_DB')
def save_data():
    return render_template('save_user_data.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    input_vector = list(result.values())
    print(input_vector) # This is the output that was stored in the JSON within the browser
    rank = CT.run(input_vector)
    similar_colleges = CT.other_colleges(rank)
    return json.dumps({'status':'OK','rank':rank, 'list':similar_colleges});


@app.route('/write_to_db', methods=['POST'])
def write():
    output = request.get_json()
    result = json.loads(output)
    user_inputs = list(result.values())
    with open ("CollegexTinder\\csv\\USER_DATA.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(user_inputs)
    
    return json.dumps({'status':'OK','code':200});


if __name__ == "__main__":
    app.run(debug=True)

