from django.db import models
from .appUsers import AppUsers 
from django.utils import timezone

class DietLog(models.Model):
    user = models.ForeignKey(AppUsers, on_delete=models.CASCADE, related_name='diet_logs')
    date = models.DateField(default=timezone.now)
    
    # Food Details
    title = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(default=0)
    
    # Macros
    protein_g = models.PositiveIntegerField(default=0)
    carbs_g = models.PositiveIntegerField(default=0)   # <--- New Field
    fat_g = models.PositiveIntegerField(default=0)     # <--- New Field
    
    # Time Details
    time = models.CharField(max_length=10)   # e.g., "08:30"
    period = models.CharField(max_length=2)  # "AM" or "PM"

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.calories} kcal)"