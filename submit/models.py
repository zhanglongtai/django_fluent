from django.db import models
from django.forms import ModelForm
from django import forms


# Create your models here.
class ComIns(models.Model):
    title = models.CharField(max_length=60)
    cas = models.FileField(upload_to='')
    dat = models.FileField(upload_to='')

    def __str__(self):
        return self.title


class ComInsForm(ModelForm):
    class Meta:
        model = ComIns
        fields = '__all__'


class SubmitForm(forms.Form):
    taskname = forms.CharField()
    casfile = forms.FileField()
    datfile = forms.FileField()
