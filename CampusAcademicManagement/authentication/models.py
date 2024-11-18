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
