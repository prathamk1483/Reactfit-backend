from django.db import models
from .appUsers import AppUsers
from django.utils import timezone

class WaterIntake(models.Model):
    user = models.ForeignKey(AppUsers, on_delete=models.CASCADE, related_name='water_logs')
    date = models.DateField(default=timezone.now)
    current_intake_ml = models.PositiveIntegerField(default=0)
    daily_goal_ml = models.PositiveIntegerField(default=3000)
    
    # Timestamp of last sip for "Reminder Time" logic
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')