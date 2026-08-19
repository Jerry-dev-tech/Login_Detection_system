from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import pandas as pd
import joblib
import sqlite3
import os

from datetime import datetime

# =====================================
# APP CONFIGURATION
# =====================================

app = Flask(__name__)

app.secret_key = "login_anomaly_secret_key"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================================
# LOAD RANDOM FOREST MODEL
# =====================================

model = joblib.load("models/model.pkl")

with open("models/accuracy.txt", "r") as f:
    model_accuracy = f.read().strip()

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("Dataset/login_data.csv")

df["Hour"] = (
    df["Login_Time"]
    .str.split(":")
    .str[0]
    .astype(int)
)

# =====================================
# SHARED DASHBOARD DATA
# =====================================

def get_dashboard_data():

    global df

    total_logins = len(df)

    suspicious_logins = len(
        df[df["Suspicious"] == 1]
    )

    failed_logins = len(
        df[df["Login_Success"] == 0]
    )

    success_rate = round(

        (
            len(df[df["Login_Success"] == 1])
            / total_logins

        ) * 100,

        2

    )

    # Hour Chart

    hour_counts = (

        df["Hour"]

        .value_counts()

        .sort_index()

    )

    hour_labels = [

        int(x)

        for x in hour_counts.index.tolist()

    ]

    hour_values = [

        int(x)

        for x in hour_counts.values.tolist()

    ]

    # Pie Chart

    normal_count = len(

        df[df["Suspicious"] == 0]

    )

    suspicious_count = len(

        df[df["Suspicious"] == 1]

    )

    # Country Chart

    country_counts = (

        df["Country"]

        .value_counts()

    )

    country_labels = country_counts.index.tolist()

    country_values = [

        int(x)

        for x in country_counts.values.tolist()

    ]

    # Recent Logins

    recent_logins = (

        df.tail(15)

        .to_dict(

            orient="records"

        )

    )

    return {

        "total_logins": total_logins,

        "suspicious_logins": suspicious_logins,

        "failed_logins": failed_logins,

        "success_rate": success_rate,

        "model_accuracy": model_accuracy,

        "hour_labels": hour_labels,

        "hour_values": hour_values,

        "normal_count": normal_count,

        "suspicious_count": suspicious_count,

        "country_labels": country_labels,

        "country_values": country_values,

        "recent_logins": recent_logins

    }

# =====================================
# LOGIN
# =====================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        connection = sqlite3.connect(
            "login_system.db"
        )

        cursor = connection.cursor()

        cursor.execute(

            "SELECT * FROM admin WHERE username=? AND password=?",

            (

                username,

                password

            )

        )

        admin = cursor.fetchone()

        connection.close()

        if admin:

            session["logged_in"] = True

            return redirect(

                url_for("dashboard")

            )

        return render_template(

            "login.html",

            error="Invalid Username or Password"

        )

    return render_template(

        "login.html"

    )
# =====================================
# DASHBOARD
# =====================================

@app.route("/")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = get_dashboard_data()

    prediction_result = ""

    if request.method == "POST":

        hour = int(request.form["hour"])

        login_success = int(request.form["login_success"])

        failed_attempts = int(request.form["failed_attempts"])

        country = request.form["country"]

        device = request.form["device"]

        night_login = 1 if hour < 5 else 0

        country_risk = {

            "India":0,
            "USA":0,
            "UK":0,
            "Russia":1,
            "China":1

        }

        device_risk = {

            "Laptop":0,
            "Desktop":0,
            "Mobile":0,
            "Unknown":1

        }

        prediction = model.predict([[

            hour,

            night_login,

            login_success,

            failed_attempts,

            country_risk[country],

            device_risk[device]

        ]])

        risk_score = (

            night_login

            + failed_attempts

            + country_risk[country]

            + device_risk[device]

        )

        if risk_score <= 1:

            risk_level = "LOW"

        elif risk_score <= 3:

            risk_level = "MEDIUM"

        else:

            risk_level = "HIGH"

        if prediction[0] == 1:

            prediction_result = (

                f"⚠ Suspicious Login | "

                f"Risk Score: {risk_score} | "

                f"Risk Level: {risk_level}"

            )

        else:

            prediction_result = (

                f"✅ Normal Login | "

                f"Risk Score: {risk_score} | "

                f"Risk Level: {risk_level}"

            )

    data["prediction_result"] = prediction_result

    return render_template(

        "dashboard.html",

        **data

    )


# =====================================
# ANALYTICS
# =====================================

@app.route("/analytics")
def analytics():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = get_dashboard_data()

    return render_template(

        "analytics.html",

        **data

    )


# =====================================
# LOGIN HISTORY
# =====================================

@app.route("/history")
def history():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = get_dashboard_data()

    history_df = df.copy()

    search = request.args.get("search", "")

    country = request.args.get("country", "")

    status = request.args.get("status", "")

    if search:

        history_df = history_df[

            history_df["Username"]

            .str.contains(

                search,

                case=False,

                na=False

            )

        ]

    if country:

        history_df = history_df[

            history_df["Country"] == country

        ]

    if status:

        history_df = history_df[

            history_df["Login_Success"] == int(status)

        ]

    data["recent_logins"] = (

        history_df

        .sort_values(

            by="Login_Date",

            ascending=False

        )

        .to_dict(

            orient="records"

        )

    )

    return render_template(

        "history.html",

        **data

    )


# =====================================
# UPLOAD LOGS
# =====================================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    results = None

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filepath = os.path.join(

                app.config["UPLOAD_FOLDER"],

                file.filename

            )

            file.save(filepath)

            data = pd.read_csv(filepath)

            data["Hour"] = (

                data["Login_Time"]

                .str.split(":")

                .str[0]

                .astype(int)

            )

            data["Night_Login"] = (

                data["Hour"] < 5

            ).astype(int)

            country_risk = {

                "India":0,
                "USA":0,
                "UK":0,
                "Russia":1,
                "China":1

            }

            device_risk = {

                "Laptop":0,
                "Desktop":0,
                "Mobile":0,
                "Unknown":1

            }

            data["Country_Risk"] = data["Country"].map(country_risk)

            data["Device_Risk"] = data["Device"].map(device_risk)

            features = data[[

                "Hour",

                "Night_Login",

                "Login_Success",

                "Failed_Attempts",

                "Country_Risk",

                "Device_Risk"

            ]]

            predictions = model.predict(features)

            data["Prediction"] = predictions

            risk = []

            for i in range(len(data)):

                score = (

                    data.loc[i, "Night_Login"]

                    + data.loc[i, "Failed_Attempts"]

                    + data.loc[i, "Country_Risk"]

                    + data.loc[i, "Device_Risk"]

                )

                if score <= 1:

                    risk.append("LOW")

                elif score <= 3:

                    risk.append("MEDIUM")

                else:

                    risk.append("HIGH")

            data["Risk_Level"] = risk

            results = data.to_dict(

                orient="records"

            )

    return render_template(

        "upload.html",

        results=results

    )
# =====================================
# REPORTS
# =====================================

@app.route("/reports")
def reports():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = get_dashboard_data()

    return render_template(
        "reports.html",
        **data
    )


# =====================================
# SETTINGS
# =====================================

@app.route("/settings")
def settings():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(

        "settings.html",

        model_accuracy=model_accuracy,

        current_time=datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    )


# =====================================
# LOGOUT
# =====================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =====================================
# ERROR PAGE
# =====================================

@app.errorhandler(404)
def page_not_found(error):

    return (

        "<h2>404 - Page Not Found</h2>",

        404

    )


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )