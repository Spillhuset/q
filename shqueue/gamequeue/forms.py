from django import forms
from .models import *

# class RegisterPersonInQueueForm(forms.ModelForm):
  # class Meta:
    # model = PersonInQueue
    # fields = ['name']

class AddPersonForm(forms.ModelForm):
  class Meta:
    model = QueuedPerson
    fields = ['name']
