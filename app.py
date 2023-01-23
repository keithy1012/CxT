import json
from flask import request, Flask, render_template, jsonify
from CollegexTinder.CollegeTinder import CollegeTinder
CT = CollegeTinder(0.01)

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to My Website!"


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
    return json.dumps({'status':'OK','rank':'testtesttest'});


if __name__ == "__main__":
    app.run(debug=True)

