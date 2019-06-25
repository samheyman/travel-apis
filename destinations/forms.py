from django import forms


class LocationSearchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, initial='Madrid')
    number_of_results = forms.CharField(label='Number of results', max_length=100, initial=10)
    provider = forms.ChoiceField(
        choices=(
            [
                ('foursquare', 'Foursquare'),
                ('avuxi', 'Avuxi'),
                ('yapq','YapQ')
            ]),
        widget=forms.Select(attrs={"class":"form-control form-control-sm", "style":"height:26px"}))
    category = forms.ChoiceField(
        choices=(
            [
                ('all', 'All'),
                ('food', 'Food (Foursquare)'), 
                ('drinks', 'Drinks (Foursquare)'), 
                ('coffee', 'Coffee (Foursquare)'), 
                ('shops', 'Shops (Foursquare)'), 
                ('arts', 'Arts (Foursquare)'), 
                ('outdoors', 'Outdoors (Foursquare)'), 
                ('sights', 'Sights (Foursquare)'), 
                ('trending', 'Trending (Foursquare)'), 
                ('nextVenues', 'Next venues (Foursquare)'), 
                ('topPicks', 'Top picks (Foursquare)'), 
            ]),
        widget=forms.Select(attrs={"class":"form-control form-control-sm", "style":"height:26px"}))


    