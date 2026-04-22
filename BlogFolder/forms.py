"""
Forms for the BlogFolder application.

Provides a ModelForm for blog comment submission.
Note: The 'post' field is excluded for security — it is set
in the view to prevent users from attaching comments to
arbitrary posts.
"""

from django import forms

from BlogFolder.models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for submitting a comment on a blog post.

    The 'post' field is intentionally excluded and set in the view
    to prevent tampering.
    """

    class Meta:
        model = Comment
        fields = ('name', 'email', 'subject', 'message')