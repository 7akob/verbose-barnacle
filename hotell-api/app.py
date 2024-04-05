from flask import Flask
from flask_cors import CORS 
from flask import request
from flask import jsonify

PORT=8332 #Jakobs port

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

rooms = [
    {'number': 101, 'type': "single"},
    {'number': 202, 'type': "double"},
    {'number': 303, 'type': "single"}
]

@app.route("/")
def main():
    return "Hotel API, endpoints / rooms / bookings"


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endpoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        rooms.append(request_body)
        return {
        'msg': f"Du har skapat nytt rum, id:{len(rooms)-1}",
    } 
    else:
        return rooms


    
@app.route("/rooms/<int:id>", methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def one_room_endpoint():
    if request.method == 'GET':
        return rooms[id]

@app.route("/get_my_ip")
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
