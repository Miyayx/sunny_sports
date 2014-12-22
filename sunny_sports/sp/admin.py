from django.contrib import admin

# Register your models here.
from models import *
from models.models import *

admin.site.register(role.StudentProperty)
admin.site.register(role.CoachProperty)
admin.site.register(role.JudgeProperty)
admin.site.register(game.Team)
admin.site.register(association.Student)
admin.site.register(association.Coach)
admin.site.register(association.Judge)
admin.site.register(train.Train)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Game)
admin.site.register(StudentTeam)
admin.site.register(Event)
admin.site.register(Umpire)
admin.site.register(GameEvent)
admin.site.register(TeamGame)
admin.site.register(StudentEvent)
