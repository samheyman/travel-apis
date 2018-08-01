from django import forms


class SearchForm(forms.Form):
    origin_field = forms.CharField(label='From', max_length=100, initial='uk')
    destination_field = forms.CharField(label='To', max_length=100, initial='us')
    from_date_field = forms.CharField(label='To', max_length=100, initial='2018')
    to_date_field = forms.CharField(label='To', max_length=100, initial='2018')
    service_field = forms.ChoiceField(choices=[('browsequotes','Quotes'),('browseroutes','Routes'),('browsedates','Dates'),('browsegrid','Grid')], widget=forms.RadioSelect())

class AirportSearchForm(forms.Form):
    airport = forms.CharField(label='Airport', max_length=100, initial='MAD')
    year = forms.ChoiceField(choices=(
        [            
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
