from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    to = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Reciever\'s Email'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(
                attrs={'placeholder': 'Enter you comment...'})
                )
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email (optional)'}),
            'body': forms.Textarea(
                attrs={'placeholder': 'Enter you comment...'}),
        }
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField()
