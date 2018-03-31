from django import forms


class LocationSearchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, initial='Madrid')
