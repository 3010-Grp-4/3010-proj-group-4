from django.db import models


# Create your models here.

class UserSetting(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_notifications_enabled = models.BooleanField(default=True)
    font_size = models.IntegerField(default=12)
    profile_img_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)


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


class Course(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    course_description = models.CharField(max_length=500)
    course_credit = models.FloatField()
    course_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course_img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.course_code + ' - ' + self.course_name


class Student(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    program = models.CharField(max_length=100, blank=True)
    batch = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
