from django import forms


class SearchForm(forms.Form):
    origin_field = forms.CharField(label='From', max_length=100, initial='uk')
    destination_field = forms.CharField(label='To', max_length=100, initial='us')
    from_date_field = forms.CharField(label='To', max_length=100, initial='2018')
    to_date_field = forms.CharField(label='To', max_length=100, initial='2018')
    service_field = forms.ChoiceField(choices=[('browsequotes','Quotes'),('browseroutes','Routes'),('browsedates','Dates'),('browsegrid','Grid')], widget=forms.RadioSelect())


class AirportSearchForm(forms.Form):
    airport = forms.CharField(label='Airport', max_length=100, initial='MAD')

class LocationSearchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, initial='Madrid')
