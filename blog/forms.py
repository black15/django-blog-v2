from django import forms
from .models import Comment

class SharePostViaEmail(forms.Form):
        name            = forms.CharField(max_length=30)
        email           = forms.EmailField(max_length=50)
        to              = forms.EmailField(max_length=50)
        comments        = forms.CharField(
                                        required=False,
                                        widget=forms.Textarea
                                        )

class CommentForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ("name", "email", "body")
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'body': forms.Textarea(
                attrs={'placeholder': 'Comment'}),
        }
