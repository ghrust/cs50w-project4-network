from django import forms


class NewPostForm(forms.Form):
    post = forms.CharField(
        required=True,
        label='New Post',
        label_suffix='',
        widget=forms.Textarea(
            attrs={
                'class': 'w-100',
                'rows': '3'
            }
        )
    )


class EditPostForm(forms.Form):
    post = forms.CharField(
        required=True,
        label='',
        label_suffix='',
        widget=forms.Textarea(
            attrs={
                'class': 'w-100',
            }
        )
    )
