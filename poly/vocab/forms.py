from django import forms

class WordWithContext(forms.Form):
    word = forms.CharField(label='Word', max_length=50)
    context = forms.CharField(label='Context', max_length = 300, widget=forms.Textarea)