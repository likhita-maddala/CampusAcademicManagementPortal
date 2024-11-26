from django.db import models


class Authentication(models.Model):
    rollno = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.rollno


class Roles(models.Model):
    rollno = models.CharField(max_length=20, primary_key=True)
    role = models.CharField(max_length=30)

    def __str__(self):
        return self.role



class Student(models.Model):
    studentID = models.CharField(max_length=20)
    name = models.CharField(max_length=100)



class StudentPersonalInfo(models.Model):
    studentID = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    deptID = models.CharField(max_length=20)
    phnNo = models.CharField(max_length=15)
    dob = models.DateField()
    personalMail = models.EmailField()
    section = models.CharField(max_length=10)
    date_of_joining = models.DateField()
    fathername = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    fatherphn = models.CharField(max_length=15)
    motherphn = models.CharField(max_length=15)
    father_occupation = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    fatherEducation = models.CharField(max_length=50)
    motherEducation = models.CharField(max_length=50)
    address = models.TextField()
    hostel_or_dayScholar = models.CharField(max_length=20)
    collegeBus = models.CharField(max_length=10)
    aadharNo = models.CharField(max_length=20)
    fee_reimbursement = models.CharField(max_length=10)
