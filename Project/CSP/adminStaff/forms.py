from django import forms
import os,sys
import numpy as np 
from string import whitespace
from portal.models import *
from Students.models import *

class DocumentForm(forms.Form):
    docfile = forms.FileField(

        label='Select a file'

    )

class read(forms.Form):
    docfile = forms.FileField(

        label='Select a file'

    )