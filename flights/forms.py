from django import forms


class SearchForm(forms.Form):
    origin = forms.CharField(label='Origin', max_length=100, initial='MAD')
    destination = forms.CharField(label='Destination', max_length=100, initial='BOS')
    departure_date= forms.CharField(label='Departure date', max_length=100, initial='2019-10-01')
    return_date = forms.CharField(label='Return date', max_length=100, initial='2019-10-10')
    #service_field = forms.ChoiceField(choices=[('browsequotes','Quotes'),('browseroutes','Routes'),('browsedates','Dates'),('browsegrid','Grid')], widget=forms.RadioSelect())
    # source = forms.ChoiceField(choices=(
    #     [
    #         ('sandbox', 'Travel Innovation Sandbox'),
    #         ('amadeus4dev', 'Amadeus for Developers')
    #     ]))

class AirportSearchForm(forms.Form):
    # airport = forms.CharField(label='Airport', max_length=100, initial='MAD')
    airport = forms.ChoiceField(choices=(
        [
            ('BCN', 'Barcelona'),
            ('FRA', 'Frankfort'),
            ('LON', 'London'),
            ('MAD', 'Madrid'),
            ('NYO', 'New York'),
            ('PAR', 'Paris'),
            ('SIN', 'Singapore'),
        ]
    ))
    year = forms.ChoiceField(choices=(
        [            
            ('2019','2019'), 
            ('2018','2018'), 
            ('2017','2017'), 
            ('2016','2016'), 
            ('2015','2015')
         ]))
    month = forms.ChoiceField(choices=(
        [
            ('01','Jan'),
            ('02','Feb'),
            ('03','Mar'),
            ('04','Apr'),
            ('05','May'),
            ('06','Jun'),
            ('07','Jul'),
            ('08','Aug'),
            ('09','Sep'),
            ('10','Oct'),
            ('11','Nov'),
            ('12','Dec'),
         ]))

class LocationSearchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, initial='London')
