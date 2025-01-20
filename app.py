from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import password_strength_detector
from groq_api import GroqClient
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY_SURVEY_MONKEY")
CLIENT_ID = os.getenv("API_CLIENT_ID_SURVEY_MONKEY")


user_info = {"username": "", "password": "", "email": ""}
groq_client = GroqClient()

# Setup Flask secret key and SQLAlchemy database URI
app.secret_key = "secret_key_for_flash_messages"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locksmith.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the BreachedData model (Table 1)
class BreachedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<BreachedData {self.url}>'

# Define the UserInfo model (Table 2)
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<UserInfo {self.username}>'

# Create tables before the first request
@app.before_request
def create_tables():
    db.create_all()

# Define the home page route
@app.route("/")
def index_page():  # Renamed to avoid conflict with /login.html
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Query using filter_by to find a specific entry by username
    user = UserInfo.query.filter_by(username=username).first()
    
    # Check if user exists and the password matches
    if user:
        if user.password == password:
            # If password matches, save user info and redirect
            user_info["username"] = username
            user_info["password"] = password
            return redirect(url_for("home_page"))
        else:
            # If password does not match
            error = "Wrong password, try contacting support from top (we are case sensitive)"
            return render_template("index.html", error=error)
    else:
        # If username does not exist
        error = "Username not found, try making an account (we are case sensitive)"
        return render_template("index.html", error=error)

    
@app.route("/homepage.html/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        username = request.form.get("username")  
        password = request.form.get("password")

        # Store the username and password
        user_info["username"] = username
        user_info["password"] = password

        # Redirect to the groq page for password evaluation
        return redirect(url_for("groq_page"))

    return render_template("homepage.html")


@app.route("/about.html/")
def about_page():
    return render_template("about.html")

@app.route("/contact.html/")
def contact_page():
    feedback_form_url = "https://www.surveymonkey.com/r/L7VQ9SG"
    return render_template("contact.html", feedback_form_url=feedback_form_url)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Check if the username or email already exists in the database
        existing_user = UserInfo.query.filter_by(username=username).first()
        existing_email = UserInfo.query.filter_by(email=email).first()

        if existing_user:
            error = "Username already exists. Please choose another one."
            return render_template("register.html", error=error)

        if existing_email:
            error = "Email already exists. Please choose another one."
            return render_template("register.html", error=error)

        # If username and email are unique, save to the database
        new_user = UserInfo(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to homepage after successful registration
        return redirect(url_for("home_page"))

    return render_template("register.html")

@app.route("/login.html")
def login_page():
    return render_template("login.html")

# Example of adding BreachedData and UserInfo records
@app.route("/add_data", methods=["GET"])
def add_data():
    # Example of adding BreachedData and UserInfo records
    new_breached_data = BreachedData(
        url="https://example.com",
        username="example_user",
        password="example_pass",
        port=8080,
        ip_address="192.168.0.1"
    )
    new_user_info = UserInfo(
        email="user@example.com",
        username="example_user",
        password="example_pass"
    )
    
    # Add data to the session
    db.session.add(new_breached_data)
    db.session.add(new_user_info)
    
    # Commit the session to the database
    db.session.commit()

    return "Data added to the database!"

@app.route("/view_users", methods=["GET"])
def view_users():
    """Fetch and display all records from the UserInfo table."""

    # new_user_info = UserInfo(
    #     email="user@example.com",
    #     username="example_user",
    #     password="example_pass"
    # )
    
    # # Add data to the session
    # db.session.add(new_user_info)
    
    # # Commit the session to the database
    # db.session.commit()

    all_users = UserInfo.query.all()  # Get all records from UserInfo table
    
    if not all_users:
        return "No records found in the UserInfo table."
    
    # Render a template to display the data (or return raw HTML for simplicity)
    return render_template("view_users.html", users=all_users)



@app.route("/retrieve_feedback", methods=["GET"])
def retrieve_feedback():
    client = requests.session()
    survey_id = "L7VQ9SG"
    url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/responses/bulk"
    headers = {
        "Authorization": "Bearer " + CLIENT_ID,
        "Content-Type": "application/json",
    }

    
    params = {
        "api_key": API_KEY,
    }
    response = client.get(url, headers=headers, params=params)

    if response.status_code == 200:
        feedback_data = response.json()
        print(feedback_data)
        return render_template("feedback-results.html", feedback=feedback_data)
    else:
        flash("Failed to retrieve feedback responses.", "danger")
        return redirect(url_for("contact_page"))


@app.route("/groq.html/")
@app.route("/groq.html/")
def groq_page():
    # Get the username and password from user_info
    username = user_info.get("username", "")
    password = user_info.get("password", "")

    # Get password strength from both methods
    password_strength_rfc = password_strength_detector.get_password_strength(password)
    password_strength_gronq = groq_client.get_password_strength(password)

    # Calculate the average password strength
    average_password_strength = (password_strength_rfc + password_strength_gronq) / 2

    # Get password critique and better password suggestions
    reason = groq_client.critique_password(password)
    better_passwords = groq_client.create_new_password(password, iterations=3)

    # Render the groq page and pass the results for display
    return render_template("groq.html", 
                           username=username, 
                           password=password,
                           password_strength_rfc=password_strength_rfc,
                           password_strength_gronq=password_strength_gronq,
                           average_password_strength=average_password_strength,
                           reason=reason, 
                           better_passwords=better_passwords)
@app.route("/contact_for_password.html/")
def reset_password():
    return render_template("contact_for_password.html")

@app.route("/dataleaks.html/")
def Dataleaks_page():
    return render_template("dataleaks.html")

if __name__ == "__main__":
    print("Starting the Flask application...")
    app.run(debug=True)