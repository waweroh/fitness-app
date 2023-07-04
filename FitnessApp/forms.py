# from django import forms
# from .models import Bmi

# class BmiForm(forms.Form):
    
#     name = forms.CharField(required=False)
#     height = forms.FloatField(label="Height in meters:", required=True, min_value=0)
#     weight = forms.FloatField(label="Weight in kg:", required=True, min_value=0)
    

# class BmiMeasurementForm(forms.ModelForm):
#     class Meta:
#         model = Bmi
#         fields = ["id", "height_in_metres", "weight_in_kg", "date_measured", "bmi_value"]