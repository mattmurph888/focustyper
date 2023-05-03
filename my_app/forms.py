from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import User_Level_Record


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='', max_length='100', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='', max_length='100', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


class UserLevelRecordForm(forms.ModelForm):
    class Meta:
        model = User_Level_Record
        fields = ['accuracy', 'speed']
        widgets = {
            'accuracy': forms.HiddenInput(),
            'speed': forms.HiddenInput(),
        }
        
    def __init__(self, user, level, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.level = level
        self.score = None
    
    # gets the highest score for this level in the database
    def get_highest_score(self):
        highest_score = 0
        try:
            previous_record = User_Level_Record.objects.filter(user=self.user, level=self.level).latest('score')
            highest_score = previous_record.score
        except User_Level_Record.DoesNotExist:
            print('no record found')
            pass
        return highest_score
    
    # caluclates the score from the speed and accuracy
    def calculate_score(self, speed, accuracy):
        cleaned_data = super().clean()
        return int(speed * accuracy / 100)
    
    # check if the current score is the highest score for this level in the database
    def is_high_score(self): 
        high_score = self.get_highest_score()
        print(f"score: {self.score} || high score: {high_score}")
        if high_score and high_score >= self.score:
            return False
        return True
    
    # updates self.score
    def clean(self):
        cleaned_data = super().clean()
        self.score = self.calculate_score(cleaned_data.get('speed'), cleaned_data.get('accuracy'))
        return cleaned_data

