from logging import PlaceHolder
from django import forms
import datetime
from bootstrap_datepicker_plus.widgets import DatePickerInput
from dateutil.relativedelta import relativedelta
from Fligts.models import Airport

#autocomplete field case
class SearchForm(forms.Form):
    
    origin_airport = forms.CharField(label='Origin', widget=forms.TextInput(attrs={'placeholder': 'Select an origin airport'}))
    destination_airport = forms.CharField(label='Destination', widget=forms.TextInput(attrs={'placeholder': 'Select a destination airport'}))

    #dep_date_widgets = forms.MultiWidget(widgets=[DatePickerInput(), forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'})])
    #, initial = datetime.date.today
    departure_date = forms.DateField(
        label = 'Departure Date',
        input_formats=['%d/%m/%Y'],
        widget = DatePickerInput(
            attrs = {'class': 'form-control datetimepicker-input'}
        ))

    arrival_date = forms.DateField(
        label = 'Arrival Date',
        required= False,
         widget = DatePickerInput(
             attrs = {'class': 'form-control datetimepicker-input'}
         ))


    def _validateDepartureDate(self, cleaned_data):
        """
        Validate departure date
        Validations:
            - departure date is >= today
            - departure date < arrival date
        """
        #get values from cleaned_data
        departure_date = cleaned_data.get("departure_date")
        arrival_date = cleaned_data.get("arrival_date")
        
        #block of validations
        #check if departure date is smaller than today
        if (departure_date - datetime.date.today()).total_seconds() < 0:
            self.add_error('departure_date', "A departure date previous than today's date is not accepted")
        if arrival_date and  departure_date > arrival_date:
            self.add_error('departure_date', 'Departure date must be prior to arrival date')
        
    
    def _validateAirports(self, cleaned_data):
        """
        Validate origin and destination airports
        Validations:
            - origin is not empty and is a valid airport
            - destination is not empty and a a valid airport
            - origin and destination are not equal
        """

        origin = cleaned_data.get("origin_airport")
        destination = cleaned_data.get("destination_airport")

        if not origin or not Airport.objects.filter(name = origin).exists():
            self.add_error('origin_airport', "Origin airport is not valid")
        elif not destination or not Airport.objects.filter(name = destination).exists():
            self.add_error('destination_airport', "Destination airport is not valid")
        elif origin == destination:
            self.add_error(None, "Origin and destination airport cannot be the same")


    def clean(self):
        """
        override clean method from parent
        throw composed errors
        validations:
            - departure date
            - arrival_date
        """
        cleaned_data = super().clean()

        self._validateDepartureDate(cleaned_data)

        self._validateAirports(cleaned_data)

    



        


