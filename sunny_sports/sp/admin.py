from django.contrib import admin

# Register your models here.
from modules import *
from modules.models import *

admin.site.register(student.StudentProperty)
admin.site.register(coach.CoachProperty)
admin.site.register(judge.JudgeProperty)
admin.site.register(team.Team)
admin.site.register(association.Student)
admin.site.register(association.Coach)
admin.site.register(association.Judge)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Game)
admin.site.register(StudentTeam)
admin.site.register(Event)
admin.site.register(Umpire)
admin.site.register(GameEvent)
admin.site.register(TeamGame)
admin.site.register(StudentEvent)
