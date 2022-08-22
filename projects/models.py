from enum import unique
from django.db import models

import uuid

from users.models import Profile

#############################################################################
# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    feature_image = models.ImageField(null=True, blank=True, default='projects/default.jpg', upload_to='projects/')
    
    tags = models.ManyToManyField('Tag', blank=True)
    # owner = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    # owner = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey('users.Profile', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        # ordering = ["created_at"]
        ordering = ["-vote_ratio", "-vote_total", "title"]
    
    @property
    def imageURL(self):
        
        try:
            url = self.feature_image.url
        except:
            url = ''
            
        return url
    
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat = True)
        return queryset
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        
        ratio = (upVotes/totalVotes) * 100
        
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
        self.save()
        
        

    
class Review(models.Model):
    
    VOTE_TYPE = (('up','Up Vote'),('down','Down Vote'))
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
     
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey('users.Profile', on_delete=models.CASCADE, null=True, blank=True)
    # owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.value} - {self.owner}"
    
    class Meta:
        unique_together = [['owner', 'project']]
        ordering = ["-created_at"]


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name