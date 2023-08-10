from django import forms
from .models import *

class AddPersonForm(forms.ModelForm):
  class Meta:
    model = QueuedPerson
    fields = ['name']
