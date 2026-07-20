from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import Comment


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox
    )

    class Meta:
        model = Comment
        fields = (
            "name",
            "email",
            "content",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Your email",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your comment...",
                }
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()

        if not content:
            raise forms.ValidationError(
                "Comment cannot be empty."
            )

        return content