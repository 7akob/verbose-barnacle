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

conn = psycopg.connect(dburl, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

roomsTEMP = [
    {'number': 101, 'type': "single"},
    {'number': 202, 'type': "double"},
    {'number': 303, 'type': "single"}
]


@app.route("/")
def info():
    return "Hotel API, endpoints /rooms /bookings"


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endpoint(): #Fixa till /rooms-endpointen så den hämtar rumslistan från databasen
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        roomsTEMP.append(request_body)
        return {
        'msg': f"Du har skapat nytt rum, id:{len(roomsTEMP)-1}!",
    } 
    else:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM hotel_room ORDER BY room_number")
            return cur.fetchall()
    
@app.route("/bookings", methods=['GET', 'POST'])
def bookings():
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""SELECT *
                        FROM hotel_booking
                        ORDER BY datefrom 
                        """)
            return cur.fetchall()
        
    if request.method == 'POST':
        body = request.get_json()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO hotel_booking (
                    room_id, 
                    guest_id,
                    datefrom
                ) VALUES (
                    %s, 
                    %s, 
                    %s
                ) RETURNING id""", [ 
                body['room'], 
                body['guest'], 
                body['datefrom'] 
            ])
            result = cur.fetchone()
        return {"msg": "Du har bokat ett rum", "result": result}



    
@app.route("/rooms/<int:id>", methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def one_room_endpoint(id):
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT *
                        FROM hotel_room
                        WHERE is ? %s""", [id])
            return cur.fetchone()



@app.route("/guests", methods=['GET'])
def guests_endpoint(): 
    with conn.cursor() as cur:
        cur.execute("""SELECT hotel_guest.*, COALESCE(visit_count, 0) AS visit_count
                    FROM hotel_guest
                    LEFT JOIN (
                        SELECT guest_id, COUNT(*) AS visit_count
                        FROM hotel_booking
                        GROUP BY guest_id
                    ) AS guest_visits ON hotel_guest.id = guest_visits.guest_id
                    ORDER BY hotel_guest.firstname
                    """)
        return cur.fetchall()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))