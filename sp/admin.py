from django.contrib import admin

# Register your models here.
from models import *
from models.models import *

admin.site.register(role.CoachProperty)
admin.site.register(role.Club)
admin.site.register(role.Coach)
admin.site.register(role.CoachOrg)
admin.site.register(train.Train)
admin.site.register(centre.Centre)
admin.site.register(MyUser)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(association.CoachTrain)

