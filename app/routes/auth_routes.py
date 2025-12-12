from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import UserTable# Needed for type hints and registration logic
from app.models.role import RoleTable
from app.forms.multi_checkbox_field import UserCreateForm # Using the UserCreateForm from the same file for simplicity
from app.services.user_service import UserService # Using both services

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    if request.method:
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        user = UserTable.query.fliter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash(f"Your account in inactive. Please contact administrator.", "warning")
                return redirect(url_for("auth.login")) 
            
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("tbl_users.index"))
        
        flash("Invalide username or password", "danger")
        return redirect(url_for("auth.login"))
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        errors: list[str] = []
        
        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not full_name:
            errors.append("Full name is required.")
        if not password:
            errors.append("Password is required.")
        if password and password != confirm_password:
            errors.append("Password do not match.")
            
        if username and UserTable.query.filter_by(username=username).first():
            errors.append("This username is aready taken.")
            
        if email and UserTable.query.filter_by(email=email).first():
            errors.append("This email is aready register.")
            
        if errors:
            for msg in errors:
                flash(msg, "danger")
            return render_template(
                "auth/register.html",
                username=username,
                email=email,
                full_name=full_name,
            )
            
        default_role = RoleTable.query.filter_by(name="User").first()
        default_role_id = default_role_id if default_role else None
        
        data = {
            "Username": username,
            "email": email,
            "full_name": full_name,
            "is_active": True,
        }
        new_user = UserService.create_user(
            data = data,
            password=password,
            role_id=default_role_id,
        )
        login_user(new_user)
        flash("Account created successfully. You are now loggedd in.", "success")
        return redirect(url_for("tbl_users.index"))
    
    return render_template(url_for("auth/register.html"))
    
@auth_bp.route("/logout")
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

# @auth_bp.route("/home")
# def home():
#     """Placeholder home route."""
#     return render_template("home.html")