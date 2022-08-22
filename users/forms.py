from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Message, Profile, Skill


class CustomUserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=200, required=True, label='Name')
    email = forms.EmailField(max_length=500, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for fieldname in ['username', 'password1', 'password2']:
        #     self.fields[fieldname].help_text = None

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'input input--text'

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        # labels = {
        #     'first_name': 'Name'
        # }
        # help_texts = {
        #     'username': None,
        #     'password1': None,
        #     'password2': None,
        # }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'input input--text'
            
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'input input--text'
            
            
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['subject'].required = True
        # self.fields['body'].required = True
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'input input--text'
            field.required = True