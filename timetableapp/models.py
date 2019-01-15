from django.db import models

class Subject(models.Model):
    sub_name=models.CharField(max_length=20,primary_key=True)
    semester=models.IntegerField()
    theory_hours=models.IntegerField()
    practical_hours=models.IntegerField()

class Faculty(models.Model):
    faculty_name=models.CharField(max_length=10)
    sub_name=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    theory_hours=models.IntegerField()
    practical_hours=models.IntegerField()

class LoadAllocate(models.Model):
	sub_name=models.CharField(max_length=10,null=True)
	theory_hours=models.IntegerField()
	pract_hours=models.IntegerField()
		
# Create your models here.
