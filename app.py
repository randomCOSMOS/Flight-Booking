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


if __name__ == '__main__':
    app.run(debug=True, port=3000)