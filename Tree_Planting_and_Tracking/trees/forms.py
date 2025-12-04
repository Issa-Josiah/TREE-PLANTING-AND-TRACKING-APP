from django import forms
from .models import Tree

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'description', 'image', 'location']

class TreeAdminForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['price', 'payment_details']
        widgets = {
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }