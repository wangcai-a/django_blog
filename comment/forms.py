from django import forms


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='评论')