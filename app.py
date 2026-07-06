from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import joblib

app = Flask(__name__)
app.secret_key = "secret123"

model = joblib.load("credit_model.pkl")

# ---------------- USERS (temporary memory storage) ----------------
users = {
    "admin": "admin123"
}

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users[username] = password
        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- DASHBOARD (PROTECTED) ----------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/predict-page")
def predict_page():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", user=session["user"])


# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    data = [
        float(request.form["laufkont"]),
        float(request.form["laufzeit"]),
        float(request.form["moral"]),
        float(request.form["verw"]),
        float(request.form["hoehe"]),
        float(request.form["sparkont"]),
        float(request.form["beszeit"]),
        float(request.form["rate"]),
        float(request.form["famges"]),
        float(request.form["buerge"]),
        float(request.form["wohnzeit"]),
        float(request.form["verm"]),
        float(request.form["alter"]),
        float(request.form["weitkred"]),
        float(request.form["wohn"]),
        float(request.form["bishkred"]),
        float(request.form["beruf"]),
        float(request.form["pers"]),
        float(request.form["telef"]),
        float(request.form["gastarb"])
    ]

    input_data = pd.DataFrame([data])
    input_data = pd.DataFrame([data])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        result = "🟢 GOOD CREDIT"
        explanation = "Low risk profile, stable financial behavior."
        score=82
        loan="Eligible for loan"
    else:
        result = "🔴 BAD CREDIT"
        explanation = "High risk financial behavior detected."
        score=38
        loan="Not Eligble for loan"

    return render_template(
        "index.html",
        prediction=result,
        explanation=explanation,
        score=score,
        loan=loan,
        user=session["user"]
    )

if __name__ == "__main__":
    app.run( debug=True)