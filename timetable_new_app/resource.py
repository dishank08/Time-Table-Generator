from import_export import resources
from .models import *

class Sem_4_C_Timetable(resources.ModelResource):
	class Meta:
		model = Sem_4_C

class Sem_4_D_Timetable(resources.ModelResource):
	class Meta:
		model = Sem_4_D

class Sem_6_C_Timetable(resources.ModelResource):
	class Meta:
		model = Sem_6_C

class Sem_6_D_Timetable(resources.ModelResource):
	class Meta:
		model = Sem_6_D
