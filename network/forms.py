from django import forms


class NewPostForm(forms.Form):
    post = forms.CharField(
        required=True,
        label='New Post'
    )
