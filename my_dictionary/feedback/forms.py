from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'E-mail',
                                                                        'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'placeholder': 'E-mail',
                                                                            'class':'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                                                            'class':'form-control'}))
