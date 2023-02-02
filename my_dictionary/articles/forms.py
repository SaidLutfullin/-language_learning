from .models import Article, Comment
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="extends"))
    
    class Meta:
        model = Article
        fields = "__all__"

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required=False

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "text": CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name="default")
        }
