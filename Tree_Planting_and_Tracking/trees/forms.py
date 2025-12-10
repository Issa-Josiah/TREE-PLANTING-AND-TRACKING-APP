from django import forms
from .models import Tree

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'second_name',  'description', 'image', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
class TreeAdminForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'second_name' , 'price', 'description', 'image', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),

        }



