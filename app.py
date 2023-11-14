
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="op360",
    database="flight_data"
)

cur = db.cursor()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    cur.execute("select * from airport")
    airports = cur.fetchall()
    airport = []

    for i in airports:
        airport.append([i[0], i[1]])
    
    if request.method == "GET":
        available="Start"
        return render_template("search.html", airports=airport, available=available)
    else:
        data = request.form
        origin = data['origin']
        destination = data['destination']
        cur.execute(f"select type from can_land where code='{origin}' INTERSECT select type from can_land where code='{destination}'")
        plane = cur.fetchall()

        if len(plane) > 0:
            available = []
            for type in plane:
                cur.execute(f"select id, num_of_seats from airplane where type='{type[0]}' UNION select company,fare from airplane_type where type='{type[0]}'")
                result = cur.fetchall()
                company = result.pop()
                for i in result:
                    available.append([i,company])
        else:
            available = "Not Found"
            
        print(available)
        return render_template("search.html", airports=airport, available=available)

@app.route("/book", methods=['POST', 'GET'])
def book():
    if request.method == "GET":
        return render_template("book.html")
    else:
        data = request.form
        name = data["name"]
        number = data["number"]
        pid = data["id"]
        email = data["email"]
        date = data["date"]

        cur.execute(f"select * from airplane where id = {pid}")
        result = cur.fetchall() 
        num_seats = result[0][1]
        plane_type = result[0][2] 

        cur.execute(f"select company,fare from airplane_type where type = '{plane_type}'")
        result = cur.fetchall()
        company = result[0][0]
        fare = result[0][1]

        personal_details = [name, number, email, date]
        flight_details = [pid, num_seats, company, fare]
        details = [personal_details, flight_details]
        return render_template("details.html", details=details)

if __name__ == '__main__':
    app.run(debug=True, port=5000)