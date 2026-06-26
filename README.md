# 🐙 GitHub Analyzer

A Flask-based web application that analyzes GitHub profiles and generates developer insights.

## 🚀 Features

- 🔐 User Registration & Login System
- 👤 GitHub Profile Analyzer
- 📊 Developer Score Calculation
- 🏆 Top Developer Leaderboard
- 💻 Programming Language Detection
- 🤖 AI-based Suggestions
- 📄 Download GitHub Report as PDF

---

## 🖥️ Project Preview

GitHub Analyzer helps recruiters and developers quickly understand GitHub activity.

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- SQLite
- GitHub REST API

### Frontend
- HTML
- CSS
- Jinja Templates

### Libraries

- Flask-Bcrypt
- Flask-Login
- Requests
- ReportLab

---

## 📂 Project Structure

```
Github-Analyzer/

│── app.py
│── requirements.txt
│── README.md
│── .gitignore

│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── report.html
│
├── static/
│   └── style.css
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Dhanu-05685/GA.git
```

Go inside project:

```bash
cd GA
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

Start Flask server:

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 🔑 Login System

Users can:

- Create account
- Login securely
- Analyze GitHub profiles

Passwords are encrypted using:

```
Flask-Bcrypt
```

---

## 📊 GitHub Analysis

The application fetches:

- Username
- Bio
- Location
- Company
- Repositories
- Followers
- Languages

using GitHub API.

---

## 📈 Developer Score

Score is calculated using:

```
Repositories × 8
+
Followers × 2
```

Maximum score:

```
100%
```

---

## 📄 PDF Report

Users can download their GitHub analysis report.

Generated using:

```
ReportLab
```

---

## 🔒 Security

Ignored files:

```
.venv/
firebase_key.json
database.db
*.pdf
```

---

## 👨‍💻 Author

**Dhanu-05685**

GitHub:

https://github.com/Dhanu-05685

---

⭐ If you like this project, give it a star!
