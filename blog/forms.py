from django import forms
from blog.models import Page,Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=256,help_text="Enter the name of Category")
    class Meta:
        model = Category
        fields = ('name',)
        exclude = ('note_number',)
    def __str__(self):
        return self.name





class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Enter the Title")
    author = forms.CharField(max_length=128,help_text="Enter your Name/Anonym")
    content = forms.CharField(widget=forms.Textarea,help_text="The text of the content")
    class Meta:
        model = Page
        exclude = ('date_print','category','views','likes','favorite','id',)
    def __str__(self):
        return self.title
