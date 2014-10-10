from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=10)
    
class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=32)
    role = models.ForeignKey(Role)
    
class StudentProperty(models.Model):
    stu_id = models.CharField(max_length=15)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    email = models.EmailField()
    phone = models.IntegerField()
    birthday = models.DateField()
    age = models.IntegerField()
    identity = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    photo = models.URLField()
    company = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
class Student(models.Model):
    property = models.ForeignKey(StudentProperty)
    club_id = models.IntegerField()
    level = models.IntegerField()
    status = models.IntegerField()
    regtime = models.DateTimeField()
    
class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    sponsor = models.CharField(max_length=50)
    coorganizer = models.CharField(max_length=200)
    begin_time = models.DateTimeField()
    sign_time = models.DateTimeField()
    end_time = models.DateTimeField()
    team_max = models.IntegerField()
    team_min = models.IntegerField()
    status = models.IntegerField()
    
class Group(models.Model):
    group_id = models.CharField(max_length=15)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    principal = models.CharField(max_length=20)
    contact = models.CharField(max_length=30)
    regtime = models.DateTimeField()
    
class StudentGroup(models.Model):
    group = models.ForeignKey(Group)
    student = models.ForeignKey(Student)
    game = models.ForeignKey(Game)
    stu_number = models.CharField(max_length=20)
    stu_status = models.IntegerField()
    
class Event(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    
class Umpire(models.Model):
    name = models.CharField(max_length=10)
    level = models.IntegerField()
    
class GameEvent(models.Model):
    game = models.ForeignKey(Game)
    event = models.ForeignKey(Event)
    property = models.IntegerField()
    umpires = models.CharField(max_length=20)
    
class GroupGame(models.Model):
    group = models.ForeignKey(Group)
    game = models.ForeignKey(Game)
    group_num = models.CharField(max_length=20)
    group_name = models.CharField(max_length=30)
    group_principal = models.CharField(max_length=20)
    prin_contact = models.CharField(max_length=30)
    group_status = models.IntegerField()
    score = models.IntegerField()
    award = models.CharField(max_length=50)
    pay_status = models.IntegerField()
    members = models.CharField(max_length=100)
    
class StudentEvent(models.Model):
    event = models.ForeignKey(GameEvent)
    stu_number = models.CharField(max_length=20)
    group_num = models.CharField(max_length=20)
    score = models.IntegerField()
    award = models.CharField(max_length=50)
    