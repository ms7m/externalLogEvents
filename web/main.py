import requests
from flask import Flask
from waitress import serve

from flask import render_template
app = Flask(__name__)
app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True



@app.route('/load/logs', methods=["GET"])
def load_devices():
    try:
        r = requests.get('http://localhost:8080/logs/all/load?flag=show-all').json()
        print(len(r['output']))
        r['output'].reverse()
    except Exception as error:
        print('idk')

    return render_template('all_logs.html', logs=r['output'])

@app.route('/load/latest/log', methods=['GET'])
def load_log():
    try:
        r = requests.get('http://localhost:8080/logs/latest/one').json()
        return render_template('latest_log.html', log=r)
    except Exception as error:
        print('errororor')

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')
serve(app, port=3003)