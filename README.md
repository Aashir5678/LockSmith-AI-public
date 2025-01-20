# LockSmithAI


A password strength and breach detection web application developed for the seventh UottaHack hackathon by first-year Computer Engineering students from the University of Ottawa.

Team members:

[Rayyan Lodhi](https://www.linkedin.com/in/rayyan-lodhi-002bab1a4/)

[Agam Singh](https://www.linkedin.com/in/agamsinghuottawa/)

[Pradyumna Uppalapati](https://www.linkedin.com/in/pradyumna0806/)

[Aashir Alam](https://www.linkedin.com/in/aashir-alam-465532222/)


# About the Project

LockedSmithAI is a password analysis and breach detection platform that evaluates password strength, detects vulnerabilities, and provides solutions for enhancing user security. The platform also checks for breached accounts and integrates seamlessly with SurveyMonkey to collect user feedback.

A password strength detector / breach detector web app, made using Python Flask. This project uses the sklearn machine learning library and the Gronq API to score how secure a password is out of 10, gives a reason for the scoring, then it shows 3 possible stronger passwords similar to the one given. Then the user can see if a certain website, password or username has been breached. Also makes use of the SurveyMonkey API for the Contact Us page. User information is stored in a SqlLite database, along witih breached user data, which includes url, username, password, ip address, and login. Includes login features.

# Key Features

**1. Password Strength Analysis**
- Scores password strength on a scale of 1-10.
- Provides insights and reasoning for the assigned score.
- Suggests three stronger alternatives for insecure passwords.
- Machine learning-powered using sklearn.
  
**2. Breach Detection**
- Checks for breached usernames, passwords, and websites.
- Breached data includes:
- URLs
- Usernames
- Passwords
- IP Addresses
- Login Timestamps
  
**3. SurveyMonkey Integration**
- Interactive "Contact Us" page for user feedback.
- Animated lock-themed interface with audio and visuals.
- Uses the SurveyMonkey API for seamless survey submissions.
  
**4. Database Integration**
- User data is securely stored using SQLite.
-Breached user data is managed for real-time checks.

# Technology Stack

**Back-End**
- Python Flask framework
- SQLite database for data storage
- Gronq API for breach detection and machine learning scoring
  
**Front-End**
- HTML5, CSS3, JavaScript
- Dynamic visuals using GIFs and sound effects
- Fully responsive design

**APIs & Libraries**
- SurveyMonkey API: For user surveys
- Gronq API: For password strength analysis
- sklearn: Machine learning library

# Project Structure
```

LockSmithAI/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Main stylesheet
│   │   ├── images/
│   │   │   ├── background_for_Ottahack7.avif
│   │   │   ├── lock-static.png
│   │   │   └── lock-unlock.gif
│   │   ├── javascript/
│   │   │   └── app.js             # Main JavaScript file
│   │   └── sounds/
│   │       └── unlock.mp3         # Sound effect for unlocking
│   ├── templates/
│   │   ├── base.html              # Base template
│   │   ├── contact.html           # Contact Us page
│   │   ├── about.html             # About LockSmith AI page
│   │   └── home.html              # Homepage
│   ├── init.py                # Initialize the Flask app
│   ├── routes.py                  # Define application routes
│   └── forms.py                   # Define form classes (if using Flask-WTF)
├── tests/
│   ├── test_routes.py             # Tests for application routes
│   └── test_forms.py              # Tests for form validations
├── venv/                          # Virtual environment directory
├── .gitignore                     # Git ignore file
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
└── run.py                         # Entry point to run the Flask application
```

# Installation Guide

1. Clone the repository:
```
git clone https://github.com/your-repository/LockSmithAI.git
```

2. Navigate to the project directory:
```
cd LockSmithAI 
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Access the web app at https://locksmith-ai.onrender.com/

# License

This project is licensed under the MIT License - see the LICENSE file for details.
