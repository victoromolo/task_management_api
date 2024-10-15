from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority_level', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All')] + Task.STATUS_CHOICES
    PRIORITY_CHOICES = [('', 'All')] + Task.PRIORITY_CHOICES

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    priority_level = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)
    due_date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    due_date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    ordering = forms.ChoiceField(choices=[
        ('due_date', 'Due Date (Ascending)'),
        ('-due_date', 'Due Date (Descending)'),
        ('priority_level', 'Priority Level (Ascending)'),
        ('-priority_level', 'Priority Level (Descending)')
    ], required=False) 
