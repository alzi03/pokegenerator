from django import forms

class GuessForm(forms.Form):
    guess = forms.CharField(required=True, label="Guess", widget=forms.TextInput(attrs={'placeholder': 'required'}))