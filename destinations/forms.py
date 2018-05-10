from django import forms


class LocationSearchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, initial='Madrid')
    number_of_results = forms.CharField(label='Number of results', max_length=100, initial=10)
    provider = forms.ChoiceField(choices=([('yapq','YapQ'), ('avuxi', 'Avuxi')]),widget=forms.Select(attrs={"class":"form-control form-control-sm", "style":"height:26px"}))
    