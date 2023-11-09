import typing as t

from flask import request
from flask_security import forms


class RegisterForm(forms.ConfirmRegisterForm, forms.NextFormMixin):
    """Override register form so we never need password confirm"""

    def validate(self, **kwargs: t.Any) -> bool:
        if not super().validate(**kwargs):
            return False
        return True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get("next", "")
