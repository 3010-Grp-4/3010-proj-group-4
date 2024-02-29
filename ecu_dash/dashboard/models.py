from django.db import models


# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=True)
    rank = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    office = models.CharField(max_length=100, blank=True)
    research_interest = models.CharField(max_length=500, blank=True)
    remarks = models.CharField(max_length=300, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name