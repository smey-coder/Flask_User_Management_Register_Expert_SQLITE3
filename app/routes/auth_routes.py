from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User # Needed for type hints and registration logic
from app.forms.login_form import LoginForm 
from app.forms.login_form import UserCreateForm # Using the UserCreateForm from the same file for simplicity
from app.services.auth_service import AuthService, UserService # Using both services

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    if current_user.is_authenticated:
        # Assuming there is a blueprint named 'users' with an index route, or define a default home.
        return redirect(url_for("auth.home")) 
    
    form = LoginForm() 

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        
        # FIXED: Delegate authentication logic to the AuthService
        user = AuthService.authenticate(username, password)
        
        if user is None:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))
        
        if not user.is_active:
            flash("Your account is inactive. Contact an administrator.", "warning")
            return redirect(url_for("auth.login"))
        
        login_user(user, remember=remember)
        flash(f"Welcome back, {user.username}!", "success")
        
        # Redirect to next page or users index
        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            # Assuming 'users.index' or 'auth.home' is the default target
            return redirect(next_page)
        return redirect(url_for("auth.home")) 
    
    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.home"))
    
    form = UserCreateForm()
    if form.validate_on_submit():
        # WARNING: In a real app, this should use db.session.execute(select(...))
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register"))
        
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))
        
        try:
            data = {
                "username": form.username.data,
                "email": form.email.data,
                "full_name": form.full_name.data,
            }
            # Delegate creation logic to UserService
            UserService.create(data, form.password.data) 
            flash(f"Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as exc:
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for("auth.register"))
    
    return render_template("auth/register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/home")
def home():
    """Placeholder home route."""
    return render_template("home.html")