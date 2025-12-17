from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUsers  # This now works because of Step 2
from .models.waterIntake import WaterIntake
from .models.dietLogs import DietLog

admin.site.register(AppUsers, UserAdmin)
admin.site.register(WaterIntake)
admin.site.register(DietLog)