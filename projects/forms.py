from django import forms
from django.forms import Form, ModelForm, widgets

from .models import Project, Review





class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__' 
        # fields = ['title', 'feature_image', 'description', 'demo_link', 'source_link', 'tags']
        fields = ['title', 'feature_image', 'description', 'demo_link', 'source_link', 'tags']
        exclude = ['tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self.fields['title'].widget.attrs.update({'class':'input input--text', "placeholder":'Enter title'})
        # self.fields['description'].widget.attrs.update({'class':'input input--text'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})
        
            
            

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your Vote',
            'body': 'Add a comment with your vote'
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = True
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})
        