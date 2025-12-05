from django import forms
from .models import Tree

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'price', 'description', 'image', 'location']

class TreeAdminForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['price', ]
        widgets = {

        }



