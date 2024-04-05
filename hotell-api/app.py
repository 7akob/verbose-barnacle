import os, psycopg
from psycopg.rows import dict_row
from flask import Flask
from flask_cors import CORS 
from flask import request
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

PORT=8332 #Jakobs port

dburl = os.environ.get("DB_URL")

print(dburl)

conn = psycopg.connect(dburl, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

rooms = [
    {'number': 101, 'type': "single"},
    {'number': 202, 'type': "double"},
    {'number': 303, 'type': "single"}
]

@app.route("/test")
def dbtest():
    with conn.cursor() as cur:
        cur.execute("SELECT * from people")
        rows = cur.fetchall()
        return rows


@app.route("/")
def info():
    return "Hotel API, endpoints / rooms / bookings"


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endpoint(): #Fixa till /rooms-endpointen så den hämtar rumslistan från databasen
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        rooms.append(request_body)
        return {
        'msg': f"Du har skapat nytt rum, id:{len(rooms)-1}",
    } 
    else:
        return rooms
    
@app.route("/bookings")
def bookings_endpoint():
    return 0 #Fixa till /bookings-endpointen så den kan spara en bokning i databasen


    
@app.route("/rooms/<int:id>", methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def one_room_endpoint():
    if request.method == 'GET':
        return rooms[id]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
