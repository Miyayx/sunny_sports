from django.contrib import admin

# Register your models here.
from models import *
from models.models import *


admin.site.register(role.StudentProperty)
admin.site.register(role.CoachProperty)
admin.site.register(role.JudgeProperty)
admin.site.register(role.Club)
admin.site.register(role.Student)
admin.site.register(role.Coach)
admin.site.register(role.Judge)
admin.site.register(role.CoachOrg)
admin.site.register(train.Train)
admin.site.register(centre.Centre)
admin.site.register(MyUser)
admin.site.register(Role)
admin.site.register(association.CoachTrain)

#admin.site.register(game.Team)
#admin.site.register(Game)
#admin.site.register(StudentTeam)
#admin.site.register(Event)
#admin.site.register(Umpire)
#admin.site.register(GameEvent)
#admin.site.register(TeamGame)
#admin.site.register(StudentEvent)

#import data
