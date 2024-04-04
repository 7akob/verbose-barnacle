from flask import Flask
from flask_cors import CORS 
from flask import request
from flask import jsonify

PORT=8332 #Jakobs port

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

@app.route("/", methods=['GET', 'POST'])
def hello():
    return {
        'greeting': "Hello, Flask-JSON",
        'method': request.method
    }

@app.route("/")

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        #skapa rad i databasen, returnera ny id..
        new_id = 555
        return {
        'msg': f"Du har skapat ny rad i databasen, id är:{new_id}",
        'method': request.method
    }


    
@app.route("/test/<int:id>", methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def testID():
    if request.method == 'GET':
        return {
        'msg': f"du requestade id: {id}",
        'method': request.method
        }
    if request.method == 'PUT' or request.method == 'PATCH':
        return {
        'msg': f"du uppdaterar id: {id}",
        'method': request.method
        }
    if request.method == 'DELETE':
        return {
        'msg': f"du har raderat {id}",
        'method': request.method
    }

@app.route("/get_my_ip")
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
