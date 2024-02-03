# forms.py
from django import forms
from .models import Suggestion
from .models import SuggestionDis
from .models import Suggestion_state_to_sch
from .models import CustomUser
from .models import SchoolYearData


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel File', widget=forms.ClearableFileInput(attrs={'accept': '.xlsx, .xls'}))


class SchoolSignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','state','District','s_category']
        widgets = {
            'password': forms.PasswordInput(),
        }


class GovernmentSignUpForm(forms.ModelForm):
    alert_message = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','state','state_id']
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'off'}),
            'state': forms.TextInput(attrs={'autocomplete': 'off'}),
            'state_id': forms.TextInput(attrs={'autocomplete': 'off'}),
        }
    
    def clean_state_id(self):
        state_id = self.cleaned_data.get('state_id')
        state = self.cleaned_data.get('state')

        # Define state IDs (replace with actual IDs)
        state_ids = {'Gujarat': '1234', 'OtherState': 'other_id'}

        # if state_id != state_ids.get(state, ''):
        #     print('Invalid state ID:', state_id)

        
        return state_id


class DistrictSignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','state','District']
        widgets = {
            'password': forms.PasswordInput(),
        }



class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['instructor_name', 'district_name', 'instruction','state_name']


class SuggestionDistForm(forms.ModelForm):
    class Meta:
        model = SuggestionDis
        fields = ['instructor_name', 'school_name', 'instruction','district_name','state_name']


class SuggestionStateToSchForm(forms.ModelForm):
    class Meta:
        model = Suggestion_state_to_sch
        fields = ['instructor_name', 'school_name', 'instruction','state_name']

class DropoutPredictionForm(forms.Form):
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[(0, 'Male'), (1, 'Female')])
    caste = forms.ChoiceField(choices=[(0, 'General'), (1, 'OBC'), (2, 'SC'), (3, 'ST')])
    area = forms.IntegerField()
    income = forms.IntegerField()


# from django import forms

# class DropoutPredictionForm(forms.Form):
#     age = forms.IntegerField()
#     gender = forms.ChoiceField(choices=[(0, 'Male'), (1, 'Female')])
#     caste = forms.ChoiceField(choices=[(0, 'General'), (1, 'OBC'), (2, 'SC'), (3, 'ST')])
#     area = forms.IntegerField()
#     income = forms.IntegerField()


class SchoolYearDataForm(forms.ModelForm):
    class Meta:
        model = SchoolYearData
        fields = ['year', 'total_students']