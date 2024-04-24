from django.db import models


# Create your models here.
DEPARTMENT_CHOICES = [
        ('CSCI', 'Computer Science'),
        ('SENG', 'Software Engineering'),
        ('DASC', 'Data Science'),
    ]

SEMESTER_CHOICES = [
    ('spring', 'Spring'),
    ('fall', 'Fall'),
    ('summer', 'Summer'),
]


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
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=4, blank=True, null=True, default='CSCI')
    position = models.CharField(max_length=100, blank=True)
    office = models.CharField(max_length=100, blank=True)
    research_interest = models.CharField(max_length=500, blank=True)
    remarks = models.CharField(max_length=300, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    img_url = models.URLField(blank=True, null=True)
    year_of_joining = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    course_name = models.CharField(max_length=100)
    course_semester = models.CharField(choices=SEMESTER_CHOICES, max_length=6, blank=True, null=True)
    course_description = models.CharField(max_length=500, blank=True, null=True)
    course_credit = models.FloatField(blank=True, null=True)
    graduate_divisor = models.FloatField(blank=True, null=True)
    undergraduate_divisor = models.FloatField(blank=True, null=True)
    course_faculty = models.ManyToManyField(Faculty, blank=True)
    course_img_url = models.URLField(blank=True, null=True)
    enrolled_students = models.ManyToManyField('Student', related_name='courses_enrolled', blank=True)
    # e.g., 'CSCI', 'SENG', 'DASC'
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=4, blank=True, null=True, default='CSCI')
    is_graduate = models.BooleanField()

    @property
    def enrollment(self):
        return self.enrolled_students.count()

    def calculate_fte(self):
        enrollment = self.enrollment
        credit_hours = self.course_credit
        divisors = {
            ('CSCI', True): 186.23,
            ('CSCI', False): 406.24,
            ('SENG', True): 90.17,
            ('SENG', False): 232.25,
            ('DASC', True): 186.23,  # Assuming DASC doesn't differentiate
            ('DASC', False): 186.23,  # between grad and undergrad
        }
        divisor = divisors.get((self.department, self.is_graduate))
        if divisor:
            return (credit_hours * enrollment) / divisor
        return 0  # FTE cannot be calculated without proper divisor

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
