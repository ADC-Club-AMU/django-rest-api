from django.db import models
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import calendar

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year() + 4)(value) 

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+4)]

def month_choices():
    return [(i, calendar.month_name[i]) for i in range(1,13)]

def semester_choices():
    return [(i,i) for i in range(1,11)]


EXAM_CHOICES = [
    ('Sessional', 'Sessional'),
    ('Mid-Sem', 'Mid-Sem'),
    ('Practical', 'Practical'),
    ('End-Sem','End-Sem')
]

# Create your models here.

class Faculty(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(editable=False,max_length=100,primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Faculty, self).save()


class Department(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(editable=False,max_length=100,primary_key=True)
    faculty = models.ForeignKey(Faculty,related_name='department',on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Department, self).save()


class Event(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True)
    faculty = models.ForeignKey(Faculty,related_name='events',on_delete=models.CASCADE,null=True, blank=True)
    department = models.ForeignKey(Department,related_name='events',on_delete=models.CASCADE,null=True, blank=True)
    venue = models.CharField(max_length=100,blank=True,null=True)
    year = models.PositiveIntegerField(choices=year_choices(),default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    month = models.PositiveIntegerField(choices=month_choices(),validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    slug = models.SlugField(editable=False,max_length=100)
    
    def __str__(self):
        return f'{self.title} on {self.slug}'

    def save(self):
        # if not self.slug:
        self.slug = f'{self.day}-{self.month}-{self.year}'
        super(Event, self).save()


class Examination(models.Model):
    subject = models.CharField(max_length=100, blank=True, default='')
    code = models.CharField(max_length=100, blank=True, default='')
    semester = models.PositiveIntegerField(choices=semester_choices(),validators=[MinValueValidator(1), MaxValueValidator(10)])
    exam_type = models.CharField(max_length=100,blank=True,choices=EXAM_CHOICES)
    faculty = models.ForeignKey(Faculty,related_name='examinations',on_delete=models.CASCADE)
    department = models.ForeignKey(Department,related_name='examinations',on_delete=models.CASCADE)
    year = models.PositiveIntegerField(choices=year_choices(),default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    month = models.PositiveIntegerField(choices=month_choices(),validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    slug = models.SlugField(editable=False,max_length=100)
    
    def __str__(self):
        return f"{self.subject} ({self.code})'s {self.exam_type} on {self.slug}"
    
    def save(self):
        # if not self.slug:
        self.slug = f'{self.day}-{self.month}-{self.year}'
        super(Examination, self).save()


class EntranceExamination(models.Model):
    course = models.CharField(max_length=100, blank=True, default='')
    year = models.PositiveIntegerField(choices=year_choices(),default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    month = models.PositiveIntegerField(choices=month_choices(),validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    slug = models.SlugField(editable=False,max_length=100)

    class Meta:
        ordering = ['year','month','day']
    
    def __str__(self):
        return f"{self.course}'s exam on {self.slug}"
    
    def save(self):
        # if not self.slug: 
        self.slug = f'{self.day}-{self.month}-{self.year}'
        super(EntranceExamination, self).save()


class Notice(models.Model):
    text = models.TextField(blank=True, null=True)
    file_url = models.CharField(max_length=100, blank=True, default='')
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"
    

class Holiday(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    year = models.PositiveIntegerField(choices=year_choices(),default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    month = models.PositiveIntegerField(choices=month_choices(),validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    slug = models.SlugField(editable=False,max_length=100)

    class Meta:
        ordering = ['year','month','day']

    def __str__(self):
        return f"{self.title} on {self.slug}"
    
    def save(self):
        # if not self.slug: 
        self.slug = f'{self.day}-{self.month}-{self.year}'
        super(Holiday, self).save()


class Staff(models.Model):
    user = models.OneToOneField(User,related_name='staff_of',on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.faculty}'