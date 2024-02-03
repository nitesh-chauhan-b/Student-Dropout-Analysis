# from django.db import models
from .managers import CustomUserManager
# Create your models here.
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_school_user = models.BooleanField(default=False)
    is_government_user = models.BooleanField(default=False)
    is_district_user = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    state = models.CharField(max_length=50, blank=True, null=True)
    District = models.CharField(max_length=50, blank=True, null=True)
    state_id = models.CharField(max_length=50, blank=True, null=True)
    s_category=models.CharField(max_length=150, blank=True,null=True)

    objects = CustomUserManager()
    # Add other fields as needed for each user type

class contactEnquiry(models.Model):
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        name=models.CharField(max_length=150 )
        age=models.IntegerField()
        gender=models.CharField(max_length=150)
        caste=models.CharField(max_length=150)
        s_category=models.CharField(max_length=150)
        Distance=models.IntegerField()
        area=models.CharField(max_length=150)
        city=models.CharField(max_length=150)
        income=models.IntegerField()
        reason=models.CharField(max_length=150)
        foccupation=models.CharField(max_length=150)
        schoolindex=models.CharField(max_length=150)
        mystate=models.CharField(max_length=150)
        studentid=models.CharField(max_length=150)
        Year=models.IntegerField()
    

class Suggestion(models.Model):
    instructor_name = models.CharField(max_length=150)
    district_name = models.CharField(max_length=150)
    state_name = models.CharField(max_length=150,null=True,blank=True)
    instruction = models.TextField()
    

    def __str__(self):
        return f'{self.instructor_name} - {self.district_name}'
    


class SuggestionDis(models.Model):
    instructor_name = models.CharField(max_length=150)
    school_name = models.CharField(max_length=150)
    district_name = models.CharField(max_length=150,null=True,blank=True)
    state_name = models.CharField(max_length=150,null=True,blank=True)
    instruction = models.TextField()

    def __str__(self):
        return f'{self.instructor_name} - {self.school_name}'
    
class Suggestion_state_to_sch(models.Model):
    instructor_name = models.CharField(max_length=150)
    school_name = models.CharField(max_length=150)
    # district_name = models.CharField(max_length=150,null=True,blank=True)
    state_name = models.CharField(max_length=150,null=True,blank=True)
    instruction = models.TextField()

    def __str__(self):
        return f'{self.instructor_name} - {self.school_name}'



class DropoutPrediction(models.Model):
    age = models.IntegerField()
    gender = models.IntegerField()
    caste = models.IntegerField()
    distance = models.IntegerField()
    income = models.IntegerField()
    fee = models.IntegerField() #new field added
    prediction = models.IntegerField()



class SchoolYearData(models.Model):
    school = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    year = models.IntegerField()
    total_students = models.IntegerField()
    state = models.CharField(max_length=150)
    district = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.school} - {self.year}"