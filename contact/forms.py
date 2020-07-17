from django import forms
class ContactForm(forms.Form):
    nome = forms.CharField(label='Nome')
    email = forms.CharField(label='Email')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())