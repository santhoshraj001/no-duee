from django.db import models
from django.utils import timezone
STS = (
	('','Select'),
    ('Paid','Due Paid'),
    ('Not Paid', 'Not Paid'),)
class Student_Detail(models.Model):
	student_name = models.CharField('Student Name', max_length=255)
	student_id = models.CharField('Student Id', max_length=255,unique=True,null=True,blank=True)
	email_id = models.EmailField('Email Id', max_length=255)
	phone_number = models.CharField('Mobile Number', max_length=50,null=True,blank=True)
	dob =  models.DateField()
	gender = models.CharField('Gender',max_length=20)
	degree = models.CharField('Degree',max_length=200)
	dept = models.CharField('Department',max_length=200)
	address = models.TextField('Address',null=True,blank=True)
	country = models.CharField('Country', max_length=100,default='India')
	state = models.CharField('State', max_length=100,default='Tamil Nadu')
	city = models.CharField('City', max_length=100,null=True,blank=True)
	username = models.CharField('Username', max_length=100, unique=True)
	password = models.CharField('Password',max_length=30)
	image = models.FileField('Student Image',upload_to='documents/',null=True)
	face_data = models.BinaryField()
	def __str__(self):
		return self.student_name
class Due_Type(models.Model):
	due_name = models.CharField('Due Name', max_length=200)
	image = models.FileField(' Image',upload_to='documents/',null=True)
	def __str__(self):
		return self.due_name
class Staff_Detail(models.Model):
	staff_name = models.CharField('Staff Name',max_length=100)
	email = models.EmailField('Email Id',max_length=100)
	mobile = models.CharField('Mobile Num',max_length=30)
	degree = models.CharField('Degree',max_length=200)
	dept = models.CharField('Department',max_length=200)
	image = models.FileField(' Image',upload_to='product/',null=True)
	username = models.CharField('Username',max_length=100,null=True)
	password = models.CharField('Password',max_length=100,null=True)
	country = models.CharField('Country',max_length=100)
	city = models.CharField(' City',max_length=300)
	address = models.TextField(' Address',max_length=2000)
	def __str__(self):
		return self.staff_name
class Student_Due(models.Model):
	due_id = models.ForeignKey(Due_Type, on_delete=models.CASCADE)
	student_id = models.CharField('Student Id',max_length=100)
	student_name = models.ForeignKey(Student_Detail, on_delete=models.CASCADE)
	amount = models.CharField('Amount(Rs)',max_length=100)
	due_date = models.DateField()
	due_status = models.CharField('Due Status',max_length=200,choices=STS)
	msg = models.TextField('Message',max_length=2000)
	def __str__(self):
		return self.student_id
class Alert_Detail(models.Model):
	staff_name = models.ForeignKey(Staff_Detail, on_delete=models.CASCADE)
	student_id = models.CharField('Student Id',max_length=100)
	send_date = models.DateField(default=timezone.now())
	amount = models.CharField('Due Amount',max_length=100)
	msg = models.TextField('Message',max_length=2000)
	def __str__(self):
		return self.student_id
	def publish(self):
		self.send_date = timezone.now()
		self.save()