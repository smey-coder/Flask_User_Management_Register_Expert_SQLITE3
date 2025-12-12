from flask import(
    Blueprint,
    render_template,
    redirect,
    flash,
    url_for,
    abort,
)
from app.forms.role_forms import RoleCreateForm, RoleEditForm, RoleConfirmDeleteForm
from app.services.role_service import RoleService

role_bp = Blueprint("roles", __name__, url_prefix="/roles")

@role_bp.route("/")
def index():
    roles = RoleService.get_all()
    return render_template("roles/index.html", roles=roles)
    
@role_bp.route("/<int:role_id>")
def detail(role_id: int):
    role = RoleService.get_by_id(role_id)
    if role is None:
        abort(404)
        
    return render_template("roles/detail.html", role=role)

@role_bp.route("/create", methods=["GET", "POST"])
def create():
    form = RoleCreateForm()
    if form.validate_on_submit():
        data = {
            "name" : form.name.data,
            "description" : form.description.data,
        }
        try:
            role = RoleService.create(data)
        except Exception as exc:
            flash("Failed to create role.", "danger")
            return render_template("roles/create.html", form=form)
        flash(f"Role '{role.name}' created successfully.", "success")
        return redirect(url_for("roles.index"))
    else:
        from flask import request
        if request.method == "POST":
            app_logger = __import__("logging").getLogger("app")
            app_logger.warning("Role creation form validation failed: %s", form.errors)
    return render_template("roles/create.html", form=form)

@role_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
def edit(role_id: int):
    role = RoleService.get_by_id(role_id)
    if role is None:
        abort(404)
        
    form = RoleEditForm(original_role=role, obj=role)
    if form.validate_on_submit():
        data = {
            "name" : form.name.data,
            "description" : form.description.data,
        }
        try:
            role = RoleService.update(role, data)
        except Exception as exc:
            flash("Failed to update role.", "danger")
            return render_template("roles/edit.html", form=form, role=role)
        flash(f"Role '{role.name}' updated successfully.", "success")
        return redirect(url_for("roles.detail", role_id=role.id))
    else:
        from flask import request
        if request.method == "POST":
            app_logger = __import__("logging").getLogger("app")
            app_logger.warning("Role edit form validation failed: %s. Errors=%s", role_id, form.errors)
    return render_template("roles/edit.html", form=form, role=role)

@role_bp.route("/<int:role_id>/delete", methods=["POST"])
def delete(role_id: int):
    role = RoleService.get_by_id(role_id)
    if role is None:
        abort(404)
        
    RoleService.delete(role)
    flash(f"Role '{role.name}' deleted successfully.", "success")
    return redirect(url_for("roles.index"))