from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
from ai_model.ai_predictor import predict_leave_approval
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ------------------ EMAIL CONFIG ------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'Your email address'
app.config['MAIL_PASSWORD'] = 'kmyo zdsp ipyw pnpe'
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)
db = SQLAlchemy(app)

# ------------------ MODELS ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    role = db.Column(db.String(20), default='Employee')  # Employee, Manager, Admin

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    reason = db.Column(db.String(255))
    status = db.Column(db.String(50), default="Pending")
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    ai_recommendation = db.Column(db.String(50))  

    user = db.relationship('User', backref='leaves', lazy=True)

# ------------------ EMAIL HELPER ------------------
def send_email(subject, recipients, html):
    try:
        msg = Message(subject, recipients=recipients, html=html)
        mail.send(msg)
        print(f" Email sent to {recipients}")
    except Exception as e:
        print(" Error sending email:", e)

# ------------------ CREATE DEFAULT ADMIN ------------------
def create_default_admin():
    """Ensures an Admin account exists at startup"""
    admin = User.query.filter_by(email="Your admin email").first()
    if not admin:
        admin = User(
            name="System Admin",
            email="Your admin email",
            password="Your pass",
            department="Admin",
            role="Admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin created (email: Your admin email, password: your pass)")

# ------------------ ROUTES ------------------
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# ---------- Register (Employees only) ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        role = "Employee"  # Only Employee allowed

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        user = User(name=name, email=email, password=password, department=department, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # Always reset session to avoid old values
            session.clear()

            # Set updated session details
            session['user_id'] = user.id
            session['name'] = user.name
            session['role'] = user.role
            session['department'] = user.department

            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('dashboard'))

        flash("Invalid email or password!", "danger")
    return render_template('login.html')

# ---------- Dashboard ----------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.role == 'Admin':
        leaves = LeaveRequest.query.all()
    elif user.role == 'Manager':
        employees = User.query.filter_by(department=user.department, role='Employee').all()
        emp_ids = [e.id for e in employees]
        leaves = LeaveRequest.query.filter(LeaveRequest.user_id.in_(emp_ids)).all()
    else:
        leaves = LeaveRequest.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, leaves=leaves)

# ---------- Apply Leave ----------
from datetime import datetime
import os, joblib, pandas as pd, numpy as np

@app.route('/apply', methods=['GET', 'POST'])
def apply_leave():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        user_id = session['user_id']

        ai_decision = "Pending"
        model_path = os.path.join('ai_model', 'model.pkl')
        encoder_path = os.path.join('ai_model', 'encoders.pkl')

        # AI Model Prediction
        if os.path.exists(model_path) and os.path.exists(encoder_path):
            try:
                model = joblib.load(model_path)
                encoders = joblib.load(encoder_path)

                user = User.query.get(user_id)
                department = user.department or "IT"
                role = user.role or "Employee"
                leave_type = "Casual"
                leave_duration = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
                previous_leaves = np.random.randint(1, 10)
                team_on_leave_ratio = np.random.randint(5, 40)

                encoded_dept = encoders['department'].transform([department])[0] if department in encoders['department'].classes_ else 0
                encoded_role = encoders['role'].transform([role])[0] if role in encoders['role'].classes_ else 0
                encoded_leave_type = encoders['leave_type'].transform([leave_type])[0] if leave_type in encoders['leave_type'].classes_ else 0
                
                features = pd.DataFrame([{
                    'department': encoded_dept,
                    'role': encoded_role,
                    'leave_type': encoded_leave_type,
                    'leave_duration': leave_duration,
                    'previous_leaves': previous_leaves,
                    'team_on_leave_ratio': team_on_leave_ratio
                }])

                probas = model.predict_proba(features)[0]
                approval_chance = probas[0] * 100

                if approval_chance >= 60:
                    ai_decision = f"High chance of approval ({approval_chance:.1f}%)"
                elif approval_chance >= 40:
                    ai_decision = f"Moderate chance of approval ({approval_chance:.1f}%)"
                else:
                    ai_decision = f"Low chance of approval ({approval_chance:.1f}%)"

            except Exception as e:
                ai_decision = "AI Error"
                print("⚠️ AI Error:", e)

        # Save Leave Request
        leave = LeaveRequest(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            ai_recommendation=ai_decision
        )

        db.session.add(leave)
        db.session.commit()

        flash("Leave request submitted successfully!", "success")

        # -------- Email to Manager/Admin with Approve/Reject Links --------
        user = User.query.get(user_id)

        html = f"""
        <h2>📝 New Leave Request</h2>
        <p><strong>Employee:</strong> {user.name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Reason:</strong> {reason}</p>
        <p><strong>Duration:</strong> {start_date} → {end_date}</p>
        <p><strong>AI Suggestion:</strong> {ai_decision}</p>
        <p><strong>Status:</strong> Pending</p>
        <br>
        <div style="margin-top:15px; display:flex; gap:10px;">
        
            <a href="{url_for('approve', leave_id=leave.id, _external=True)}" 
                style="background:#10b981;padding:10px 15px;border-radius:6px;
                color:white;text-decoration:none;">
                ✔ Approve
            </a>

            <a href="{url_for('reject', leave_id=leave.id, _external=True)}" 
                style="background:#ef4444;padding:10px 15px;border-radius:6px;
                color:white;text-decoration:none;">
                ✖ Reject
            </a>
        </div>
        """

        send_email("New Leave Request Submitted", ["Your Email"], html)

        return redirect(url_for('dashboard'))

    return render_template('apply_leave.html')

# ---------- Reports ----------
@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Role-based report visibility
    if user.role == 'Admin':
        leaves = LeaveRequest.query.all()
    elif user.role == 'Manager':
    # Get everyone in the same department INCLUDING themselves
        team = User.query.filter_by(department=user.department).all()
        team_ids = [member.id for member in team]

        leaves = LeaveRequest.query.filter(LeaveRequest.user_id.in_(team_ids)).all()
    else:
        leaves = LeaveRequest.query.filter_by(user_id=user.id).all()

    return render_template('reports.html', user=user, leaves=leaves)

# ---------- Approve (Manager/Admin only) ----------
@app.route('/approve/<int:leave_id>')
def approve(leave_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user = User.query.get(session['user_id'])
    if current_user.role not in ['Manager', 'Admin']:
        flash("Access denied! Only Manager or Admin can approve leaves.", "danger")
        return redirect(url_for('dashboard'))

    leave = LeaveRequest.query.get_or_404(leave_id)
    leave.status = "Approved"
    db.session.commit()

    user = User.query.get(leave.user_id)
    send_email(
        "Your Leave Request Approved",
        [user.email],
        f"<p>Hi {user.name},</p><p>Your leave from {leave.start_date} to {leave.end_date} has been approved .</p>"
    )
    flash("Leave approved successfully.", "success")
    return redirect(url_for('dashboard'))

#  DELETE LEAVE REQUEST
@app.route('/delete/<int:leave_id>', methods=['POST'])
def delete_leave(leave_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    leave = LeaveRequest.query.get_or_404(leave_id)
    user = User.query.get(session['user_id'])

    # Restrict access: Employees can delete only their own pending requests
    if user.role != 'Admin' and leave.user_id != user.id:
        flash("You are not authorized to delete this leave request.", "danger")
        return redirect(url_for('dashboard'))

    # Optional: Prevent deleting approved/rejected requests for employees
    if user.role == 'Employee' and leave.status != 'Pending':
        flash("You can only delete pending leave requests.", "warning")
        return redirect(url_for('dashboard'))

    db.session.delete(leave)
    db.session.commit()
    flash("Leave request deleted successfully.", "success")
    return redirect(url_for('dashboard'))

# ---------- Reject (Manager/Admin only) ----------
@app.route('/reject/<int:leave_id>')
def reject(leave_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user = User.query.get(session['user_id'])
    if current_user.role not in ['Manager', 'Admin']:
        flash("Access denied! Only Manager or Admin can reject leaves.", "danger")
        return redirect(url_for('dashboard'))

    leave = LeaveRequest.query.get_or_404(leave_id)
    leave.status = "Rejected"
    db.session.commit()

    user = User.query.get(leave.user_id)
    send_email(
        "Your Leave Request Rejected",
        [user.email],
        f"<p>Hi {user.name},</p><p>Your leave from {leave.start_date} to {leave.end_date} has been rejected .</p>"
    )
    flash("Leave rejected successfully.", "info")
    return redirect(url_for('dashboard'))

# ---------- Admin Dashboard ----------
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.role != 'Admin':
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('dashboard'))

    all_users = User.query.all()
    all_leaves = LeaveRequest.query.all()
    return render_template('admin_dashboard.html', user=user, all_users=all_users, all_leaves=all_leaves)

# ---------- Update Role (Admin only) ----------
@app.route('/update-role/<int:user_id>', methods=['POST'])
def update_role(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    admin = User.query.get(session['user_id'])
    if admin.role != 'Admin':
        flash("Access denied! Only admins can update roles.", "danger")
        return redirect(url_for('dashboard'))

    new_role = request.form.get('role')
    user = User.query.get_or_404(user_id)
    
    if new_role not in ['Employee', 'Manager', 'Admin']:
        flash("Invalid role selected!", "danger")
        return redirect(url_for('admin_dashboard'))

    # Prevent admin from removing their own admin access
    if user.id == admin.id:
        flash("You cannot change your own role.", "warning")
        return redirect(url_for('admin_dashboard'))

    user.role = new_role
    db.session.commit()
    flash(f"{user.name}'s role updated to {new_role}.", "success")
    return redirect(url_for('admin_dashboard'))

# ---------- Delete User (admin) ----------
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user = User.query.get(session['user_id'])
    if not current_user or current_user.role != 'Admin':
        flash("Access denied! Only Admins can delete users.", "danger")
        return redirect(url_for('admin_dashboard'))

    user_to_delete = User.query.get_or_404(user_id)

    # Prevent admin from deleting themselves
    if user_to_delete.id == current_user.id:
        flash("You cannot delete your own account!", "warning")
        return redirect(url_for('admin_dashboard'))

    # Delete user's leave requests first (cascade manually if needed)
    LeaveRequest.query.filter_by(user_id=user_to_delete.id).delete()
    db.session.delete(user_to_delete)
    db.session.commit()

    flash(f"User '{user_to_delete.name}' and all related leave records deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))

# ---------- Change Password ----------
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Basic checks
        if user.password != current_password:
            flash(" Current password is incorrect.", "danger")
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash(" New passwords do not match.", "warning")
            return redirect(url_for('change_password'))

        # Update password
        user.password = new_password
        db.session.commit()
        flash(" Password changed successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('change_password.html', user=user)

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# ------------------ MAIN ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()  
    app.run(debug=True)
