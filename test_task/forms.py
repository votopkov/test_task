from django import forms
from django.forms import Textarea, TextInput
from models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['product', 'name', 'comment']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={'class': 'form-control'})
        }
