#  Smart Leave Approval System

The **Smart Leave Approval System** is a web-based application designed to automate and streamline the leave management process in an organization. It enables employees to apply for leave online, allows managers and administrators to approve or reject requests, and integrates an **AI-based recommendation system** to assist in decision-making.

---

##  Table of Contents

1. Project Overview
2. Features
3. Technology Stack
4. System Architecture
5. Project Structure
6. Installation & Setup
7. Running the Application
8. Machine Learning Module
9. Email Configuration
10. Usage Guide
11. Screenshots
12. Security Considerations
13. Limitations
14. Future Enhancements
15. License

---

##  1. Project Overview

Traditional leave management systems rely on manual processes or basic digital tools, leading to inefficiencies and lack of transparency.
The **Smart Leave Approval System** offers a centralized, automated, and intelligent platform for managing employee leave requests.

An AI-based recommendation engine analyzes historical leave data and provides approval suggestions while keeping the **final decision under human control**.

---

##  2. Features

* Role-based Authentication (Employee / Manager / Admin)
* Online Leave Application & Tracking
* AI-based Leave Approval Recommendation
* Manager Approval / Rejection Workflow
* Admin User & Role Management
* Automated Email Notifications
* Leave Reports & History
* Secure Session Management

---

##  3. Technology Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* Tailwind CSS
* JavaScript

### Database

* SQLite
* SQLAlchemy ORM

### Machine Learning

* Random Forest Algorithm
* Scikit-learn
* Pandas, NumPy

### Other Tools

* Flask-Mail
* Joblib
* Visual Studio Code

---

##  4. System Architecture

The system follows a **Layered / MVC-based Architecture**:

* **Presentation Layer:** HTML templates (UI)
* **Application Layer:** Flask Controllers & Business Logic
* **AI Layer:** ML Model for Recommendation
* **Data Layer:** SQLite Database
* **Notification Layer:** Email Service

---

##  5. Project Structure

```
Smart-Leave-Approval-System/
│
├── app.py
├── config.py
├── ai_predictor.py
├── train_model.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── apply_leave.html
│   ├── admin_dashboard.html
│   ├── change_password.html
│   ├── reports.html
│   └── status_update.html
│
├── static/
│   ├── style.css
│   └── images/
│
└── README.md
```

---

##  6. Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/smart-leave-approval-system.git
cd smart-leave-approval-system
```

---

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  7. Running the Application

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/
```

---

##  8. Machine Learning Module

* The AI model is trained using **Random Forest Classifier**
* Training script: `train_model.py`
* Model predicts leave approval probability based on:

  * Department
  * Role
  * Leave Duration
  * Previous Leaves
  * Team Availability

To retrain the model:

```bash
python train_model.py
```

>  AI only **assists**, final approval is always manual.

---

##  9. Email Configuration

Update SMTP details in `config.py`:

```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your_email@gmail.com'
MAIL_PASSWORD = 'your_app_password'
```

Emails are sent for:

* Leave submission
* Leave approval
* Leave rejection

---

##  10. Usage Guide

### Employee

* Register / Login
* Apply for leave
* View leave status and history

### Manager

* View pending leave requests
* See AI recommendation
* Approve / Reject leave

### Admin

* Manage users and roles
* View all leave requests
* Generate reports

---

##  11. Screenshots

Screenshots of:

* Login Page
* Dashboard
* Apply Leave
* Manager Approval
* AI Recommendation
* Status Update

<img width="944" height="533" alt="image" src="https://github.com/user-attachments/assets/fd305245-bb98-4879-9703-9d44c1901a1f" />
<img width="965" height="549" alt="image" src="https://github.com/user-attachments/assets/26ddf272-d5be-4601-a90c-16effe593053" />
<img width="940" height="518" alt="image" src="https://github.com/user-attachments/assets/186ec144-79bf-4614-b1ef-3b09dd5edf1d" />
<img width="953" height="527" alt="image" src="https://github.com/user-attachments/assets/26a762bd-1027-40db-a173-436f4e5b8f01" />
<img width="984" height="520" alt="image" src="https://github.com/user-attachments/assets/f20f2294-c6b0-4952-9359-b90d972835af" />
<img width="984" height="558" alt="image" src="https://github.com/user-attachments/assets/15b50555-cc82-4056-b2f7-57a21fc7ac1b" />
<img width="960" height="507" alt="image" src="https://github.com/user-attachments/assets/9888f8ed-ca73-4818-b754-b352300b293b" />
<img width="982" height="501" alt="image" src="https://github.com/user-attachments/assets/78fe7490-c06e-4782-bdd1-b45543b2edbd" />

---

## 🔐 12. Security Considerations

* Session-based Authentication
* Role-based Access Control
* Server-side Validation
* ORM-based Database Access
* No direct database or model exposure

>  This is an academic project; production-level security enhancements can be added.

---

##  13. Limitations

* AI accuracy depends on training data
* SQLite limits scalability
* No cloud deployment yet
* No mobile application support

---

##  14. Future Enhancements

* Cloud Deployment (AWS / Heroku)
* Mobile App Integration
* Advanced Analytics Dashboard
* Real-time Team Leave Tracking
* Improved AI Accuracy with Larger Datasets

---

##  15. License

This project is developed for **academic purposes** only.
Feel free to use and modify it for learning and educational use.

---

###  If you like this project, don’t forget to star the repository!
