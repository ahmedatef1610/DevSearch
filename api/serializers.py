import re
from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

#############################################################################
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

############################

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

############################

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
    # owner = ProfileSerializer(many=False)
    owner = serializers.SerializerMethodField('owner_info')

    def owner_info(self, obj):
        return obj.owner.username

############################
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # reviews = serializers.SerializerMethodField()
    reviews = ReviewSerializer(source='review_set', many=True)
    
        
    # def get_reviews(self, obj): # obj = Project model
    #     reviews = obj.review_set.all()
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return serializer.data
        
        
############################


