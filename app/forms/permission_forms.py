from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models.permission import Permission
from extensions import db

class PermissionCreateForm(FlaskForm):
    name = StringField(
        "Permission Name",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "e.g., create_user, edit_user, delete_user"},
    )
    description = StringField(
        "Description",
        validators=[Length(max=255)],
        render_kw={"placeholder": "What does this permission allow?"},
    )
    
    submit = SubmitField("Create")
    
    def validate_name(self, field):
        exists = db.session.scalar(
            db.select(Permission).filter(Permission.name == field.data)
        )
        if exists:
            raise ValidationError("This permission already exists.")

class PermissionEditForm(FlaskForm):
    name = StringField(
        "Permission Name",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    description = StringField(
        "Description",
        validators=[Length(max=255)],
    )
    
    submit = SubmitField("Update")
    
    def __init__(self, original_permission: Permission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_permission = original_permission
    
    def validate_name(self, field):
        if field.data != self.original_permission.name:
            exists = db.session.scalar(
                db.select(Permission).filter(Permission.name == field.data)
            )
            if exists:
                raise ValidationError("This permission already exists.")

class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")
