from django import forms


class LocationSearchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, initial='Madrid')
    number_of_results = forms.CharField(label='Number of results', max_length=100, initial=10)
    provider = forms.ChoiceField(
        choices=(
            [
                ('foursquare', 'FourSquare'),
                ('avuxi', 'Avuxi'),
                ('yapq','YapQ')
            ]),
        widget=forms.Select(attrs={"class":"form-control form-control-sm", "style":"height:26px"}))
    category = forms.ChoiceField(
        choices=(
            [
                ('all', 'All'),
                ('food', 'Food (FourSquare)'), 
                ('drinks', 'Drinks (FourSquare)'), 
                ('coffee', 'Coffee (FourSquare)'), 
                ('shops', 'Shops (FourSquare)'), 
                ('arts', 'Arts (FourSquare)'), 
                ('outdoors', 'Outdoors (FourSquare)'), 
                ('sights', 'Sights (FourSquare)'), 
                ('trending', 'Trending (FourSquare)'), 
                ('nextVenues', 'Next venues (FourSquare)'), 
                ('topPicks', 'Top picks (FourSquare)'), 
            ]),
        widget=forms.Select(attrs={"class":"form-control form-control-sm", "style":"height:26px"}))


    