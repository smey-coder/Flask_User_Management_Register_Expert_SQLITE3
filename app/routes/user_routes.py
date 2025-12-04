from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
)

from app.forms.user_forms import UserCreateForm, UserEditForm, ConfirmDeleteForm
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/")
def index():
    users = UserService.get_all()
    return render_template("users/index.html", users=users)

@user_bp.route("/<int:user_id>")
def detail(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    return render_template("users/detail.html", user=user)

@user_bp.route("/create", methods=["GET", "POST"])
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data
        try:
            user = UserService.create(data, password)
        except Exception as exc:
            flash("Failed to create user: an internal error occurred.", "danger")
            return render_template("users/create.html", form=form)
        flash(f"User '{user.username}' was created successfully.", "success")
        return redirect(url_for("users.index"))
    else:
        # If this is a POST but form did not validate, show debug info
        from flask import request
        if request.method == "POST":
            # Log or flash errors to the user to help debugging
            app_logger = __import__("logging").getLogger("app")
            app_logger.warning("Create user: form failed to validate. Errors=%s", form.errors)
            flash("There were errors creating the user. Please review the form.", "warning")

    return render_template("users/create.html", form=form)

@user_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
        
    form = UserEditForm(original_user=user, obj=user)
    
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data or None
        try:
            UserService.update(user, data, password)
        except Exception as exc:
            flash("Failed to update user: an internal error occurred.", "danger")
            return render_template("users/edit.html", form=form, user=user)
        flash(f"User '{user.username}' was updated successfully.", "success")
        return redirect(url_for("users.detail", user_id=user.id))
    else:
        from flask import request
        if request.method == "POST":
            app_logger = __import__("logging").getLogger("app")
            app_logger.warning("Edit user: form failed to validate for user %s. Errors=%s", user_id, form.errors)
            flash("There were errors updating the user. Please review the form.", "warning")
    
    return render_template("users/edit.html", form=form, user=user)

@user_bp.route("/<int:user_id>/delete", methods=["GET"])
def delete_confirm(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
        
    form = ConfirmDeleteForm()
    return render_template("users/delete_confirm.html", user=user,form=form)

@user_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
        
    UserService.delete(user)
    flash("User was deleted successfully.", "success")
    
    return redirect(url_for("users.index"))

    