from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your comment...",
                }
            ),
        }
    def clean_body(self):
        body = self.cleaned_data["body"].strip()

        if not body:
            raise forms.ValidationError("Comment cannot be empty.")

        return body