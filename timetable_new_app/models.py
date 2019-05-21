from django.db import models

class Subject(models.Model):
    sub_name=models.CharField(max_length=20,primary_key=True)
    semester=models.IntegerField()
    theory_hours=models.IntegerField()
    practical_hours=models.IntegerField()
    allocated=models.IntegerField()

class Faculty(models.Model):
    fac_id=models.IntegerField(null=True)
    faculty_name=models.CharField(max_length=10)
    sub_name=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    #sub_name=models.CharField(max_length=15,null=True)
    theory_hours=models.IntegerField()
    practical_hours=models.IntegerField()

class LoadAllocate(models.Model):
    sub_name=models.CharField(max_length=10,null=True)
    theory_hours=models.IntegerField()
    pract_hours=models.IntegerField()

class LabAllocation(models.Model):
    day=models.CharField(max_length=20)
    slot=models.CharField(max_length=5)
    batch=models.CharField(max_length=5)
    sub_name=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    lab_no=models.CharField(max_length=5)
    faculty_name=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
    sem=models.IntegerField()
    division=models.CharField(max_length=2)

class Faculty_Availability(models.Model):
    day=models.CharField(max_length=15)
    faculty_name=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
    slot=models.CharField(max_length=5)
    availability=models.IntegerField()

class Faculty_Subject_Totalhours(models.Model):
    faculty_name=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
    sub_name=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    total_hours=models.IntegerField()

class TheoryAllocation(models.Model):
    day=models.CharField(max_length=15)
    faculty_name=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
    sub_name=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)

class Sem_4_C(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Sem_4_D(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Sem_6_C(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Sem_6_D(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Monday(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Tuesday(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Wednesday(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Thursday(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Friday(models.Model):
    slot1=models.CharField(max_length=100)
    slot2=models.CharField(max_length=100)
    slot3=models.CharField(max_length=100)
    slot4=models.CharField(max_length=100)
    slot5=models.CharField(max_length=100)
    slot6=models.CharField(max_length=100)
    slot7=models.CharField(max_length=100)
    slot8=models.CharField(max_length=100)

class Sem_4_C_lab(models.Model):
    batch1=models.CharField(max_length=500)
    batch2=models.CharField(max_length=500)
    batch3=models.CharField(max_length=500)
    batch4=models.CharField(max_length=500)

class Sem_4_D_lab(models.Model):
    batch1=models.CharField(max_length=500)
    batch2=models.CharField(max_length=500)
    batch3=models.CharField(max_length=500)
    batch4=models.CharField(max_length=500)

class Sem_6_C_lab(models.Model):
    batch1=models.CharField(max_length=500)
    batch2=models.CharField(max_length=500)
    batch3=models.CharField(max_length=500)
    batch4=models.CharField(max_length=500)

class Sem_6_D_lab(models.Model):
    batch1=models.CharField(max_length=500)
    batch2=models.CharField(max_length=500)
    batch3=models.CharField(max_length=500)
    batch4=models.CharField(max_length=500)
