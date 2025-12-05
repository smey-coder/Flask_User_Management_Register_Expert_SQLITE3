from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models.role import Role
from extensions import db

# Role forms
class RoleCreateForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Role name"},
    )
    description = StringField(
        "Description",
        validators=[Length(max=255)],
        render_kw={"placeholder": "Short description (Optional)"},
    )
    
    submit = SubmitField("Save")
    
    # ---------- server-side uniqueness checks ---------
    
    def validate_name(self, field):
        exists = db.session.scalar(
            db.select(Role).filter(Role.name == field.data)
        )
        if exists:
            raise ValidationError("This name is already taken.")
        
        
# --------- edit form (password optional) -------------
class RoleEditForm(FlaskForm):
    name = StringField(
        "Name:",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    
    description = StringField(
        "Description",
        validators=[Length(max=255)],
    )
    
    submit = SubmitField("Update")
    
    def __init__(self, original_role: Role, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_role = original_role

    def validate_name(self, field):
        q = db.select(Role).filter(Role.name == field.data, Role.id != self.original_role.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This name is already taken.")


class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")
    
