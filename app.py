import json
from flask import request, Flask, render_template, jsonify
from CollegexTinder.CollegeTinder import CollegeTinder
import csv
CT = CollegeTinder(0.01)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/tester')
def tester():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_func():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    input_vector = list(result.values())
    print(input_vector) # This is the output that was stored in the JSON within the browser
    rank = CT.run(input_vector)
    print(rank)
    return json.dumps({'status':'OK','rank':rank});


@app.route('/write_to_db', methods=['POST'])
def write():
    output = request.get_json()
    result = json.loads(output)
    user_inputs = list(result.values())
    print(user_inputs)
    with open ("CollegexTinder\\csv\\USER_DATA.csv", "r+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(user_inputs)
    
    return json.dumps({'status':'OK','rank':'testtesttest'});


if __name__ == "__main__":
    app.run(debug=True)

